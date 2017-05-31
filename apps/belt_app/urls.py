from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/process$', views.register_process),
    url(r'^login$', views.login)
]