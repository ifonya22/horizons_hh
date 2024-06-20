import streamlit as st
import json
import os

from methods import __send_request__

methods = ["vacancies"]
experience_list = [
    {
        "id": "noExperience",
        "name": "Нет опыта"
    },
    {
        "id": "between1And3",
        "name": "От 1 года до 3 лет"
    },
    {
        "id": "between3And6",
        "name": "От 3 до 6 лет"
    },
    {
        "id": "moreThan6",
        "name": "Более 6 лет"
    }
]


def parse_vacancies(text, experience):
    os.makedirs('jsons', exist_ok=True)
    with open(f'jsons/{methods[0]}.json', 'w', encoding='utf8') as file:
        page = 0
        params_vacancies = {
            "experience": experience_list[experience]["id"],
            "professional_role": 96,
            "page": page,
            "per_page": 100,
            "employment": "full",
            "schedule": "fullDay",
            "vacancy_search_fields": "name",
            "gender": "male",
            "education_level": "higher",
            "text": text,
            "area": "113",
            # "only_with_salary": True,
            # "period": 30,
            "premium": False
        }

        vacancy_count = 0
        response_json = __send_request__(
            endpoint=methods[0],
            params=params_vacancies
        )

        bar = st.progress(0)
        for page in range(1, 19):
            params_vacancies = {
                "experience": experience_list[experience]["id"],
                "professional_role": 96,
                "page": page,
                "per_page": 100,
                "employment": "full",
                "schedule": "fullDay",
                "vacancy_search_fields": "name",
                "gender": "male",
                "education_level": "higher",
                "text": text,
                "area": "113",
                # "only_with_salary": True,
                # "period": 30,
                "premium": False
            }

            answer = __send_request__(
                endpoint=methods[0],
                params=params_vacancies
            )["items"]
            response_json["items"] += answer

            bar.progress((page + 1) / 19)
            vacancy_count += len(answer)
        json.dump(response_json, file, ensure_ascii=False, indent=3)

    st.success(f"Обработано вакансий: {vacancy_count}")
