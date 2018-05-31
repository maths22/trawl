from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('review', views.review, name='review'),
    path('submit_template', views.submit_template, name='submit_template'),
]
