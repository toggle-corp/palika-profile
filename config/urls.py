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
