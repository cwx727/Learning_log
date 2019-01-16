from django.urls import path,include,re_path
from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('topics/', views.topics,name='topics'),
    re_path('topics/(\d+)', views.topic,name='topic'),
    path('new_topic/', views.new_topic,name='new_topic'),
    re_path('new_entry/(\d+)', views.new_entry, name='new_entry'),
    re_path('edit_entry/(\d+)', views.edit_entry, name='edit_entry'),

]

'''
from django.conf.urls import url
from . import views
from django.urls import path,include

urlpatterns = [
# 主页
	path('', views.index),
]
'''
