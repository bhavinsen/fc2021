from . import add_data_functions
from re import M
import re
from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, context
from django.contrib import messages
import io
import codecs
import csv,json
from django.template import loader
from django.template.loader import get_template
from django.db.models import Q, query
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django import template
from .models import TestBale, Bale
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers import serialize
from django.db.models import Avg, Max, Min, Sum
from .serializers import BalesSerializer






def view_my_bales_data(request):
    User = get_user_model()
    users = User.objects.all()
    data = TestBale.objects.all()
    query = request.user
    if request.user.is_superuser:
        bales = Bale.objects.all()
    else:
       bales = Bale.objects.filter(Q(user__exact=query))

    new_data = []
    unique_station = []
    for j,i in enumerate(bales):
        bales_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter().count()
        if i.Lot_ID in unique_station:
            continue
        else:
            unique_station.append(i.Lot_ID)
            new_data.append({
                'Station': i.Station,
                'variety': i.variety,
                'bales_count': bales_count,
                'Lot_ID':i.Lot_ID,
                'Micronaire': i.Micronaire,
                'Staple_length': i.Staple_length,
                'Rd':i.Rd,
                'Available_For_Sale':i.Available_For_Sale,
                'Spot_Price': i.Spot_Price,
                'weightinkg': i.weightinkg,
                'Organic': i.Organic,
                'BCI': i.BCI,
                'GTex': i.GTex,
                'user': i.user
            })
    return new_data
        