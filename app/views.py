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

from . import lots_views_functions
from . import view_my_bales

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dashboard(request):
    User = get_user_model()
    users = len(User.objects.all())
    bales = len(Bale.objects.all())
    lots = len(Bale.objects.values_list('Lot_ID', flat=True).distinct())
    Station = len(Bale.objects.values_list('Station', flat=True).distinct())
    test = len(TestBale.objects.all())

    from . import inventory_functions
    new_data = inventory_functions.get_inventory_data()
    
    context = {
    'users':users,
    'bales':bales,
    'lots':lots,
    'Station':Station,
    'test':test,
    }
    #return render(request,"dashboard.html",context)
    return render (request,"dashboard.html",{"context":context, "list_data": new_data})

@login_required(login_url="/login/")
def settings(request):
    return render(request,'settings.html')


@login_required(login_url="/login/")
@csrf_exempt
def viewmybales(request):
    User = get_user_model()
    users = User.objects.all()
    data = TestBale.objects.all()
    query = request.user
    new_data = view_my_bales.view_my_bales_data(request)
    return render(request,'viewmybales.html',{'data':data,'users':users,'bales':new_data,'rbales':new_data})

@login_required(login_url="/login/")
@csrf_exempt
def available_for_sale(request):
    data= json.loads(request.body)
    sale_id = data['id']
    sale_value =  data['value']
    bales = Bale.objects.filter(Lot_ID=sale_id)
    for bale in bales:

        if sale_value == "True":
            bale.Available_For_Sale = False
        else:
            bale.Available_For_Sale = True
        bale.save()
    return JsonResponse({"msg": "success"},safe=False)

@login_required(login_url="/login/")
def addbales(request):
    users = add_data_functions.add_bales_function(request)
    return render(request,'addbales.html',{"users":users})

@login_required(login_url="/login/")
def addtestdata(request):
    data = add_data_functions.add_test_data_function(request)
    return render(request, 'addtestdata.html')

@login_required(login_url="/login/")
@csrf_exempt
def searchbalesdata(request):
    # user = request.user
    bales = Bale.objects.raw("SELECT id, Bale_ID, COUNT(Bale_ID) as count_of_bales, Station, variety, weightinkg, MAX(Staple_length) as max_sl, min(Staple_length) as min_sl, max(Micronaire), min(Micronaire), max(Rd), min(Rd), "
                             "Organic, BCI FROM app_bale GROUP BY Station")
    new_data = []
    for i in bales:
        
        for_sale_count = Bale.objects.filter(Station=i.Station).filter(Available_For_Sale=True).count()

        max_staple = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Staple_length'))[
            'Staple_length__max']
        min_staple = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Staple_length'))[
            'Staple_length__min']

        max_mic = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Micronaire'))[
            'Micronaire__max']
        min_mic = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Micronaire'))[
            'Micronaire__min']

        max_rd = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Rd'))['Rd__max']
        min_rd = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Rd'))['Rd__min']

        max_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Spot_Price'))['Spot_Price__max']
        min_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Spot_Price'))['Spot_Price__min']

        organic_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(Organic=True).count()
        bci_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(BCI=True).count()

        max_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('GTex'))['GTex__max']
        min_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('GTex'))['GTex__min']


        new_data.append({
            'Lot_ID':i.Lot_ID,
            'station': i.Station,
            'variety': i.variety,
            'total_bales': i.count_of_bales,
            'for_sale': for_sale_count,
            'mic_range': str(min_mic) + " - " + str(max_mic),
            'staple_range': str(min_staple) + " - " + str(max_staple),
            'rd_range': str(min_rd) + " - " + str(max_rd),
            'price_range': str(min_price) + " - " + str(max_price),
            'organic_count': str(organic_count),
            'bci_count': str(bci_count),
            'gtex_range': str(min_gtex) + " - " + str(max_gtex),
        })
    print("🚀 ~ file: views.py ~ line 375 ~ new_data", new_data)
    return HttpResponse(
        json.dumps(new_data),
        content_type="application/json"
    )

# @login_required(login_url="/login/")
# @csrf_exempt
# def searchbales(request):
#     bales = Bale.objects.raw("SELECT id, Bale_ID, COUNT(Bale_ID) as count_of_bales, Station, variety, weightinkg, MAX(Staple_length) as max_sl, min(Staple_length) as min_sl, max(Micronaire), min(Micronaire), max(Rd), min(Rd), "
#                              "Organic, BCI FROM app_bale GROUP BY Station, variety")
#     new_data = []
#     for i in bales:

