from datetime import datetime, time

from EnricherService import EnricherService
from logger import logger_load
from ProducerService import ProducerService
from settings import STATE_KEY
from State import State
from TransformService import TransformService


def main():

    state_storage = State()
    producer_service = ProducerService()
    richer_service = EnricherService()
    transform_service = TransformService()

    load_date = state_storage.get_state(STATE_KEY)
    logger_load.info(
        'Дата начала импорта данных = {date_load}'.format(date_load=load_date)
    )
    print('ДАТА = {dt}'.format(dt=load_date))
    for item in producer_service.get_film(load_date):
        films = richer_service.richer_films(item, load_date)
        transform_service.save_etl(films)

    loc_dt = datetime.now()
    str_date = loc_dt.strftime('%Y-%m-%d %H:%M:%S')
    state_storage.set_state(STATE_KEY, str_date)
    logger_load.info(
        'Окончание импорта данных = {end_date}'.format(end_date=str_date)
    )


if __name__ == '__main__':

    while True:
        try:
            main()
            time.sleep(120)
        except Exception as e:
            logger_load.exception(e)
