from .models import TestBale, Bale
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
import csv,json
import codecs


def add_bales_function(request):
    data = TestBale.objects.all()
    User = get_user_model()
    users = User.objects.all()
    if request.method == "POST":
        csv_file = request.FILES['formFile']
        task = request.POST.get('country')
        print("🚀 ~ file: views.py ~ line 136 ~ task", task)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        common_header = ['\ufeffginnerid', 'baleid', 'lotid', 'variety', 'station ', 'crop year', 'staple ',
                         'micronaire', 'Rd', ' Gtex', 'spot_price', 'weightinkg', 'for_sale', 'organic', 'BCI']
        reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
        for j, column in enumerate(reader):
            if j == 0:
                if common_header != column:
                    messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
                    break
                else:
                    messages.success(request, 'Records Imported!')

            if j != 0:
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
                    ginnerid=column[0],
                    Bale_ID=column[1],
                    Lot_ID=column[2],
                    variety=column[3],
                    Station=column[4],
                    Crop_Year=column[5],
                    Staple_length=column[6],
                    Micronaire=column[7],
                    Rd=column[8],
                    GTex=column[9],
                    Spot_Price=column[10],
                    weightinkg=column[11],
                    Available_For_Sale=sale,
                    Organic=org_up,
                    BCI=bci_up,
                    user=User.objects.get(id=request.user.id)
                )
                created.save()

    return users

def add_test_data_function(request):
    data = TestBale.objects.all()
    if request.method == "POST":
        csv_file = request.FILES['formFile']
        common_header = ['\ufeffBale ID','Staple length','Trash','Bundle Strength','Micronaire','Rd','b','test by fc','test_report\r\n']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        for index, row in enumerate(csv_file):
            data = row.decode('utf-8')
            if data:
                line = data.split('","')
                print("🚀 ~ file: views.py ~ line 80 ~ line", line)
            if index == 0:
                if (line != common_header):
                    messages.error(request, 'THIS IS NOT SAME HEADER CSV FILE')
                    print("XXXXX")
                    print(line)
                    print(common_header)
                else:
                    messages.success(request, 'Records Correct, not imported yet!')
