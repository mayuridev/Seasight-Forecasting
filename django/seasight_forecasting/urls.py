# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('past/', views.past, name='past'),
    path('stop_thread/', views.stop_thread, name='stop_thread'),
    path('present/', views.present, name='present'),
    path('future/', views.future, name='future'),
    path('demo/', views.demo, name='demo'),
    path('clean_KML/', views.clean_KML, name='clean_KML'),
    path('clean_ALL/', views.clean_ALL, name='clean_ALL'),
]