from rest_framework import viewsets, response, reverse
from rest_framework.decorators import action

from .models import Generator
from .tasks import (
    generate_pdf,
    test_doc,
)
from .serializers import (
    TaskSerializer,
    GeneratorSerializer,
    GeneratorDataSerializer,
    GeneratorMetaSerializer,
)


class TaskViewSet(viewsets.ViewSet):
    def retrieve(self, request, version=None, pk=None):
        serializer = TaskSerializer(data={'task_id': pk})
        serializer.is_valid()
        return response.Response(serializer.data)


class GeneratorViewSet(viewsets.ModelViewSet):
    queryset = Generator.objects.all()
    serializer_class = GeneratorSerializer

    @staticmethod
    def get_task_response(task_id, request):
        return response.Response({
            'task_id': task_id,
            'task_url': reverse.reverse(
                'task-detail',
                kwargs={
                    'version': 'v1',
                    'pk': task_id,
                },
                request=request,
            ),
        })

    @action(
        detail=True,
        url_path='data',
        serializer_class=GeneratorDataSerializer,
    )
    def get_data(self, request, pk=None, version=None):
        generator = self.get_object()
        serializer = self.get_serializer(generator)
        return response.Response(serializer.data)

    @action(
        detail=True,
        url_path='meta',
        serializer_class=GeneratorMetaSerializer,
    )
    def get_errors(self, request, pk=None, version=None):
        generator = self.get_object()
        serializer = self.get_serializer(generator)
        return response.Response(serializer.data)

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path='trigger-export',
    )
    def trigger_export(self, request, pk=None, version=None):
        if request.method == 'POST':
            generator = self.get_object()
            task_id = generate_pdf.s(
                generator.id,
                request.data.get('selected_palika_codes'),
            ).delay().id
        else:
            generator = self.get_object()
            task_id = generate_pdf.s(generator.id).delay().id
        return GeneratorViewSet.get_task_response(task_id, request)

    @action(
        detail=True,
        url_path='trigger-validation',
    )
    def trigger_validation(self, request, pk=None, version=None):
        generator = self.get_object()
        task_id = test_doc.s(generator.id).delay().id
        return GeneratorViewSet.get_task_response(task_id, request)
