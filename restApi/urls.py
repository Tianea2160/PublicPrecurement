from django.urls import path, include
from . import views

urlpatterns = [
    path('corporation/', views.CorporationCreate.as_view()),
    path('corporation/<int:pk>/', views.CorporationDetail.as_view()),
]