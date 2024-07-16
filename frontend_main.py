import datetime
import streamlit as st
import time
import pandas as pd

from data_processing.data_parsing import parse_vacancies
from data_processing.data_analysis import analysis
from data_processing.data_visualization import visualization


st.title("Поиск вакансий")

tab = st.sidebar.radio(
    "Выберите вкладку",
    ["Добавление вакансий в очередь для парсинга", "Текущие поиски", "Вкладка 3"],
)
if tab == "Добавление вакансий в очередь для парсинга":
    job_query = st.text_input(
        "Введите запрос для поиска вакансии", "Java backend разработчик"
    )

    experience_options = {
        "Нет опыта": 0,
        "От 1 года до 3 лет": 1,
        "От 3 до 6 лет": 2,
        "Более 6 лет": 3,
    }
    experience = st.radio("Введите опыт работы:", list(experience_options.keys()))

    st.date_input(
        "Дата следующего поиска", value=datetime.date.today(), key="next_search_date"
    )
    if st.button("Поиск"):
        with st.spinner("Идет поиск..."):
            time.sleep(1)
            vacancy_count = parse_vacancies(
                text=job_query, experience=experience_options[experience]
            )

            next_search_date = st.session_state.next_search_date.strftime("%d-%m-%Y")

            result, cleared_vacancy_count = analysis(job_query, next_search_date)

            if result:
                st.success("Обработка завершена. Данные очищены")
                st.success(
                    f"Осталось {cleared_vacancy_count} вакансий из {vacancy_count} найденных"
                )
                st.session_state.search_completed = True
            else:
                st.session_state.search_completed = False

    # if st.session_state.get("search_completed", False):
    #     visualization()
elif tab == "Текущие поиски":

    df = pd.read_csv("csv/results.csv", sep=",", index_col=0)

    @st.cache_data(experimental_allow_widgets=True)
    def download_row_as_csv(row):
        # csv = row.to_csv()
        csv = pd.read_csv(f"csv/{row['uuid']}.csv", sep="\t", index_col=0)
        csv = csv[
            [
                "вакансия",
                "зарплата от",
                "зарплата до",
                "средняя",
                "Валюта",
                "Локация",
                "Опубликовано",
                "Работодатель",
                "Роль",
                "Опыт",
                "Ссылка на вакансию",
            ]
        ].to_csv()
        st.download_button(
            label=f"Скачать {row['Название вакансии']}",
            data=csv,
            file_name=f"{row['Название вакансии']}_{datetime.datetime.now()}.csv",
            mime="text/csv",
        )

    st.title("Скачивание отчётов")
    for index, row in df.iterrows():
        st.write(
            f"{row['Название вакансии']} - {row['Время создания']} - {row['Дата следующего отчета']}"
        )
        download_row_as_csv(row)
