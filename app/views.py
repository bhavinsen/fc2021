
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
# @login_required(login_url="/login/")
# def index(request):
#     context = {}
#     context['segment'] = 'dashboard'

#     html_template = loader.get_template( 'dashboard.html' )
#     return HttpResponse(html_template.render(context, request))

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
    
    context = {
    'users':users,
    'bales':bales,
    'lots':lots,
    'Station':Station,
    'test':test,
    }
    return render(request,"dashboard.html",context)


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
    rbales = Bale.objects.filter(Q(user__exact=query))
    bales = Bale.objects.all()
    newdata = []
    # if request.method == 'POST':
    #     arr = json.loads(request.body)
    #     newlist = arr['arr']
    #     for i in newlist:
            
    #         multi = Bale.objects.filter(Q(user__username__exact=str(i)))
    #         print("multi",multi)
    #     if len(multi) > 0:
    #         new = serialize('json', multi)
    #         newdata.append(new)
    #     else:
    #         print("*************** ")
    #     print(newdata)
    #     return JsonResponse(newdata,safe=False)
    return render(request,'viewmybales.html',{'data':data,'users':users,'bales':bales,'rbales':rbales})

@login_required(login_url="/login/")
@csrf_exempt
def available_for_sale(request):
    
    data= json.loads(request.body)
    print("🚀 ~ file: views.py ~ line 130 ~ data", data['id'][-3:])
    sale_id = data['id'][-3:]
    sale_value =  data['value']
    bales = Bale.objects.get(id=sale_id)
    if sale_value == "True":
        bales.Available_For_Sale = False
    else:
        bales.Available_For_Sale = True
    bales.save()
    print("🚀 ~ file: views.py ~ line 134 ~ bales", bales.Available_For_Sale)
    return JsonResponse({"msg": "success"},safe=False)

@login_required(login_url="/login/")
def addbales(request):
    data = TestBale.objects.all()
    User = get_user_model()
    users = User.objects.all()
    if request.method == "POST":
        csv_file = request.FILES['formFile']
        task = request.POST.get('country')
        print("🚀 ~ file: views.py ~ line 136 ~ task", task)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        common_header =  ['\ufeffginnerid', 'baleid', 'lotid', 'variety', 'station ', 'crop year', 'staple ', 'micronaire', 'Rd', ' Gtex', 'spot_price', 'weightinkg', 'for_sale', 'organic', 'BCI']
        # common_header = ['ginnerid,baleid,lotid,variety,station,crop year,staple,micronaire,Rd,Gtex,spot_price,weightinkg,for_sale,organic,BCI\r\n']
        # for index,row in enumerate(csv_file):
        #     data = row.decode('utf-8')
        #     if data:
        #         line = data.split('","')
        #         # print("🚀 ~ file: views.py ~ line 125 ~ line", line)
        #     if index == 0:
        #         if (line != common_header):
        #             messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
        #         else:
        #             messages.success(request, 'THIS IS SAME HEADER CSV FILE')
        # data_set = csv_file.read().decode('UTF-8')
        # io_string = io.StringIO(data_set)
        # next(io_string)
        # for column in csv.reader(data_set, delimiter=',', quotechar="|"):
                    # print("🚀 ~ file: views.py ~ line 152 ~ column",  row[0],row[1])
            # _, created = Bale.objects.update_or_create(
            #     ginnerid = column[0],
            #     Bale_ID=column[1],
            #     Lot_ID=column[2],
            #     variety = column[3],
            #     Station=column[4],
            #     Crop_Year=column[5],
            #     Staple_length=column[6],
            #     Micronaire=column[7],
            #     Rd= column[8],
            #     GTex= column[9],
            #     Spot_Price=column[10],
            #     weightinkg= column[11],
            #     Available_For_Sale= column[12],
            #     Organic=column[13],
            #     BCI=column[14],
            #     user = User.objects.get(id=request.user.id)
            # )
        reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
        for j,column in enumerate(reader):
            if j == 0:
                print("🚀 ~ file: views.py ~ line 441 ~ i", column)
                # print("🚀 ~ file: views.py ~ line 430 ~ common_header != i", common_header != i)
                if common_header != column:
                    messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
                    break
                else:
                    messages.success(request, 'THIS IS SAME HEADER CSV FILE')
            if j != 0:
                
                # print("🚀 ~ file: views.py ~ line 186 ~ column", column[0],column[1])

                print("🚀 ~ file: views.py ~ line 441 ~ i")
                For_Sale = column[12]
                org = column[13]
                bci = column[14]
                if For_Sale == "TRUE":
                    sale = True
                else:
                    sale = False
                if org == "TRUE":
                    org_up = True
                else:
                    org_up = False
                if bci == "TRUE":
                    bci_up = True
                else:
                    bci_up = False
                created = Bale(
                    ginnerid = column[0],
                    Bale_ID=column[1],
                    Lot_ID=column[2],
                    variety = column[3],
                    Station=column[4],
                    Crop_Year=column[5],
                    Staple_length=column[6],
                    Micronaire=column[7],
                    Rd= column[8],
                    GTex= column[9],
                    Spot_Price=column[10],
                    weightinkg= column[11],
                    Available_For_Sale= sale,
                    Organic=org_up,
                    BCI=bci_up,
                    user = User.objects.get(id=request.user.id)
                )
                created.save()
              
        return render(request,'addbales.html',{"users":users})
    return render(request,'addbales.html',{"users":users})

