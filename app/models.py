# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.
class TestBale(models.Model):
    Bale_ID = models.CharField(max_length=255,null=False,blank=False)
    Staple_length = models.CharField(max_length=255,null=False,blank=False)
    Trash = models.CharField(max_length=255,null=False,blank=False)
    Bundle_Strength = models.CharField(max_length=255,null=False,blank=False)
    Micronaire = models.CharField(max_length=255,null=False,blank=False)
    Rd = models.CharField(max_length=255,null=False,blank=False)
    b = models.CharField(max_length=255,null=False,blank=False)
    test_by_fc = models.CharField(max_length=255,null=False,blank=False)
    test_report = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.Bale_ID


class Bale(models.Model):
    ginnerid = models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Bale_ID = models.CharField(max_length=255,null=False,blank=False)
    Lot_ID = models.CharField(max_length=255, null=False, blank=False)
    Station = models.CharField(max_length=255,null=False,blank=False)
    variety = models.CharField(max_length=255,null=False,blank=False)
    Crop_Year = models.CharField(max_length=255,null=False,blank=False)
    Pick = models.CharField(max_length=255,null=False,blank=False)
    Staple_Type = models.CharField(max_length=255,null=False,blank=False)
    Staple_length = models.CharField(max_length=255,null=False,blank=False)
    Trash = models.CharField(max_length=255,null=False,blank=False)
    Bundle_Strength = models.CharField(max_length=255,null=False,blank=False)
    Micronaire = models.CharField(max_length=255,null=False,blank=False)
    Moisture = models.CharField(max_length=255,null=False,blank=False)
    Rd = models.CharField(max_length=255,null=False,blank=False)
    GTex = models.CharField(max_length=255,null=False,blank=False)
    Spot_Price = models.CharField(max_length=255,null=False,blank=False)
    weightinkg = models.CharField(max_length=255,null=False,blank=False)
    Available_For_Sale = models.BooleanField(default=False,null=False,blank=False)
    Organic = models.BooleanField(default=False,null=False,blank=False)
    BCI = models.BooleanField(default=False,null=False,blank=False)

    class Meta:
        unique_together = ('Lot_ID', 'Bale_ID','Station','user','ginnerid')

    # class Meta:
    #     db_table = 'bales'
    #     constraints = [
    #         models.UniqueConstraint(fields=['Lot_ID', 'Bale_ID','Station','user','ginnerid'], name='unique appversion')
    #     ]

    def __str__(self):
        return str(self.Bale_ID) + str(self.Lot_ID) + str(self.variety) + str(self.Station)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255,null=False,blank=False)
    address  =  models.TextField(max_length=255,null=False,blank=False)
    number = models.CharField(max_length=255,null=False,blank=False)

class SeeksBidsToSupply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    numberofbales = models.CharField(max_length=255,null=False,blank=False)
    dateofdelivery = models.DateField()
    Station = models.CharField(max_length=255,null=False,blank=False)
    StapleLength = models.CharField(max_length=255,null=False,blank=False)
    MaxStapleLength = models.CharField(max_length=255,null=False,blank=False)
    Trash = models.CharField(max_length=255,null=False,blank=False)
    BundleStrength = models.CharField(max_length=255,null=False,blank=False)
    Rd = models.CharField(max_length=255,null=False,blank=False)
    bdata = models.CharField(max_length=255,null=False,blank=False)
    Organic = models.BooleanField(default=False,null=False,blank=False)
    BCI = models.BooleanField(default=False,null=False,blank=False)
    end_time = models.DateTimeField(blank=True,null=True)
    pincode = models.CharField(max_length=255,null=False,blank=False)

class AuctionMyBales(models.Model):
    bales = models.ForeignKey(Bale,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    pincode = models.CharField(max_length=255,null=False,blank=False)
    startingprice = models.CharField(max_length=255,null=False,blank=False)
    auctionduration = models.DateField(blank=True,null=True)
    paymentterms = models.CharField(max_length=255,null=False,blank=False)
    auction = models.BooleanField(default=False,null=False,blank=False)