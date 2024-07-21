
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_')
    host: str = Field('localhost', alias='host')
    port: int = Field(5432, alias='port')
    dbname: str = Field('moviesdb', alias='dbname')
    user: str = 'adminmovies'
    password: str = 'admin24qwl'

    def get_dsn(self) -> dict:
        return self.model_dump()

class ElasticsearchSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='es_')
    host: str = 'localhost'
    port: str = '9200'

    def get_host(self):
        return f'http://{self.host}:{self.port}'

class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()
    elasticsearch_settings: ElasticsearchSettings = ElasticsearchSettings()

settings = Settings()

BATCH_SIZE = 100
STATE_KEY = 'last_load_date'
ETL_INDEX = 'movies'

FILM_COUNT = 'count'

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_PATH = BASE_DIR / 'postgres_to_es/state_storage/stateFilm.txt'
