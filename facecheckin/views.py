from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CreateTransactionSerializer, ActivityByManagerSerializer,
    ActivityByUserSerializer,
)
from .models import Transaction
from users.permissions import Is_Superuser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from datetime import timedelta
from django.utils import timezone


class CreateTransaction(APIView):
    def post(self, request):
        serializer = CreateTransactionSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        message = {
            "status": response[0], "fullname": response[1]}
        if message["status"]:
            print("Fullname: {} -> {}".format(
                message["fullname"], serializer.validated_data["status"].capitalize()))
        else:
            print("Fullname: {}".format(message["fullname"]))
        return Response(message, status=status.HTTP_201_CREATED)


class PingAPI(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class ActivityByManager(APIView):
    permission_classes = (Is_Superuser,)

    def post(self, request):
        serializer = ActivityByManagerSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response, status=status.HTTP_200_OK)


class ActivityByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivityByUserSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user).order_by("-created_at")

        past_days = self.request.query_params.get("past_days", None)
        if past_days:

            try:
                past_days = int(past_days)
            except:
                return None

            queryset = queryset.filter(
                created_at__range=(
                    timezone.now() - timedelta(days=past_days),
                    timezone.now(),
                )
            )

        return queryset
