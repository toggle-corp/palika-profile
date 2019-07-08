from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf.urls import url, static
from django.urls import include, path
from django.views.static import serve
from rest_framework import routers
from django.conf import settings
from django.contrib import admin

from generator.apis import (
    GeneratorViewSet,
    TaskViewSet,
)
from generator.views import (
    get_latest_palika_pdf,
    download_export_as_zip,
)

# Rest Routers
router = routers.DefaultRouter()

router.register(r'generators', GeneratorViewSet, basename='generator')
router.register(r'tasks', TaskViewSet, basename='task')

# Versioning : (v1|v2|v3)
API_PREFIX = r'^api/(?P<version>(v1))/'


def get_api_path(path):
    return '{}{}'.format(API_PREFIX, path)


urlpatterns = [
    # Admin url patterns
    path('admin/', admin.site.urls),

    # Recent palika document
    url(
        r'^recent-palika-document/(?P<palika_code>\d+)/(?P<language>\w+)/$',
        get_latest_palika_pdf,
        name='recent-palika-document',
    ),
    url(
        r'^download-palika-documents/$',
        download_export_as_zip,
        name='recent-palika-document',
    ),

    # API url patterns
    url(get_api_path(''), include(router.urls)),

    # App url patterns
    url(r'^generators/', include(
        ('generator.urls', 'generator'),
        namespace='generator'),
        ),

] + static.static(
    settings.MEDIA_URL, view=xframe_options_exempt(serve),
    document_root=settings.MEDIA_ROOT
)
