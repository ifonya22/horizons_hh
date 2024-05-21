# from requests import Session
# import json
# base_url = "https://api.hh.ru/"
# HEADERS = {
#     "User-Agent": "Mozilla/5.0",
#     "Content-type": "application/json"
# } # type: ignore

# endpoint = "vacancies"
# url = base_url + endpoint
# print(f"url = {url}")
# with Session() as current_session:
#     current_session.headers = HEADERS
#     response = current_session.get(url=url, headers=HEADERS)
# data = response.json()
# with open('vacancies.json', 'w', encoding='utf8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=3)

from methods import get_method, __send_request__
methods = ["vacancies"]
import json
from datetime import datetime
from time import sleep

if __name__ == "__main__":
    # for method in methods:
    #     get_method(endpoint=method)
    text = input("""____
Введите запрос для поиска вакансии
Например: Java backend разработчик
____
""")
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
    experience = int(input("""____
Введите опыт работы:
0 - Нет опыта
1 - От 1 года до 3 лет
2 - От 3 до 6 лет
3 - Более 6 лет
____
"""))
    while not str(experience) in ['0','1','2','3']:
        print("""
----!!!Опыт работы должен быть указан целым числом от 0 до 3 включительно----""")
        experience = int(input("""____
Введите опыт работы:
0 - Нет опыта
1 - От 1 года до 3 лет
2 - От 3 до 6 лет
3 - Более 6 лет
____
"""))
    now = datetime.now().strftime('%dT%H%M')
    with open('jsons/'+methods[0]+'.json', 'w', encoding='utf8') as file:
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
        response_json = __send_request__(endpoint=methods[0], params=params_vacancies)
        for page in range(1, 19):
            print(f"page = {page}")
            # sleep(3)
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
            response_json["items"] += __send_request__(endpoint=methods[0], params=params_vacancies)["items"]
        json.dump(response_json, file, ensure_ascii=False, indent=3)

    # get_method(endpoint=methods[0], params=params_vacancies)
    # get_method(endpoint='dictionaries')
    # get_method(endpoint='areas')
    # get_method(endpoint='professional_roles')
