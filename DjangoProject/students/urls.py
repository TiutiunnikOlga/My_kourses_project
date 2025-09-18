from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('about/', views.about, namespace='about'),

]