from django.contrib import admin
from django.urls import path
from newapp.apps import NewappConfig
from newapp.views import contacts

app_name = NewappConfig.name

urlpatterns = [
    path('contacts/',contacts, name='contacts')
]