import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from .mytools import *
import warnings

warnings.filterwarnings("ignore")


# Create your views here.

# 首页
def index(request):
    # test()
    # clear_all_db()
    context = {

    }
    return render(request, 'index.html', context)


# 爬取电影数据并进行展示
def present_movie(request):
    # 在访问前清空movie数据库里的数据
    clear_db(mv_flag=1)
    # 重新爬取电影数据，实现实时更新
    multiprocessing_crawl(mv_flag=1)
    mv_list = Douban.objects.all()
    context = {
        "mv_list": mv_list
    }
    return render(request, 'movie.html', context)


# 爬取小说数据并进行展示
def present_novel(request):
    # 在访问前清空novel数据库里的数据
    clear_db(nv_flag=1)
    # 重新爬取小说数据，实现实时更新
    multiprocessing_crawl(nv_flag=1)
    nv_list = Novel.objects.all()
    context = {
        "nv_list": nv_list
    }
    return render(request, 'novel.html', context)


# @csrf_exempt是token令牌
@csrf_exempt
def statis_nv(request):
    category, category_num = statis_novels()
    nv_data = []
    for type, num in zip(category, category_num):
        nv_dic = {'value': num, 'name': type}
        nv_data.append(nv_dic)
    return HttpResponse(json.dumps(nv_data), content_type='application/json')


@csrf_exempt
def statis_mv(request):
    score_list, score_num = statis_movies()
    mv_data = []
    for score, num in zip(score_list, score_num):
        mv_dic = {'value': num, 'name': score}
        mv_data.append(mv_dic)
    return HttpResponse(json.dumps(mv_data), content_type='application/json')


@csrf_exempt
def statis_t(request):
    date_list, temperature_list = statis_temperature()
    # print(temperature_list)
    t_data = {
        0: date_list,
        1: temperature_list
    }
    # print(t_data)
    return HttpResponse(json.dumps(t_data, cls=NpEncoder), content_type='application/json')


# 爬取天气数据并进行展示
def present_weather(request):
    # 在访问前清空weather数据库里的数据
    clear_db(wea_flag=1)
    # 重新爬取天气数据，实现实时更新
    get_weather()
    wea_data = Weather.objects.all()
    context = {
        "wea_data": wea_data
    }
    return render(request, 'weather.html', context)


# 尾页展示
def final_page(request):
    context = {

    }
    return render(request, 'end_page.html', context)


def test():
    ob = Douban()
    ob.mv_name = "西欧昂红"
    ob.mv_rank = "1"
    ob.mv_star = "9.6"
    ob.save()


def clear_all_db():
    clear_db(mv_flag=1, nv_flag=1, wea_flag=1)
    return


if __name__ == '__main__':
    pass
