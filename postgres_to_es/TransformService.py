import json
from typing import List

import backoff
from elasticsearch import ConnectionError, ConnectionTimeout, Elasticsearch

from logger import logger_load
from settings import ELASTIC_URL, ETL_INDEX


class TransformService:
    def __init__(self):
        self.etl_client = Elasticsearch(ELASTIC_URL)

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        jitter=backoff.random_jitter,
    )
    @backoff.on_exception(
        backoff.expo,
        ConnectionTimeout,
        max_tries=5,
        jitter=backoff.random_jitter,
    )
    def save_etl(self, films: List):
        for item in films:
            try:
                item.id = str(item.id)
                del item.modified
                result = json.dumps(item.__dict__)
                self.etl_client.index(index=ETL_INDEX, id=item.id, body=result)
            except Exception as err:
                logger_load.error(
                    'Film_Id-{Id}: def save_etl -> {Errors}'.format(
                        Id=item.id, Errors=err.args
                    )
                )
