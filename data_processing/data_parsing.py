import streamlit as st
import json
import os

from methods import __send_request__

methods = ["vacancies"]
experience_list = [
    {"id": "noExperience", "name": "Нет опыта"},
    {"id": "between1And3", "name": "От 1 года до 3 лет"},
    {"id": "between3And6", "name": "От 3 до 6 лет"},
    {"id": "moreThan6", "name": "Более 6 лет"},
]


def parse_vacancies(text, experience):
    os.makedirs("jsons", exist_ok=True)
    with open(f"jsons/{methods[0]}.json", "w", encoding="utf8") as file:
        page = 0
        params_vacancies = {
            "experience": experience_list[experience]["id"],
            "page": page,
            "per_page": 100,
            "text": text,
            "premium": False,
        }

        vacancy_count = 0
        per_page = 100
        response_json = __send_request__(endpoint=methods[0], params=params_vacancies)

        bar = st.progress(0)
        for page in range(0, 19):
            params_vacancies = {
                "experience": experience_list[experience]["id"],
                "page": page,
                "per_page": per_page,
                "text": text,
                "premium": False,
            }

            answer = __send_request__(endpoint=methods[0], params=params_vacancies)
            print(
                f"page = {page}, len = {len(answer['items'])}, {len(response_json['items'])}"
            )
            response_json["items"] += answer["items"]

            bar.progress((page + 1) / 19)
            vacancy_count += len(answer["items"])
            if page * per_page >= answer["found"]:
                bar.progress(0.99)
                break
        json.dump(response_json, file, ensure_ascii=False, indent=3)

    return vacancy_count
    st.success(f"Обработано вакансий: {vacancy_count} / {len(response_json['items'])}")
