from rest_framework import serializers
from celery.result import AsyncResult

from common.serializers import RemoveNullFieldsMixin
from .models import Generator, Export


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
        fields = ('id', 'file',)


class GeneratorSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    exports = ExportSerializer(many=True, read_only=True)

    class Meta:
        model = Generator
        exclude = ('data', 'errors',)


class GeneratorDataSerializer(GeneratorSerializer):
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = Generator
        fields = ('data',)


class GeneratorErrorsSerializer(GeneratorSerializer):
    errors = serializers.JSONField(read_only=True)

    class Meta:
        model = Generator
        fields = ('errors',)
