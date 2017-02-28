from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^character/$', views.character_detail, name='character_detail'),
    url(r'^character/(?P<character_pk>\d+)/$', views.character_detail, name='character_detail'),
    url(r'^character/create/$', views.character_create, name='character_create'),
    url(r'^character/(?P<character_pk>\d+)/edit/$', views.character_update, name='character_update'),
    url(r'^character/(?P<character_pk>\d+)/delete/$', views.character_delete, name='character_delete'),
    url(r'^character/(?P<character_pk>\d+)/copy/$', views.character_copy, name='character_copy'),
    url(r'^character/export/$', views.character_export, name='character_export'),
    url(r'^character/import/$', views.character_import, name='character_import'),
    url(r'^character/srd/$', views.character_srd, name='character_srd'),
    url(r'^characters/delete/$', views.characters_delete, name='characters_delete'),
]
