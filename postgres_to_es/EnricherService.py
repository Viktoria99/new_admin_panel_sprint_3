import contextlib
from typing import List

import psycopg
from psycopg.rows import class_row, tuple_row

from logger import logger_load
from models import Film, Movie_item, Person
from constants import (
    ACTOR,
    ACTORS,
    ACTORS_NAMES,
    DIRECTOR,
    DIRECTORS,
    DIRECTORS_NAMES,
    GENRES,
    WRITER,
    WRITERS,
    WRITERS_NAMES
)
from sql import select_one_film
from utils import get_first, get_sql_genre_film, get_sql_person_film

from pydantic_settings import BaseSettings
from psycopg.conninfo import make_conninfo

class EnricherService:
    dsn: str

    def __init__(self, settings_db: BaseSettings) -> None:
        connect_db = settings_db.database_settings.get_dsn()
        self.dsn = make_conninfo(connect_db)

    def richer_films(self, id_list: List) -> List:
        film_list = []
        for id in id_list:
            try:
                film = self.get_film(id['id'])
                film.__dict__['imdb_rating'] = film.rating
                del film.rating

                genres = self.get_film_genre(id['id'])
                film.__dict__[GENRES] = genres

                film_card = self.get_film_person(id['id'], film)
                film_list.append(film_card)
            except Exception as err:
                logger_load.error(
                    'Film_Id-{Id}: def richer_films -> {Errors}'.format(
                        Id=id['id'], Errors=err.args
                    )
                )
        return film_list

    def get_film(self, film_id: str) -> Film:
        with contextlib.closing(
            psycopg.connect(self.dsn, row_factory=class_row(Film))
        ) as pg_conn:
            with pg_conn.cursor() as cur:
                sql = select_one_film.format(film_id)
                film = cur.execute(sql).fetchone()
                return film

    def get_film_genre(self, film_id: str) -> List:
        with contextlib.closing(
            psycopg.connect(self.dsn, row_factory=tuple_row)
        ) as pg_conn:
            with pg_conn.cursor() as cur:
                genre_sql = get_sql_genre_film()
                genre_list = cur.execute(genre_sql, (film_id,)).fetchall()
                genres = [map(get_first, genre_list)]
                return genres

    def get_film_person(self, film_id: str, film: Film) -> Film:
        with contextlib.closing(
            psycopg.connect(self.dsn, row_factory=class_row(Person))
        ) as pg_conn:
            with pg_conn.cursor() as cur:
                sql = get_sql_person_film()
                person_list = cur.execute(sql, (film_id,)).fetchall()

                film.__dict__[DIRECTORS_NAMES] = [
                    person.full_name
                    for person in person_list
                    if person.role == DIRECTOR
                ]
                film.__dict__[ACTORS_NAMES] = [
                    person.full_name
                    for person in person_list
                    if person.role == ACTOR
                ]
                film.__dict__[WRITERS_NAMES] = [
                    person.full_name
                    for person in person_list
                    if person.role == WRITER
                ]
                film.__dict__[DIRECTORS] = [
                    Movie_item(person.id, person.full_name)
                    for person in person_list
                    if person.role == DIRECTOR
                ]
                film.__dict__[ACTORS] = [
                    Movie_item(person.id, person.full_name)
                    for person in person_list
                    if person.role == ACTOR
                ]
                film.__dict__[WRITERS] = [
                    Movie_item(person.id, person.full_name)
                    for person in person_list
                    if person.role == WRITER
                ]

                return film
