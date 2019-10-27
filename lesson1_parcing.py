#1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com/users/octokit/repos?per_page=100'

repo = []
data = requests.get(url)
j_data = data.json()

for i in j_data:
    repo.append(i['name'])

with open(r'C:\Users\alber\PycharmProjects\GB_Basics\repo_octokit.json','w') as j_file:
    j_file.write(json.dumps(repo))

#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Выбрал сервис Яндекс.Погода
X_Yandex_API_Key = '3b05964a-f02f-4ab0-a476-973b12e767d2'

url = 'https://api.weather.yandex.ru/v1/forecast?'
response = requests.get(
    url,
    params = {'lat': '55.751244', 'lon': '37.618423'},
    headers = {'X-Yandex-API-Key': f'{X_Yandex_API_Key}'}
)

json_response = response.json()

with open(r'C:\Users\alber\PycharmProjects\GB_Basics\yandex_weather.json','w') as j_file:
    j_file.write(json.dumps(json_response))