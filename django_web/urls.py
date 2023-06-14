from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("present_movie", views.present_movie, name='present_movie'),
    path("present_novel", views.present_novel, name='present_novel'),
    path("present_weather", views.present_weather, name='present_weather'),
    path("final_page", views.final_page, name='final_page'),
    path('statis_mv', views.statis_mv, name='statis_mv'),
    path('statis_nv', views.statis_nv, name='statis_nv'),
    path('statis_t', views.statis_t, name='statis_t'),

    # #配置users信息操作信息，name表示对应url的别名
    # path("upload", views.upload,name='upload'),
    # path("doupload", views.DoUpload,name='doupload'),
    # path("users", views.indexUsers,name='indexusers'),
    # path("users/add", views.addUsers,name='addusers'),
    # path("users/insert", views.insertUsers,name='insertusers'),
    # path("users/del/<int:uid>", views.delUsers,name='delusers'),
    # path("users/edit/<int:uid>", views.editUsers,name='editusers'),
    # path("users/update", views.updateUsers,name='updateusers'),
    # path("pageusers/<int:pindex>", views.pageUsers,name='pageusers'),
    # path("ueditor", views.myueditor,name='myueditor'),

]
