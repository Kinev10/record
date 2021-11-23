from django.urls import path, include
from . import views
urlpatterns = [
    path('active-band', views.ActiveBandsList.as_view()),
]
