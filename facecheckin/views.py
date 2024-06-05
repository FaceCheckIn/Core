from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateTransactionSerializer, ActivityViewSerializer
from users.permissions import Is_Superuser


class CreateTransaction(APIView):
    def post(self, request):
        serializer = CreateTransactionSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        message = {
            "status": response[0], "fullname": response[1]}
        print("Fullname: {} -> {}".format(
            message["fullname"], serializer.validated_data["status"].capitalize()))
        return Response(message, status=status.HTTP_201_CREATED)


class PingAPI(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class ActivityView(APIView):
    permission_classes = (Is_Superuser,)

    def post(self, request):
        serializer = ActivityViewSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response, status=status.HTTP_200_OK)
