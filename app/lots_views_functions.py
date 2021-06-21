from .models import TestBale, Bale
from django.db.models import Avg, Max, Min, Sum


def get_lots_views_data(station_txt, variety_txt):

    query_string = f"SELECT id, Lot_ID, COUNT(Bale_ID) as count_of_bales, Station, variety, weightinkg," \
                   f"Organic, BCI FROM app_bale " \
                   f"WHERE station like '{station_txt}' AND variety like '{variety_txt}'" \
                   f"GROUP BY Lot_ID"
    bales = Bale.objects.raw(query_string)
    new_data = []
    for i in bales:
        #Lot_id = Bale.objects.get(Bale_ID=i.Bale_ID, Lot_ID=i.Lot_ID, Station=i.Station, variety=i.variety)
        for_sale_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(Available_For_Sale=True).count()

        max_staple = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Staple_length'))['Staple_length__max']
        min_staple = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Staple_length'))['Staple_length__min']
        max_mic = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Micronaire'))['Micronaire__max']
        min_mic = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Micronaire'))['Micronaire__min']

        max_rd = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Rd'))['Rd__max']
        min_rd = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Rd'))['Rd__min']

        max_price = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Spot_Price'))['Spot_Price__max']
        min_price = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Spot_Price'))['Spot_Price__min']

        organic_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(Organic=True).count()
        bci_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(BCI=True).count()

        max_gtex = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('GTex'))['GTex__max']
        min_gtex = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('GTex'))['GTex__min']

        bales_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter().count()

        new_data.append({
            'Lot_ID': i.Lot_ID,
            'station': i.Station,
            'variety': i.variety,
            'total_bales': bales_count,
            'for_sale': for_sale_count,
            'mic_range': str(min_mic) + " - " + str(max_mic),
            'staple_range': str(min_staple) + " - " + str(max_staple),
            'rd_range': str(min_rd) + " - " + str(max_rd),
            'price_range': str(min_price) + " - " + str(max_price),
            'organic_count': str(organic_count),
            'bci_count': str(bci_count),
            'gtex_range': str(min_gtex) + " - " + str(max_gtex),
        })

    print(new_data)
    return new_data

def get_lots_views_data_fromstation(station_txt):

    query_string = f"SELECT id, Lot_ID, COUNT(Bale_ID) as count_of_bales, Station, variety, weightinkg," \
                   f"Organic, BCI FROM app_bale " \
                   f"WHERE station like '{station_txt}'" \
                   f"GROUP BY variety, Lot_ID"
    bales = Bale.objects.raw(query_string)
    new_data = []
    for i in bales:
        #Lot_id = Bale.objects.get(Bale_ID=i.Bale_ID, Lot_ID=i.Lot_ID, Station=i.Station, variety=i.variety)
        for_sale_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(Available_For_Sale=True).count()

        max_staple = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Staple_length'))['Staple_length__max']
        min_staple = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Staple_length'))['Staple_length__min']
        max_mic = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Micronaire'))['Micronaire__max']
        min_mic = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Micronaire'))['Micronaire__min']

        max_rd = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Rd'))['Rd__max']
        min_rd = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Rd'))['Rd__min']

        max_price = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('Spot_Price'))['Spot_Price__max']
        min_price = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('Spot_Price'))['Spot_Price__min']

        organic_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(Organic=True).count()
        bci_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter(BCI=True).count()

        max_gtex = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Max('GTex'))['GTex__max']
        min_gtex = Bale.objects.filter(Lot_ID=i.Lot_ID).aggregate(Min('GTex'))['GTex__min']

        bales_count = Bale.objects.filter(Lot_ID=i.Lot_ID).filter().count()

        new_data.append({
            'Lot_ID': i.Lot_ID,
            'station': i.Station,
            'variety': i.variety,
            'total_bales': bales_count,
            'for_sale': for_sale_count,
            'mic_range': str(min_mic) + " - " + str(max_mic),
            'staple_range': str(min_staple) + " - " + str(max_staple),
            'rd_range': str(min_rd) + " - " + str(max_rd),
            'price_range': str(min_price) + " - " + str(max_price),
            'organic_count': str(organic_count),
            'bci_count': str(bci_count),
            'gtex_range': str(min_gtex) + " - " + str(max_gtex),
        })

    print(new_data)
    return new_data