# from .models import Bale
# Create your views here.
@login_required(login_url="/login/")
def addtestdata(request):
    data = TestBale.objects.all()
    if request.method == "POST":
        # csv_file = request.FILES['formFile']
        # if not csv_file.name.endswith('.csv'):
        #     messages.error(request, 'THIS IS NOT A CSV FILE')
        # data_set = csv_file.read().decode('UTF-8')
        # io_string = io.StringIO(data_set)
        # next(io_string)
        # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #     _, created = TestBale.objects.update_or_create(
        #         Bale_ID=column[0],
        #         Staple_length=column[1],
        #         Trash=column[2],
        #         Bundle_Strength=column[3],
        #         Micronaire=column[4],
        #         Rd=column[5],
        #         b=column[6],
        #     )
        csv_file = request.FILES['formFile']
        common_header = ['Bale ID,Staple length,Trash,Bundle Strength,Micronaire,Rd,+b,test by fc,test_report\r\n']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        for index,row in enumerate(csv_file):
            data = row.decode('utf-8')
            if data:
                line = data.split('","')
                print("🚀 ~ file: views.py ~ line 180 ~ line", line)
            if index == 0:
                if (line != common_header):
                    messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
                else:
                    messages.success(request, 'THIS IS SAME HEADER CSV FILE')
        return render(request,'addtestdata.html',{'data':data})
    return render(request,'addtestdata.html')

@login_required(login_url="/login/")
@csrf_exempt
def searchbales(request):
    # request.body
    if request.method == 'POST' and request.is_ajax:
        print("🚀 ~ file: views.py ~ line 191 ~ request.body", json.loads(request.body)['Station'])
    
        data= json.loads(request.body)
        # bales = Bale.objects.all()
        bales = Bale.objects.filter(Q(Station__exact=json.loads(request.body)['Station']))
        # print(bales)
        new_data = []
        for j,i in enumerate(bales):
            new_data.append({
                'Station':i.Station,
                'Bale_ID':i.Bale_ID,
                'Available_For_Sale':i.Available_For_Sale,
                'BCI':i.BCI,
                'Rd':"",
                'Organic':i.Organic,
                'Staple_length':"",
                'Micronaire':"",
            })
            # new_data['Station']=i.Station
            # new_data['Bale_ID']=i.Bale_ID
            # new_data['Available_For_Sale']=i.Available_For_Sale
            # new_data['BCI']=i.BCI
            # print(i.BCI)
        # print("🚀 ~ file: views.py ~ line 199 ~ bales", bales)
        # data = serialize("json", bales)
            max_staple = Bale.objects.filter(Q(Station__exact=data["Station"])).aggregate(Max('Staple_length'))['Staple_length__max']
            print("🚀 ~ file: views.py ~ line 204 ~ max_staple", max_staple)
            
            min_staple = Bale.objects.filter(Q(Station__exact=data["Station"])).aggregate(Min('Staple_length'))['Staple_length__min']
            print("🚀 ~ file: views.py ~ line 207 ~ min_staple", min_staple)
            
            max_micronaire = Bale.objects.filter(Q(Station__exact=data["Station"])).aggregate(Max('Micronaire'))['Micronaire__max']
            print("🚀 ~ file: views.py ~ line 210 ~ max_micronaire", max_micronaire)
            
            min_micronaire = Bale.objects.filter(Q(Station__exact=data["Station"])).aggregate(Min('Micronaire'))['Micronaire__min']
            print("🚀 ~ file: views.py ~ line 213 ~ min_micronaire", min_micronaire)
            # data = [
            #     {'station':new_data,'max_staple':max_staple+ "-" + min_staple,'max_micronaire':max_micronaire +"-"+min_micronaire}
            # ] 
            max_rd = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Max('Rd'))['Rd__max']
            print("🚀 ~ file: views.py ~ line 204 ~ max_rd", max_rd)
            max_gtex = Bale.objects.filter(Station=i.Station).aggregate(Max('GTex'))['GTex__max']
            min_gtex = Bale.objects.filter(Station=i.Station).aggregate(Min('GTex'))['GTex__min']
            min_rd = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Min('Rd'))['Rd__min']
            print("🚀 ~ file: views.py ~ line 207 ~ min_Rd", Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Min('Rd'))['Rd__min'])
            new_data[j]['Staple_length'] = max_staple+ "-" + min_staple
            new_data[j]['Micronaire'] = max_micronaire +"-"+min_micronaire
            new_data[j]['Rd'] = max_rd + "-" + min_rd
            new_data[j]['Gtex'] =  min_gtex +"-"+ max_gtex
            # new_data.append({'max_staple':max_staple+ "-" + min_staple,'max_micronaire':max_micronaire +"-"+min_micronaire})
            print("🚀 ~ file: views.py ~ line 203 ~ new_data", new_data)
        # return render(request,"searchbales.html",new_data)
        return HttpResponse(
            json.dumps(new_data),
            content_type="application/json"
        )
    # bales = Bale.objects.all()
    # if request.method == 'GET':
    #     query= request.GET.get('q')
    #     submitbutton= request.GET.get('submit')
    #     if query is not None:
    #         lookups= Q(Bale_ID__icontains=query) | Q(Lot_ID__icontains=query) | Q(Station__icontains=query) | Q(Crop_Year__icontains=query) | Q(Pick__icontains=query) | Q(Staple_Type__icontains=query) | Q(Staple_length__icontains=query) | Q(Trash__icontains=query) | Q(Bundle_Strength__icontains=query) | Q(Micronaire__icontains=query) | Q(Moisture__icontains=query) | Q(Asking_Price__icontains=query)
    #         results= Bale.objects.filter(lookups).distinct()
    #         context={'results': results,
    #                  'submitbutton': submitbutton}
    #         return render(request, 'searchbales.html', context)
    return render(request,"searchbales.html")

