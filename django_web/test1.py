import requests
from bs4 import BeautifulSoup



url = 'https://tianqi.2345.com/Pc/GetHistory'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}
# 发送请求
params = {
    'areaInfo[areaId]': 71464,
    'areaInfo[areaType]': 2,
    'date[year]': 2023,
    'date[month]': 5
}

response = requests.get(url=url, headers=headers, params=params)
if response.status_code != 200:
    raise Exception("err")

response.encoding = 'gbk'
html_data = response.json()['data']
# print(weather_data)
soup = BeautifulSoup(html_data, 'html.parser')
dates_weather = soup.find('table', class_='history-table').find_all('tr')[1:]
for day in dates_weather:
    date = day.find_all('td')[0].get_text()
    max_temperature = day.find_all('td')[1].get_text()
    min_temperature = day.find_all('td')[2].get_text()
    wea_condition = day.find_all('td')[3].get_text()
    wind = day.find_all('td')[4].get_text()
    wea_quality = day.find_all('td')[5].get_text()
    print(date, wea_condition)
