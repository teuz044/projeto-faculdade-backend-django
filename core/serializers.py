from rest_framework import serializers
from .models import Acidente

class AcidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acidente
        fields = '__all__'