@login_required(login_url="/login/")
@csrf_exempt
def searchbalesdata(request):
    # request.body
    bales = Bale.objects.all()
    # print(bales)
    new_data = []
    unique_station = {}
    for j,i in enumerate(bales):
        
        total_bales = Bale.objects.filter(Q(Station__exact=i.Station)).count()
        max_staple = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Max('Staple_length'))['Staple_length__max']
        
        min_staple = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Min('Staple_length'))['Staple_length__min']
        
        
        max_rd = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Max('Rd'))['Rd__max']
        
        min_rd = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Min('Rd'))['Rd__min']
        
        
        max_micronaire = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Max('Micronaire'))['Micronaire__max']
        
        min_micronaire = Bale.objects.filter(Q(Station__exact=i.Station)).aggregate(Min('Micronaire'))['Micronaire__min']
        total_org = Bale.objects.filter(Q(Station__exact=i.Station)).filter(Organic=True).count()
        total_bci = Bale.objects.filter(Q(Station__exact=i.Station)).filter(BCI=True).count()
        total_sale = Bale.objects.filter(Q(Station__exact=i.Station)).filter(Available_For_Sale=True).count()
        max_gtex = Bale.objects.filter(Station=i.Station).aggregate(Max('GTex'))['GTex__max']
        min_gtex = Bale.objects.filter(Station=i.Station).aggregate(Min('GTex'))['GTex__min']
        Staple_length = min_staple+ "-" +  max_staple
        Micronaire =  min_micronaire +"-"+ max_micronaire
        Rd =min_rd + "-" +  max_rd 
        Gtex =  min_gtex +"-"+ max_gtex
        if i.Lot_ID in unique_station:
            continue
        else:
            unique_station[i.Lot_ID] = True
            new_data.append({
                    'Lot_ID':i.Lot_ID,
                    'Station':i.Station,
                    'variety':i.variety,
                    'Bale_ID':total_bales,
                    'weightinkg':i.weightinkg,
                    'Staple_length':Staple_length,
                    'Micronaire':Micronaire,
                    'Rd':Rd,
                    'GTex':Gtex,
                    'Available_For_Sale':total_sale,
                    'BCI':total_bci,
                    'Organic': total_org,
            })
    # new_data.append({'max_staple':max_staple+ "-" + min_staple,'max_micronaire':max_micronaire +"-"+min_micronaire})
    print("🚀 ~ file: views.py ~ line 203 ~ new_data", new_data)
    return HttpResponse(
        json.dumps(new_data),
        content_type="application/json"
    )




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
    rbales = Bale.objects.filter(Q(user__exact=query))
    bales = Bale.objects.all()
    return render(request,'auction_my_bales.html',{'users':users,'bales':bales,'rbales':rbales})

@login_required(login_url="/login/")
@csrf_exempt
def seeks_bids_to_supply(request):
    return render(request,'seeks_bids_to_supply.html')


@login_required(login_url="/login/")
@csrf_exempt
def live_auction(request):
    return render(request,'live_auction.html')

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
    return JsonResponse(data1.data,safe=False)



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