from rest_framework import serializers
from celery.result import AsyncResult

from common.serializers import RemoveNullFieldsMixin
from geo.models import (
    Palika,
    District,
    Province,
)
from geo.serializers import (
    ProvinceSerializer,
    DistrictSerializer,
    PalikaSerializer,
)

from .models import Generator, Export
from .tasks import test_doc


class TaskSerializer(RemoveNullFieldsMixin, serializers.Serializer):
    task_id = serializers.CharField()
    state = serializers.SerializerMethodField()

    def state_info(self, task):
        try:
            return task.info
        except TypeError:
            return {}

    def get_state(self, obj):
        task = AsyncResult(obj['task_id'])
        return self.state_info(task)


class ExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Export
        fields = ('id', 'file', 'title')


class GeneratorSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    exports = ExportSerializer(many=True, read_only=True)

    class Meta:
        model = Generator
        exclude = ('data', 'errors', 'geo_meta',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        test_doc.delay(instance.id)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('file'):
            test_doc.delay(instance.id)
        return instance


class GeneratorDataSerializer(GeneratorSerializer):
    class Meta:
        model = Generator
        fields = ('data',)


class GeneratorMetaSerializer(GeneratorSerializer):
    geo_meta = serializers.SerializerMethodField()

    class Meta:
        model = Generator
        fields = ('errors', 'geo_meta')

    def get_geo_meta(self, obj):
        palika_codes = obj.geo_meta.get('palika_codes', [])
        provinces = Province.objects.filter(
            district__palika__code__in=palika_codes,
        ).distinct()
        districts = District.objects.filter(
            palika__code__in=palika_codes,
        ).distinct()
        palikas = Palika.objects.filter(code__in=palika_codes).distinct()
        return {
            'provinces': ProvinceSerializer(provinces, many=True).data,
            'districts': DistrictSerializer(districts, many=True).data,
            'palikaCodes': PalikaSerializer(palikas, many=True).data
        }
