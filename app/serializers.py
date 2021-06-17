from rest_framework import fields, serializers
from .models import Bale

class BalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bale
        fields = '__all__'