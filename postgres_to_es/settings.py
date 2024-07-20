import os
from pathlib import Path

DSL = {
    'dbname': os.environ.get('dbname', 'moviesdb'),
    'user': os.environ.get('user', 'adminmovies'),
    'password': os.environ.get('password', 'admin24qwl'),
    'host': os.environ.get('host', 'localhost'),
    'port': os.environ.get('port', 5432),
    'options': os.environ.get('options', '-c search_path=content'),
}

BATCH_SIZE = 100
STATE_KEY = 'last_load_date'
ETL_INDEX = 'movies'

WRITER = 'writer'
DIRECTOR = 'director'
ACTOR = 'actor'

DIRECTORS_NAMES = 'directors_names'
ACTORS_NAMES = 'actors_names'
WRITERS_NAMES = 'writers_names'

DIRECTORS = 'directors'
ACTORS = 'actors'
WRITERS = 'writers'
GENRES = 'genres'

FILM_COUNT = 'count'

ELASTIC_URL = 'http://localhost:9200/'

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_PATH = BASE_DIR / 'postgres_to_es/state_storage/stateFilm.txt'
