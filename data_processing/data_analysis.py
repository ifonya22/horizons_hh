import os

# import streamlit as st
import pandas as pd
import uuid
from datetime import datetime


def analysis(job_query, next_search_date):
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
        "вакансия",
        "зарплата от",
        "зарплата до",
        "Валюта",
        "Локация",
        "Опубликовано",
        "Работодатель",
        "Роль",
        "Опыт",
        "Ссылка на вакансию",
    ]

    # дропаем строки с пустой зарплатой, заполняем зп, если указана
    # одна сторона вилки, приводим в порядок дату, делаем нормальный индекс
    # добавляем среднюю зп
    df["зарплата от"].fillna("0", inplace=True)
    df = df.drop(df[df["зарплата от"] == "0"].index)
    df["зарплата до"].fillna(df["зарплата от"], inplace=True)
    df["Опубликовано"] = pd.to_datetime(df["Опубликовано"]).dt.date
    df.reset_index(drop=True, inplace=True)
    df["средняя"] = (df["зарплата от"] + df["зарплата до"]) / 2

    # сохраняем файл
    os.makedirs("csv", exist_ok=True)
    df.to_csv("csv/clean_vac.csv", sep="\t", encoding="utf-8")
    uuid = create_uuid()
    df.to_csv(f"csv/{uuid}.csv", sep="\t", encoding="utf-8")
    insert_uuid(uuid, job_query, next_search_date)
    return True, len(df)


def create_uuid():

    return str(uuid.uuid4())


def insert_uuid(uuid, job_query, next_search_date):
    df = pd.read_csv("csv/results.csv", sep=",", index_col=0)
    df.loc[len(df.index)] = [
        uuid,
        job_query.replace(" ", "_"),
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        next_search_date,
    ]
    df.to_csv("csv/results.csv", sep=",")
