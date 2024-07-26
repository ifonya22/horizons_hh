import os

# import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

from data_processing.connect import engine

def analysis(job_query, next_search_date, experience):
    with open("jsons/vacancies.json", encoding="utf-8") as inputfile:
        myfile = pd.read_json(inputfile)

    # из json забираем словарь, в котором находятся информативные поля
    mydict = []
    for i in range(len(myfile["items"])):
        mydict.append(myfile["items"][i])
        # print (mydict)

    # далее идут блоки, где мы из словаря формируем столбцы датафрейма
    name = []
    salaryfr = []
    salaryto = []
    salarycur = []
    area = []
    publish = []
    employer = []
    prole = []
    exp = []
    vacancy_url = []
    count = len(mydict)

    for i in range(count):
        name.append(mydict[i]["name"])
        try:
            salaryfr.append(mydict[i]["salary"]["from"])
        except Exception as e:
            print(f"Внимание! {e}")
            salaryfr.append("0")

        try:
            salaryto.append(mydict[i]["salary"]["to"])
        except Exception as e:
            print(f"Внимание! {e}")
            salaryto.append("0")

        try:
            salarycur.append(mydict[i]["salary"]["currency"])
        except Exception as e:
            print(f"Внимание! {e}")
            salarycur.append("0")

        area.append(mydict[i]["area"]["name"])
        publish.append(mydict[i]["published_at"])
        employer.append(mydict[i]["employer"]["name"])
        prole.append(mydict[i]["professional_roles"][0]["name"])
        exp.append(mydict[i]["experience"]["name"])
        vacancy_url.append(mydict[i]["alternate_url"])

    # собираем датафрейм, транспонируя списки с данными из hh api.
    # Задаем имена столбцов
    data = []
    data.append(name)
    data.append(salaryfr)
    data.append(salaryto)
    data.append(salarycur)
    data.append(area)
    data.append(publish)
    data.append(employer)
    data.append(prole)
    data.append(exp)
    data.append(vacancy_url)
    df = pd.DataFrame(data).transpose()
    df.columns = [
        "req_str",
        "sal_from",
        "sal_to",
        "currency",
        "city",
        "pub_date",
        "employer",
        "job_title",
        "experience",
        "link",
    ]

    # дропаем строки с пустой зарплатой, заполняем зп, если указана
    # одна сторона вилки, приводим в порядок дату, делаем нормальный индекс
    # добавляем среднюю зп
    df["sal_from"].fillna("0", inplace=True)
    df = df.drop(df[df["sal_from"] == "0"].index)
    df["sal_to"].fillna(df["sal_from"], inplace=True)
    df["pub_date"] = pd.to_datetime(df["pub_date"]).dt.date
    df.reset_index(drop=True, inplace=True)
    df["average_value"] = (df["sal_from"] + df["sal_to"]) / 2

    uuid = create_uuid()
    df['search_date'] = [datetime.now().strftime("%d-%m-%Y %H:%M:%S") for _ in range(len(df))]
    df['uuid'] = [uuid for _ in range(len(df))]
    # df['req_str'] = [job_query for _ in range(len(df))]
    # сохраняем файл
    os.makedirs("csv", exist_ok=True)
    # df.to_csv("csv/clean_vac.csv", sep="\t", encoding="utf-8")
    df.to_sql('gen_table', con=engine, if_exists='append', index=False)
    
    # df.to_csv(f"csv/{uuid}.csv", sep="\t", encoding="utf-8")
    if next_search_date is not None:
        insert_uuid(uuid, job_query, next_search_date, experience)
    return True, len(df)


def create_uuid():

    return str(uuid.uuid4())


def insert_uuid(uuid, job_query, next_search_date, experience):
    # df = pd.read_csv("csv/results.csv", sep=",", index_col=0)
    df = pd.DataFrame(columns=['uuid', 'req_str', 'experience', 'last_search_date', 'next_search_date', 'csv'])
    df.loc[len(df.index)] = [
        uuid,
        job_query.replace(" ", "_"),
        experience,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        next_search_date,
        'csv',
    ]
    # df.to_csv("csv/results.csv", sep=",")
    df.to_sql('schedule_table', con=engine, if_exists='append', index=False)


from sqlalchemy import select
import pandas as pd
from data_processing.connect import Session
from data_processing.models import ScheduleTable
from sqlalchemy import create_engine, text
def get_schedule_data():

    # session = Session()
    # query = select(
    #     ScheduleTable.uuid,
    #     ScheduleTable.req_str,
    #     ScheduleTable.experience,
    #     ScheduleTable.last_search_date,
    #     ScheduleTable.next_search_date
    # )

    # result = session.execute(query).fetchall()
    # df_schedule = pd.DataFrame(result, columns=['uuid', 'req_str', 'experience', 'last_search_date', 'next_search_date'])
    # df_schedule['last_search_date'] = pd.to_datetime(df_schedule['last_search_date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    # df_schedule['next_search_date'] = pd.to_datetime(df_schedule['next_search_date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

    # session.close()
#     engine = create_engine('sqlite:///mydatabase.db')  # Замените на ваш URL соединения

# # Выполните запрос
#     with engine.connect() as connection:
#         sql_query = text("""
#             SELECT uuid, req_str, experience, last_search_date, next_search_date
#             FROM schedule_table
#             """)
    
#     result = connection.execute(sql_query).fetchall()
    
#     # Преобразование результатов в DataFrame
#     df_schedule = pd.DataFrame(result, columns=['uuid', 'req_str', 'experience', 'last_search_date', 'next_search_date'])
    
#     # Преобразование столбцов в формат даты и времени
#     df_schedule['last_search_date'] = pd.to_datetime(df_schedule['last_search_date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
#     df_schedule['next_search_date'] = pd.to_datetime(df_schedule['next_search_date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    import sqlite3
    conn = sqlite3.connect('/database/mydatabase.db')

    # Создание курсора для выполнения запросов
  

    # Выполнение запроса для получения списка всех таблиц
    df = pd.read_sql_query("SELECT * FROM 'schedule_table'", conn)
    conn.close()

    print(df)
    return df
