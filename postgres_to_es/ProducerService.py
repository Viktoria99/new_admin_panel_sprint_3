import contextlib

import backoff
import psycopg
from psycopg.rows import dict_row

from settings import BATCH_SIZE, FILM_COUNT
from utils import get_batch_count, get_sql_film, get_sql_film_count

from pydantic_settings import BaseSettings
from psycopg.conninfo import make_conninfo


class ProducerService:
    dsn: str

    def __init__(self, settings_db: BaseSettings) -> None:
        connect_db = settings_db.database_settings.get_dsn()
        self.dsn = make_conninfo(connect_db)

    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionTimeout,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionException,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    @backoff.on_exception(
        backoff.expo,
        psycopg.errors.ConnectionFailure,
        max_tries=2,
        jitter=backoff.random_jitter,
    )
    def get_film(self, load_date: str) -> None:
        with contextlib.closing(psycopg.connect(self.dsn)) as pg_conn:
            with pg_conn.cursor(row_factory=dict_row) as cur:
                raws = cur.execute(get_sql_film_count(load_date)).fetchone()
                batch_count = get_batch_count(raws[FILM_COUNT], BATCH_SIZE)

                sql_film = get_sql_film(load_date)
                cur.execute(sql_film)
                for i in range(batch_count):
                    film_list = cur.fetchmany(BATCH_SIZE)
                    yield film_list
                pg_conn.commit()
