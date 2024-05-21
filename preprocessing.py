#открыть файл из директории
import pandas as pd

with open('jsons/vacancies.json', encoding='utf-8') as inputfile:
    myfile = pd.read_json(inputfile)

#из json забираем словарь, в котором находятся информативные поля
mydict = []
for i in range(len(myfile['items'])):
    mydict.append(myfile['items'][i])
    # print (mydict)

#далее идут блоки, где мы из словаря формируем столбцы датафрейма

name = []
salaryfr = []
salaryto = []
salarycur = []
area = []
publish = []
employer = []
prole = []
exp = []
count = len(mydict)
for i in range(count):
    print(f"{i} from {count}")
    name.append(mydict[i]['name'])
    try: 
        salaryfr.append(mydict[i]['salary']['from'])
    except: 
        salaryfr.append('0')
    try: 
        salaryto.append(mydict[i]['salary']['to'])
    except: 
        salaryto.append('0')
    try: 
        salarycur.append(mydict[i]['salary']['currency'])
    except: 
        salarycur.append('0')
    area.append(mydict[i]['area']['name'])
    publish.append(mydict[i]['published_at'])
    employer.append(mydict[i]['employer']['name'])
    prole.append(mydict[i]['professional_roles'][0]['name'])
    exp.append(mydict[i]['experience']['name'])

#собираем датафрейм, транспонируя списки с данными из hh api. Задаем имена столбцов
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
df = pd.DataFrame(data).transpose()
df.columns = ['вакансия', 'зарплата от', 'зарплата до', 'Валюта', 'Локация', 'Опубликовано', 'Работодатель', 'Роль', 'Опыт']
df

#дропаем строки с пустой зарплатой, заполняем зп, если указана одна сторона вилки, приводим в порядок дату, делаем нормальный индекс 
#добавляем среднюю зп
df['зарплата от'].fillna('0', inplace=True)
df = df.drop(df[df['зарплата от'] == '0'].index)
df['зарплата до'].fillna(df['зарплата от'], inplace=True)
df['Опубликовано']=pd.to_datetime(df['Опубликовано']).dt.date
df.reset_index(drop=True, inplace=True)
df['средняя'] = (df['зарплата от']+df['зарплата до'])/2

#сохраняем файл
df.to_csv('csv/clean_vac.csv', sep='\t', encoding='utf-8')

import seaborn as sns
import matplotlib.pyplot as plt

plt.barh(df['Роль'], df['средняя'])