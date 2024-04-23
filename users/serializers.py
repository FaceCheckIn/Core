from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .utils import get_user_messages, is_valid_iran_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "identification_code", "first_name", "last_name", "role",
            "is_active", "is_staff", "is_superuser",
        )


class LoginSerializer(serializers.Serializer):
    identification_code = serializers.CharField()
    password = serializers.CharField()

    def validate_identification_code(self, value):
        if not CustomUser.objects.filter(identification_code=value).exists():
            raise serializers.ValidationError(
                get_user_messages("identification_code_not_exists"))
        return value


class RegisterSerializer(serializers.Serializer):
    identification_code = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if CustomUser.objects.filter(identification_code=attrs["identification_code"]).exists():
            raise ValidationError(
                {"identification_code": get_user_messages("identification_code_exists")})
        if not is_valid_iran_code(attrs["identification_code"]):
            raise ValidationError(
                {"identification_code": get_user_messages("identification_invalid")})
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(
                {"passwords": get_user_messages("equal_passwords")})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    superuser_password = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["superuser_password"]):
            raise ValidationError(
                {"password": get_user_messages("wrong_password")})
        if attrs["new_password"] != attrs["confirm_password"]:
            raise ValidationError(
                {"passwords": get_user_messages("equal_passwords")})
        return attrs

    def change_password(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
