import datetime
from data_processing.connect import get_db
from data_processing.utils import get_data_by_uuid
import streamlit as st
import time
import pandas as pd

from data_processing.data_parsing import parse_vacancies
from data_processing.data_analysis import analysis, get_schedule_data
from data_processing.data_visualization import visualization


st.title("Поиск вакансий")

tab = st.sidebar.radio(
    "Выберите вкладку",
    ["Добавление вакансий в очередь для парсинга", "Отчеты"],
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

    selected_experience = []
    for option, value in experience_options.items():
        if st.checkbox(option, key=value):
            selected_experience.append(value)

    st.date_input(
        "Дата следующего поиска", value=datetime.date.today(), key="next_search_date"
    )

    if st.button("Поиск"):
        if not selected_experience:
            st.warning("Пожалуйста, выберите хотя бы один опыт работы.")
        else:
            with st.spinner("Идет поиск..."):
                time.sleep(1)
                
                total_vacancies_count = 0
                for exp in selected_experience:
                    vacancy_count = parse_vacancies(text=job_query, experience=exp)
                    total_vacancies_count += vacancy_count

                    next_search_date = st.session_state.next_search_date.strftime("%Y-%m-%d %H:%M:%S")

                    result, cleared_vacancy_count = analysis(job_query, next_search_date, exp)

                    if result:
                        st.success("Обработка завершена. Данные очищены")
                        st.success(
                            f"Осталось {cleared_vacancy_count} вакансий из {total_vacancies_count} найденных"
                        )
                        st.session_state.search_completed = True
                    else:
                        st.session_state.search_completed = False

    # if st.session_state.get("search_completed", False):
    #     visualization()
elif tab == "Отчеты":

    # df = pd.read_csv("csv/results.csv", sep=",", index_col=0)

    # @st.cache_data(experimental_allow_widgets=True)
    # def download_row_as_csv(row):
    #     # csv = row.to_csv()
    #     csv = pd.read_csv(f"csv/{row['uuid']}.csv", sep="\t", index_col=0)
    #     csv = csv[
    #         [
    #             "вакансия",
    #             "зарплата от",
    #             "зарплата до",
    #             "средняя",
    #             "Валюта",
    #             "Локация",
    #             "Опубликовано",
    #             "Работодатель",
    #             "Роль",
    #             "Опыт",
    #             "Ссылка на вакансию",
    #         ]
    #     ].to_csv()
    #     st.download_button(
    #         label=f"Скачать {row['Название вакансии']}",
    #         data=csv,
    #         file_name=f"{row['Название вакансии']}_{datetime.datetime.now()}.csv",
    #         mime="text/csv",
    #     )

    # st.title("Скачивание отчётов")
    # for index, row in df.iterrows():
    #     st.write(
    #         f"{row['Название вакансии']} - {row['Время создания']} - {row['Дата следующего отчета']}"
    #     )
    #     download_row_as_csv(row)
    df = get_schedule_data()

    colms = st.columns((1, 2, 2, 2, 2, 2, 2))
    header_names = ["№", 'uuid', "Название вакансии", "Опыт", "Дата создания", "Дата следующего отчета", 'csv']
    for col, field_name in zip(colms, header_names):
        col.write(field_name)

    
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns((1, 2, 2, 2, 2, 2, 2))
        col1.write(row['idschedule_table'])  # index
        col2.write(row['uuid'])  # job
        col3.write(row['req_str'])  # experience
        col4.write(row['experience'])
        col5.write(row['last_search_date'])  # last request time
        col6.write(row['next_search_date'])
        # col7.download_button(label="Скачать CSV", data=csv, file_name=filename, mime='text/csv')
        if col7.button(f"Скачать Отчёт {row['idschedule_table']}", key=f"btn_{i}"):
            # Генерация CSV файла

            filtered_df = get_data_by_uuid(next(get_db()), row['uuid'])
            filename = f"{row['idschedule_table']}.csv"
            csv = filtered_df.to_csv(index=False)
            
            # Использование компонента для скачивания сгенерированного файла
            st.download_button(
                label=f"Скачать {filename}",
                data=csv,
                file_name=filename,
                mime='text/csv'
            )