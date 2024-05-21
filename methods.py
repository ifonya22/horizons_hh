from requests import Session
import json
import os
import glob
from datetime import datetime

base_url = "https://api.hh.ru/"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-type": "application/json"
} # type: ignore

def __send_request__(endpoint=None, params :dict=None):
    url = base_url + endpoint
    print(f"Requesting {endpoint}")
    with Session() as current_session:
        current_session.headers = HEADERS
        response = current_session.get(url=url, headers=HEADERS, params=params)
        status_code = response.status_code
        if status_code == 400:
            raise Exception(f"Error request with code {status_code}")
        print(f"Response status = {status_code}")
    return response.json()

# TODO преобразовать к функции с одним параметром(ендпоинт). При сохранении файла слеш меняется на землю _
def get_method(endpoint: str=None, params :dict=None):
    response_json = __send_request__(endpoint, params=params)
    now = datetime.now().strftime('%dT%H%M')
    with open('jsons/'+endpoint+now+'.json', 'w', encoding='utf8') as file:
        json.dump(response_json, file, ensure_ascii=False, indent=3)

def get_areas():
    endpoint = 'areas'
    url = base_url + endpoint
    print(f"Requesting All Areas")

def clean_folfer_jsons(directory):
    '''
    Очищаем директорию
    '''
    # Создаем путь к шаблону всех файлов в директории
    files = glob.glob(os.path.join(directory, '*'))
    for file in files:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"File {file} has been deleted.")
            elif os.path.isdir(file):
                print(f"Directory {file} is not deleted. This script only removes files.")
        except Exception as e:
            print(f"Error occurred while deleting file {file}: {e}")

def choose_option():
    pass

# endpoint = "vacancies"
# url = base_url + endpoint
# print(f"url = {url}")
# with Session() as current_session:
#     current_session.headers = HEADERS
#     response = current_session.get(url=url, headers=HEADERS)
# data = response.json()
# with open('vacancies.json', 'w', encoding='utf8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=3)