from django.urls import path
from .views import CreateTransaction, PingAPI, ActivityByManager, ActivityByUser

app_name = "facecheckin"

urlpatterns = [
    path('create/', CreateTransaction.as_view(), name='create'),
    path('ping/', PingAPI.as_view(), name='PingAPI'),

    path('activity/by/manager/',
         ActivityByManager.as_view(), name='ActivityByManager'),
    path('activity/by/user/',
         ActivityByUser.as_view(), name='ActivityByUser'),
]
