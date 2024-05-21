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

from methods import get_method
methods = ["vacancies"]

if __name__ == "__main__":
    # for method in methods:
    #     get_method(endpoint=method)
    
    params = {
"experience":"between1And3",
"per_page":"100",
"employment":"full",
"schedule":"fullDay",
"vacancy_search_fields":"name",
"gender":"male",
"education_level":"higher",
"text":"python разработчик",
"area":"1261"
    }
    get_method(endpoint=methods[0], params=params)