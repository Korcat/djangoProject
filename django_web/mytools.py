import requests
from bs4 import BeautifulSoup
import threading
import MySQLdb as mysql
from .models import Douban, Novel, Weather
import numpy as np
import json


# 根据指令，清除对应数据库里的数据
def clear_db(mv_flag=0, nv_flag=0, wea_flag=0):
    '''

    :param mv_flag: movie数据库清空标志
    :param nv_flag: novel数据库清空标志
    :param wea_flag: weather数据库清空标志
    :return:
    '''
    # 连接数据库
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="111111",
        database="softwareproject"
    )
    # print(db)
    cursor = db.cursor()
    # defining all the Query
    # 电影数据库
    if mv_flag:
        cursor.execute("truncate table movie")
    if nv_flag:
        cursor.execute("truncate table novel")
    if wea_flag:
        cursor.execute("truncate table weather")

    # query1 = "truncate table movie"
    # # 小说数据库
    # query2 = "truncate table novel"
    # # 天气数据库
    # query3 = "truncate table weather"
    # # executing all the query
    # cursor.execute(query1)
    # cursor.execute(query2)
    # cursor.execute(query3)

    # 确认更改完毕
    db.commit()
    db.close()


# 多线程爬取数据
def multiprocessing_crawl(mv_flag=0, nv_flag=0):
    if mv_flag:
        threads = []
        for i in range(0, 250, 25):
            t = threading.Thread(target=get_movie, args=(i,))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return
    if nv_flag:
        threads = []
        for i in range(1, 11):
            t = threading.Thread(target=get_novel, args=(i,))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return


# 爬取豆瓣电影top250
def get_movie(start):
    url = 'https://movie.douban.com/top250?start=' + str(start)
    print(start)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}
    # 发送请求
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("err")
    response.encoding = 'utf-8'
    # 解析页面
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = (soup.find("div", id="content").
              find("div", class_="article").
              find("ol", class_="grid_view").
              find_all("div", class_="item"))
    for movie in movies:
        ob = Douban()
        ob.mv_rank = movie.find("div", class_="pic").find("em").get_text()
        ob.mv_name = movie.find('div', class_='hd').find('a').find('span', class_='title').get_text()
        ob.mv_star = movie.find('span', class_='rating_num').get_text()
        quote_temp = movie.find('div', class_='bd').find('span', class_='inq')
        if quote_temp:
            ob.mv_quote = quote_temp.get_text()
        else:
            ob.mv_quote = "暂无数据"
        ob.save()


# 爬取笔趣阁小说总排行前10页
def get_novel(page):
    url = f'https://www.bbiquge.net/top/allvisit/{page}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}
    # 发送请求
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("err")
    response.encoding = 'GB2312'  # 一定要进行编码格式转化，否则是乱码（编码形式可以在网页上捕获到）
    soup = BeautifulSoup(response.text, 'html.parser')
    novel_list = soup.find('div', id='articlelist').find_all('li')[1:]
    for novel in novel_list:
        ob = Novel()
        ob.nv_type = novel.find('span', class_='l1').get_text()
        ob.nv_name = novel.find('span', class_='l2').find('a').get_text()
        ob.nv_author = novel.find('span', class_='l3').get_text()
        ob.nv_new_chapter = novel.find('span', class_='l4').find('a').get_text()
        ob.nv_recommend = novel.find('span', class_='l6').get_text()
        ob.save()


