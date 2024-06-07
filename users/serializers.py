from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .utils import get_user_messages, is_valid_iran_code
from facecheckin.models import Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "identification_code", "first_name", "last_name", "role",
            "is_active", "is_staff", "is_superuser", "image1",
        )

    def to_representation(self, instance):
        request = self.context["request"]
        res = super().to_representation(instance)
        if res["image1"] is not None:
            res["image1"] = request.build_absolute_uri(res['image1'])
        return res


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
    image2 = serializers.ImageField(required=False)
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


class UsersListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id", "identification_code", "first_name", "last_name",
            "image1", "role", "status")

    def get_status(self, obj):
        return Transaction.objects.filter(user=obj).last().status
