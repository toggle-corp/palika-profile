from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list, name='generator_list'),
    url(r'^add/$', views.add, name='generator_add'),
]
