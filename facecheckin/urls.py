from django.urls import path
from .views import CreateTransaction

app_name = "facecheckin"

urlpatterns = [
    path('create/', CreateTransaction.as_view(), name='create'),
]
