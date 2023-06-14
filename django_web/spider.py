import requests
from bs4 import BeautifulSoup
import threading
import MySQLdb
from datetime import datetime

# 数据库连接信息
host = 'localhost'
user = 'root'
password = '111111'  # 请替换为您的密码
db = 'softwareproject'
port = 3306
# 建立数据库连接
conn = MySQLdb.connect(
    host=host,
    user=user,
    password=password,
    db=db
    # port=port,
    # charset='utf8mb4',
    # cursorclass=MySQLdb.cursors.DictCursor
)


# 获取电影列表
def get_movie_list(start):
    url = 'https://movie.douban.com/top250?start=' + str(start)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
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

        movie_id = movie.find("div", class_="pic").find("em").get_text()
        movie_name = movie.find('div', class_='hd').find('a').find('span', class_='title').get_text()
        movie_star = movie.find('span', class_='rating_num').get_text()
        movie_addtime = datetime.now()
        # movie_quote = movie.find('div', class_='bd').find('span', class_='inq').get_text()
        try:
            # 写入数据库
            with conn.cursor() as cursor:
                sql = "insert into django_web_douban (id,mv_rank, mv_name, mv_star,addtime) VALUES (%s, %s, %s)"
                cursor.execute(sql, (movie_id, movie_name, movie_star,movie_addtime))
                cursor.close()
            conn.commit()
        except Exception as e:
            print(e)


# 多线程抓取
# threads1 = []
# for i in range(0, 250, 25):
#     t = threading.Thread(target=get_movie_list, args=(i,))
#     threads1.append(t)
# for t in threads1:
#     t.start()
# for t in threads1:
#     t.join()
# 关闭数据库连接
conn.close()
# threads_mv = []
# threads_nv = []
# for i, j in zip(range(0, 250, 25), range(1, 11)):
#     m = threading.Thread(target=get_movie, args=(i,))
#     n = threading.Thread(target=get_novel, args=(j,))
#     threads_mv.append(m)
#     threads_nv.append(n)
#
# for m, n in zip(threads_mv, threads_nv):
#     m.start()
#     n.start()
#
# for m, n in zip(threads_mv, threads_nv):
#     m.join()
#     n.join()
