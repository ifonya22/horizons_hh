import sqlite3
from datetime import datetime, timedelta
from data_processing.connect import get_db
from data_processing.models import ScheduleTable
from data_processing.data_analysis import analysis
from data_processing.data_parsing import parse_vacancies
import schedule
import time
import logging
logging.basicConfig(level=logging.WARNING)
def parse(req_str, experience):
    vacancy_count = parse_vacancies(text=req_str, experience=experience)
    result, cleared_vacancy_count = analysis(req_str, None, experience)

    logging.warning(f"Parsing with req_str: {req_str} and experience: {experience}")

def update_search_dates():
    session = next(get_db())
    # try:
    logging.warning('start')
    
    # Определяем текущую дату
    now = datetime.now()

    # Устанавливаем время на полночь
    midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    today = midnight_today.strftime("%Y-%m-%d %H:%M:%S")
    
    # Получаем строки с нужной датой
    rows = session.query(ScheduleTable).filter(ScheduleTable.next_search_date == today).all()
    logging.warning(f"rows = {today}\n{type(today)}")
    
    for row in rows:
        record_id = row.idschedule_table
        req_str = row.req_str
        experience = row.experience
        
        logging.warning(f"req_str = {req_str}, experience = {experience}")
        parse(req_str, int(experience))
        
        # Обновляем дату в `my_table`
        now = datetime.now()

    # Устанавливаем время на полночь
        midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S') 
        new_date = midnight_today + timedelta(days=30)
        new_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
        session.query(ScheduleTable).filter(ScheduleTable.idschedule_table == record_id).update({'next_search_date': new_date})

    
    session.commit()
# except Exception as e:
    # session.rollback()
    # logging.warning(f"Error occurred: {e}")
# finally:
    session.close()

schedule.every().day.at("00:00").do(update_search_dates)
# schedule.every(15).seconds.do(update_search_dates)

while True:
    time.sleep(10)
    schedule.run_pending()
    
