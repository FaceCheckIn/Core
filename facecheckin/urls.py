from django.urls import path
from .views import CreateTransaction, PingAPI

app_name = "facecheckin"

urlpatterns = [
    path('create/', CreateTransaction.as_view(), name='create'),
    path('ping/', PingAPI.as_view(), name='PingAPI'),
]
