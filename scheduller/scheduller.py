import sqlite3
from datetime import datetime, timedelta
from data_processing.data_analysis import analysis
from data_processing.data_parsing import parse_vacancies
import schedule
import time

def parse(req_str, experience):
    vacancy_count = parse_vacancies(text=req_str, experience=experience)
    result, cleared_vacancy_count = analysis(req_str, None, experience)

    print(f"Parsing with req_str: {req_str} and experience: {experience}")

def update_search_dates():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    print('start')
    
    # today = datetime.now().date()
    today = datetime.now().strftime('%d-%m-%Y')
    
    cursor.execute("SELECT idschedule_table, req_str, experience FROM 'schedule_table' WHERE next_search_date = ?", (today,))
    rows = cursor.fetchall()
    print(f"rows = {today}")
    
    for row in rows:
        record_id, req_str, experience = row
        
        print(f"req_str = {req_str}, experience = {experience}")
        parse(req_str, int(experience))
        
        today = datetime.now().date()
        new_date = today + timedelta(days=30)
        
        cursor.execute("UPDATE my_table SET 'schedule_table' = ? WHERE idschedule_table = ?", (new_date, record_id))
    
    conn.commit()
    conn.close()

# schedule.every().day.at("00:00").do(update_search_dates)
schedule.every(15).seconds.do(update_search_dates)

while True:
    schedule.run_pending()
    # time.sleep(60)
