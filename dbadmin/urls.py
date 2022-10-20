from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('take_sample/', views.take_sample, name='take_sample')
]
