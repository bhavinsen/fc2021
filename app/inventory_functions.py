from .models import TestBale, Bale
from django.db.models import Avg, Max, Min, Sum

def get_inventory_data():
    bales = Bale.objects.raw(
        "SELECT id, Bale_ID, COUNT(Bale_ID) as count_of_bales, Station, variety, weightinkg, MAX(Staple_length) as max_sl, min(Staple_length) as min_sl, max(Micronaire), min(Micronaire), max(Rd), min(Rd), "
        "Organic, BCI FROM app_bale GROUP BY Station, variety")
    new_data = []
    for i in bales:
        LOt_id = Bale.objects.get(Bale_ID=i.Bale_ID, Lot_ID=i.Lot_ID, Station=i.Station, variety=i.variety)
        print("🚀 ~ file: views.py ~ line 310 ~ bale_id", LOt_id.Lot_ID)

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

        max_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('Spot_Price'))[
            'Spot_Price__max']
        min_price = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('Spot_Price'))[
            'Spot_Price__min']

        organic_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(Organic=True).count()
        bci_count = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).filter(BCI=True).count()

        max_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Max('GTex'))['GTex__max']
        min_gtex = Bale.objects.filter(Station=i.Station).filter(variety=i.variety).aggregate(Min('GTex'))['GTex__min']

        # bales_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter().count()

        new_data.append({
            'Lot_ID': i.Lot_ID,
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

    return new_data
