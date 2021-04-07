# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # The home page
    path('', views.dashboard, name='home'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('settings',views.settings,name='settings'),
    path('addtestdata',views.addtestdata,name='addtestdata'),
    path('viewmybales',views.viewmybales,name='viewmybales'),
    path('addbales',views.addbales,name='addbales'),
    path('searchbales',views.searchbales,name='searchbales'),
    
]
