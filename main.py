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

from methods import get_all_vacancies

if __name__ == "__main__":
    get_all_vacancies()