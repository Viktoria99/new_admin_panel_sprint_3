import contextlib

import backoff
import psycopg
from psycopg.rows import dict_row

from settings import BATCH_SIZE, FILM_COUNT, DSL
from utils import get_batch_count, get_sql_film, get_sql_film_count


class ProducerService:
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
        with contextlib.closing(psycopg.connect(**DSL)) as pg_conn:
            with pg_conn.cursor(row_factory=dict_row) as cur:
                raws = cur.execute(get_sql_film_count(load_date)).fetchone()
                batch_count = get_batch_count(raws[FILM_COUNT], BATCH_SIZE)

                sql_film = get_sql_film(load_date)
                cur.execute(sql_film)
                for i in range(batch_count):
                    film_list = cur.fetchmany(BATCH_SIZE)
                    yield film_list
                pg_conn.commit()
