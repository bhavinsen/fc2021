# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TestBale(models.Model):
    Bale_ID = models.CharField(max_length=255,null=False,blank=False)
    Staple_length = models.CharField(max_length=255,null=False,blank=False)
    Trash = models.CharField(max_length=255,null=False,blank=False)
    Bundle_Strength = models.CharField(max_length=255,null=False,blank=False)
    Micronaire = models.CharField(max_length=255,null=False,blank=False)
    Rd = models.CharField(max_length=255,null=False,blank=False)
    b = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.Bale_ID


class Bale(models.Model):
    Bale_ID = models.CharField(max_length=255,null=False,blank=False)
    Lot_ID = models.CharField(max_length=255, null=False, blank=False)
    Station = models.CharField(max_length=255,null=False,blank=False)
    Crop_Year = models.CharField(max_length=255,null=False,blank=False)
    Pick = models.CharField(max_length=255,null=False,blank=False)
    Staple_Type = models.CharField(max_length=255,null=False,blank=False)
    Staple_length = models.CharField(max_length=255,null=False,blank=False)
    Trash = models.CharField(max_length=255,null=False,blank=False)
    Bundle_Strength = models.CharField(max_length=255,null=False,blank=False)
    Micronaire = models.CharField(max_length=255,null=False,blank=False)
    Moisture = models.CharField(max_length=255,null=False,blank=False)
    Asking_Price = models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.Lot_ID