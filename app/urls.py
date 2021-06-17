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
    path('all_bales/<str:lotID>',views.all_bales,name='all_bales'),
    path('searchbalesdata',views.searchbalesdata,name='searchbalesdata'),
    path('auction_my_bales',views.auction_my_bales,name='auction_my_bales'),
    path('available_for_sale',views.available_for_sale,name='available_for_sale'),
    path('seeks_bids_to_supply',views.seeks_bids_to_supply,name='seeks_bids_to_supply'),
    path('live_auction',views.live_auction,name='live_auction'),
    
]