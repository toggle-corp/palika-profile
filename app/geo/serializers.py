from rest_framework import serializers

from .models import (
    Palika,
    District,
    Province,
)


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class PalikaSerializer(serializers.ModelSerializer):
    province = serializers.IntegerField(source='district.province.pk')

    class Meta:
        model = Palika
        fields = '__all__'
