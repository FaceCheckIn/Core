from django.urls import path
from .views import CreateTransaction, PingAPI, ActivityView

app_name = "facecheckin"

urlpatterns = [
    path('create/', CreateTransaction.as_view(), name='create'),
    path('ping/', PingAPI.as_view(), name='PingAPI'),

    path('activity/by/manager/', ActivityView.as_view(), name='activity'),
]