# 爬取重庆市南岸区2023年每天的所有天气（实时更新）
def get_weather():
    year = 2023
    area_id = 71464
    area_type = 2
    # month = m
    month_list = [1, 2, 3, 4, 5, 6]
    # url
    url = 'https://tianqi.2345.com/Pc/GetHistory'
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}

    for month in month_list:
        # 请求参数
        params = {
            'areaInfo[areaId]': area_id,
            'areaInfo[areaType]': area_type,
            'date[year]': year,
            'date[month]': month
        }
        # 发送请求
        response = requests.get(url=url, headers=headers, params=params)
        # 判断是否请求成功
        if response.status_code != 200:
            raise Exception("err")
        response.encoding = 'gbk'  # 求数据数据格式为‘gbk’
        html_data = response.json()['data']  # 得到返回的html代码
        # 利用bs4对html进行解析
        soup = BeautifulSoup(html_data, 'html.parser')
        dates_weather = soup.find('table', class_='history-table').find_all('tr')[1:]
        for day in dates_weather:
            ob = Weather()
            ob.date = day.find_all('td')[0].get_text()
            ob.max_temperature = day.find_all('td')[1].get_text()
            ob.min_temperature = day.find_all('td')[2].get_text()
            ob.wea_condition = day.find_all('td')[3].get_text()
            ob.wind = day.find_all('td')[4].get_text()
            ob.wea_quality = day.find_all('td')[5].get_text()
            ob.save()


# 统计各个类别小说的个数
def statis_novels():
    category = ['玄幻小说', '修真小说', '都市小说', '历史小说', '网游小说', '科幻小说']
    category_num = [0, 0, 0, 0, 0, 0]
    nv_list = Novel.objects.all()
    for nv in nv_list:
        if nv.nv_type == category[0]:
            category_num[0] += 1
            continue
        if nv.nv_type == category[1]:
            category_num[1] += 1
            continue
        if nv.nv_type == category[2]:
            category_num[2] += 1
            continue
        if nv.nv_type == category[3]:
            category_num[3] += 1
            continue
        if nv.nv_type == category[4]:
            category_num[4] += 1
            continue
        if nv.nv_type == category[5]:
            category_num[5] += 1
            continue
    return category, category_num


# 统计电影各个评分段的个数
def statis_movies():
    score_list = ['9.7', '9.6', '9.5', '9.4', '9.3', '9.2', '9.1', '9.0', '8.9', '8.8', '8.7', '8.6', '8.5', '8.4']
    score_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mv_list = Douban.objects.all()
    for mv in mv_list:
        if mv.mv_star == score_list[0]:
            score_num[0] += 1
            continue
        if mv.mv_star == score_list[1]:
            score_num[1] += 1
            continue
        if mv.mv_star == score_list[2]:
            score_num[2] += 1
            continue
        if mv.mv_star == score_list[3]:
            score_num[3] += 1
            continue
        if mv.mv_star == score_list[4]:
            score_num[4] += 1
            continue
        if mv.mv_star == score_list[5]:
            score_num[5] += 1
            continue
        if mv.mv_star == score_list[6]:
            score_num[6] += 1
            continue
        if mv.mv_star == score_list[7]:
            score_num[7] += 1
            continue
        if mv.mv_star == score_list[8]:
            score_num[8] += 1
            continue
        if mv.mv_star == score_list[9]:
            score_num[9] += 1
            continue
        if mv.mv_star == score_list[10]:
            score_num[10] += 1
            continue
        if mv.mv_star == score_list[11]:
            score_num[11] += 1
            continue
        if mv.mv_star == score_list[12]:
            score_num[12] += 1
            continue
        if mv.mv_star == score_list[13]:
            score_num[13] += 1
            continue
    return score_list, score_num


# 统计2023年每天的平均温度
def statis_temperature():
    data = Weather.objects.all()
    n = 0
    for i in data:
        n += 1  # 统计天数
    temperature_list = []
    date_list = []
    for j, day in enumerate(data):
        max_t = get_temperature(day.max_temperature)
        min_t = get_temperature(day.min_temperature)
        temperature_list.append((max_t + min_t) / 2)
        date_list.append(day.date)
    return date_list, temperature_list


# 从字符串温度里获取数字温度
def get_temperature(t):
    i = 0
    local_num = []
    while t[i] != "°":
        local_num.append(float(t[i]))
        i += 1
    # local_num中最多有两位数字，如果只有一位，该数字就是个位的数字；如果有两位，第一位为十位，第二位为个位
    t_len = len(local_num)
    if t_len == 1:  # 只有一位
        t_new = local_num[0]
    else:  # 有两位
        t_new = local_num[0] * 10 + local_num[1]
    return t_new


# 防止数据容器不能变为json格式
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
