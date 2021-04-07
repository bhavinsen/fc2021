
from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, context
from django.contrib import messages
import io
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
def addbales(request):
    data = TestBale.objects.all()
    User = get_user_model()
    users = User.objects.all()
    if request.method == "POST":
        csv_file = request.FILES['formFile']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        common_header = ['Bale ID,Lot ID,Station,Crop Year,Pick,Staple Type,Staple length,Trash,Bundle Strength,Micronaire,Moisture,Asking Price\r\n']
        for index,row in enumerate(csv_file):
            data = row.decode('utf-8')
            if data:
                line = data.split('","')
                print("🚀 ~ file: views.py ~ line 125 ~ line", line)
            if index == 0:
                if (line != common_header):
                    messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
                else:
                    messages.success(request, 'THIS IS SAME HEADER CSV FILE')
        # data_set = csv_file.read().decode('UTF-8')
        # io_string = io.StringIO(data_set)
        # next(io_string)
        # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #     _, created = Bale.objects.update_or_create(
        #         Bale_ID=column[0],
        #         Lot_ID=column[1],
        #         Station=column[2],
        #         Crop_Year=column[3],
        #         Pick=column[4],
        #         Staple_Type=column[5],
        #         Staple_length=column[6],
        #         Trash=column[7],
        #         Bundle_Strength=column[8],
        #         Micronaire=column[9],
        #         Moisture=column[10],
        #         Asking_Price=column[11]
                # user = user.objects.get(id=request.user.id)
        #     )
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
        common_header = ['Bale ID,Staple length,Trash,Bundle Strength,Micronaire,Rd,+b\r\n']
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
def searchbales(request):
    bales = Bale.objects.all()
    # if request.method == 'GET':
    #     query= request.GET.get('q')
    #     submitbutton= request.GET.get('submit')
    #     if query is not None:
    #         lookups= Q(Bale_ID__icontains=query) | Q(Lot_ID__icontains=query) | Q(Station__icontains=query) | Q(Crop_Year__icontains=query) | Q(Pick__icontains=query) | Q(Staple_Type__icontains=query) | Q(Staple_length__icontains=query) | Q(Trash__icontains=query) | Q(Bundle_Strength__icontains=query) | Q(Micronaire__icontains=query) | Q(Moisture__icontains=query) | Q(Asking_Price__icontains=query)
    #         results= Bale.objects.filter(lookups).distinct()
    #         context={'results': results,
    #                  'submitbutton': submitbutton}
    #         return render(request, 'searchbales.html', context)
    return render(request,"searchbales.html",{"bales":bales})




def handler404(request,exception):
    return render(request, '404.html', status=404)
def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request,exception):
    return render(request, '403.html', status=403)