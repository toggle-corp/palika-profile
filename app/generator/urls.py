from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^add/$', views.add, name='add'),
]
