#открыть файл из директории
import pandas as pd

with open('jsons/vacancies.json', encoding='utf-8') as inputfile:
    myfile = pd.read_json(inputfile)

#из json забираем словарь, в котором находятся информативные поля
mydict = []
for i in range(len(myfile['items'])):
    mydict.append(myfile['items'][i])
    print (mydict)

#далее идут блоки, где мы из словаря формируем столбцы датафрейма

name = []
for i in range(len(mydict)):
    name.append(mydict[i]['name'])
print(name)

salaryfr = []
for i in range(len(mydict)):
    try: 
        salaryfr.append(mydict[i]['salary']['from'])
    except: 
        salaryfr.append('0')
print(salaryfr)

salaryto = []
for i in range(len(mydict)):
    try: 
        salaryto.append(mydict[i]['salary']['to'])
    except: 
        salaryto.append('0')
print(salaryto)

salarycur = []
for i in range(len(mydict)):
    try: 
        salarycur.append(mydict[i]['salary']['currency'])
    except: 
        salarycur.append('0')
print(salarycur)

area = []
for i in range(len(mydict)):
        area.append(mydict[i]['area']['name'])
print(area)

publish = []
for i in range(len(mydict)):
        publish.append(mydict[i]['published_at'])
print(publish)

employer = []
for i in range(len(mydict)):
        employer.append(mydict[i]['employer']['name'])
print(employer)

prole = []
for i in range(len(mydict)):
        prole.append(mydict[i]['professional_roles'][0]['name'])
print(prole)

exp = []
for i in range(len(mydict)):
        exp.append(mydict[i]['experience']['name'])
print(exp)

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