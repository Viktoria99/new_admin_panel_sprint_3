import json
from typing import List

import backoff
from elasticsearch import ConnectionError, ConnectionTimeout, Elasticsearch
from elasticsearch.helpers import bulk

from logger import logger_load
from settings import ELASTIC_URL, ETL_INDEX
from pydantic_settings import BaseSettings

class TransformService:
    def __init__(self, settings_elt: BaseSettings):
        connect_etl = settings_elt.elasticsearch_settings.get_host()
        self.etl_client = Elasticsearch(connect_etl)


    def gendata(self, films: List):
        for item in films:
            item.id = str(item.id)
            del item.modified
            result = json.dumps(item.__dict__)
            yield dict(_index=ETL_INDEX, _id=item.id, body=result)

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger_load
    )
    @backoff.on_exception(
        backoff.expo,
        ConnectionTimeout,
        max_tries=5,
        jitter=backoff.random_jitter,
        logger=logger_load
    )
    def save_etl(self, films:List):
       bulk(self.etl_client, self.gendata(films))
