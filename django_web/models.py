from django.db import models
from datetime import datetime


# Create your models here.
class Douban(models.Model):
    # id = models.AutoField(primary_key=True) #主键可省略不写
    mv_rank = models.IntegerField()
    mv_name = models.CharField(max_length=32)
    mv_star = models.CharField(max_length=32)
    mv_quote = models.CharField(max_length=321)
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "movie"  # 指定表名（mysql中显示的表名）


class Weather(models.Model):
    date = models.CharField(max_length=32)
    max_temperature = models.CharField(max_length=32)
    min_temperature = models.CharField(max_length=32)
    wea_condition = models.CharField(max_length=32)
    wea_quality = models.CharField(max_length=32)
    wind = models.CharField(max_length=32)
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "weather"  # 指定表名（mysql中显示的表名）


class Novel(models.Model):
    nv_type = models.CharField(max_length=32)
    nv_name = models.CharField(max_length=32)
    nv_author = models.CharField(max_length=32)
    nv_new_chapter = models.CharField(max_length=32)
    nv_recommend = models.CharField(max_length=32)
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "novel"  # 指定表名（mysql中显示的表名）