#         for_sale_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(Available_For_Sale=True).count()

#         max_staple = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Staple_length'))[
#             'Staple_length__max']
#         min_staple = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Staple_length'))[
#             'Staple_length__min']

#         max_mic = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Micronaire'))[
#             'Micronaire__max']
#         min_mic = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Micronaire'))[
#             'Micronaire__min']

#         max_rd = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Rd'))['Rd__max']
#         min_rd = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Rd'))['Rd__min']

#         max_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Spot_Price'))['Spot_Price__max']
#         min_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Spot_Price'))['Spot_Price__min']

#         organic_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(Organic=True).count()
#         bci_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(BCI=True).count()

#         max_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('GTex'))['GTex__max']
#         min_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('GTex'))['GTex__min']

#         new_data.append({
#             'station': i.Station,
#             'variety': i.variety,
#             'total_bales': i.count_of_bales,
#             'for_sale': for_sale_count,
#             'mic_range': str(min_mic) + " - " + str(max_mic),
#             'staple_range': str(min_staple) + " - " + str(max_staple),
#             'rd_range': str(min_rd) + " - " + str(max_rd),
#             'price_range': str(min_price) + " - " + str(max_price),
#             'organic_count': str(organic_count),
#             'bci_count': str(bci_count),
#             'gtex_range': str(min_gtex) + " - " + str(max_gtex),
#         })
#     return render(request,"searchbales.html",{"list_data":new_data})



def handler404(request,exception):
    return render(request, '404.html', status=404)
def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request,exception):
    return render(request, '403.html', status=403)

@login_required(login_url="/login/")
@csrf_exempt
def auction_my_bales(request):
    User = get_user_model()
    users = User.objects.all()
    query = request.user
    new_data = view_my_bales.view_my_bales_data(request)
    return render(request,'auction_my_bales.html',{'users':users,'bales':new_data,'rbales':new_data})

@login_required(login_url="/login/")
@csrf_exempt
def seeks_bids_to_supply(request):
    return render(request,'seeks_bids_to_supply.html')


@login_required(login_url="/login/")
@csrf_exempt
def live_auction(request):
    return render(request,'live_auction.html')

@login_required(login_url="/login/")
@csrf_exempt
def all_bales(request,lotID):
    print("🚀 ~ file: views.py ~ line 434 ~ lotID", lotID)
    data = Bale.objects.filter(Lot_ID=lotID)
    print("🚀 ~ file: views.py ~ line 435 ~ data", data)
    # return HttpResponse(
    #     json.dumps(data),
    #     content_type="application/json"
    # )
    data1 = BalesSerializer(data,many=True)
    return render(request,'all_bales.html',{"data":data1.data})
    # return JsonResponse(data1.data,safe=False)



@login_required(login_url="/login/")
@csrf_exempt
def searchform(request):
    if request.method == 'POST':
        data = request.POST
        bales = Bale.objects.filter(Q(Station=data.get("Station","")) | Q(Lot_ID=data.get("Lot_ID","")) | Q(variety=data.get("variety","")) | Q(Bale_ID=data.get("Bale_ID",""))
                                    # | Q(Micronaire=data["Micronaire"]) | Q(Rd=data["Rd"]) | Q(GTex=data["GTex"]) | Q(Spot_Price=data["Spot_Price"])
                                    # | Q(weightinkg__exact=data["weightinkg"]) | Q(Available_For_Sale=data.get("Available_For_Sale",None)) | Q(Organic=data.get("Organic",None))
                                    # | Q(BCI__icontains=data.get("BCI",None)) | Q(Moisture=data["Trash"]) | Q(Pick=data["Pick"]) | Q(Crop_Year=data['Crop_Year'])
                                    )
        ser_data = BalesSerializer(bales,many=True)
        return render(request,'searchform.html',{"data":ser_data.data})
    return render(request,'searchform.html')

@login_required(login_url="/login/")
@csrf_exempt
def viewlots(request, station_txt, variety_txt):
    print (request.GET)
    data_object = lots_views_functions.get_lots_views_data(station_txt, variety_txt)
    return render(request,'lotsview.html',{"list_data":data_object})

@login_required(login_url="/login/")
@csrf_exempt
def viewlotsfromstation(request, station_txt):
    data_object = lots_views_functions.get_lots_views_data_fromstation(station_txt)
    return render(request,'lotsview.html',{"list_data":data_object})

@login_required(login_url="/login/")
@csrf_exempt
def searchbales(request):
    print("dummy function")