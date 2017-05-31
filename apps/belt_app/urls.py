from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register/process$', views.register_process),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'wish_items/create$', views.create_item, name='create_item'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^wish_items/create/process$', views.create_item_process, name='item_create_process'),
    url(r'^with_items/(?P<id>\d+)$', views.show_wish_item, name='show_item'),
    url(r'^add/(?P<id>\d+)$', views.add_item, name='add_item'),
    url(r'^remove/wish/(?P<id>\d+)$', views.remove_wish, name='remove_wish'),
    url(r'^delete/item/(?P<id>\d+)$', views.delete_item, name='delete_item')
]