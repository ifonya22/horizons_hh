import streamlit as st
import time

from data_processing.data_parsing import parse_vacancies
from data_processing.data_analysis import analysis
from data_processing.data_visualization import visualization


st.title("Поиск вакансий")

job_query = st.text_input(
    "Введите запрос для поиска вакансии", "Java backend разработчик"
)

experience_options = {
    "Нет опыта": 0,
    "От 1 года до 3 лет": 1,
    "От 3 до 6 лет": 2,
    "Более 6 лет": 3
}
experience = st.radio("Введите опыт работы:", list(experience_options.keys()))

if st.button("Поиск"):
    with st.spinner("Идет поиск..."):
        time.sleep(1)
        parse_vacancies(
            text=job_query,
            experience=experience_options[experience]
        )
        result = analysis()
        if result:
            st.success('Обработка завершена. Данные очищены')
            st.session_state.search_completed = True
        else:
            st.session_state.search_completed = False

if st.session_state.get('search_completed', False):
    visualization()
