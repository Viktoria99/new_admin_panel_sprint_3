from sql import (
    select_film,
    select_film_count,
    select_film_genre,
    select_film_person,
)


def get_batch_count(raws: int, batch_size: int) -> int:
    batch_count = round(raws / batch_size)
    if raws < batch_size:
        batch_count = 1
    if ((raws / batch_size) - batch_count) > 0:
        batch_count += 1
    return batch_count


def get_sql_film_count(date: str):
    return select_film_count.format(date)


def get_sql_film(date: str):
    return select_film.format(date)


def get_sql_person_film():
    return select_film_person


def get_sql_genre_film():
    return select_film_genre


def get_first(item: tuple):
    return item[0]
