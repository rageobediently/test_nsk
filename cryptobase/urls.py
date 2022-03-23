from django.urls import path
from cryptobase import views

urlpatterns = [
    path('get_highlow/<str:pair>', views.get_high_low),
]
