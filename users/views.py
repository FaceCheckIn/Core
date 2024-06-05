from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .permissions import Is_Superuser
from .models import CustomUser
from .utils import get_user_messages, get_tokens_for_user
from .serializers import (
    LoginSerializer, ChangePasswordSerializer, UserSerializer, RegisterSerializer,
    UsersListSerializer,
)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        identification_code = serializer.validated_data["identification_code"]
        password = serializer.validated_data["password"]
        user = CustomUser.objects.get(identification_code=identification_code)
        if user.check_password(password):
            user.update_login_time()
            message = {
                "user": UserSerializer(user).data,
                "tokens": get_tokens_for_user(user),
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {"Password": get_user_messages("password")}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class Register(CreateAPIView):
    permission_classes = (Is_Superuser,)
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()


class ChangePassword(APIView):
    permission_classes = (Is_Superuser,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.change_password()
            message = {
                "message": get_user_messages("successful_change_password")}
            return Response(message, status=status.HTTP_200_OK)


class UsersList(ListAPIView):
    permission_classes = (Is_Superuser,)
    serializer_class = UsersListSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()

        search_input = self.request.query_params.get("search", None)
        if search_input is not None:
            queryset = queryset.filter(
                role__icontains=search_input)

        return queryset
