from rest_framework import serializers
from .models import Transaction
from AI.recognition import recognition
from users.models import CustomUser
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .tasks import get_emotion_recognition
import threading
import time


class CreateTransactionSerializer(serializers.Serializer):
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()
    image3 = serializers.ImageField()
    image4 = serializers.ImageField()
    image5 = serializers.ImageField()
    image6 = serializers.ImageField()
    status = serializers.CharField()

    def validate_status(self, value):
        valid_data = list(
            map(lambda x: x[0], Transaction.TransactionStatus.choices))
        if value not in valid_data:
            raise serializers.ValidationError(
                "You can choose between {} and {}.".format(valid_data[0], valid_data[1]))
        return value

    def fetch_data_from_db(self):
        employees_images, emp_identification_codes = [], []
        employees_data = CustomUser.objects.only(
            "identification_code", "image1", "image2")
        for data in employees_data:
            employees_images.append(data.image1.path)
            employees_images.append(data.image2.path)
            emp_identification_codes.extend(
                [data.identification_code, data.identification_code])
        return employees_images, emp_identification_codes

    def create_transaction(self, identification_code: str, status: Transaction.TransactionStatus):
        user = CustomUser.objects.get(identification_code=identification_code)
        status = Transaction.TransactionStatus.ENTER if status == "enter" else Transaction.TransactionStatus.EXIT
        obj = Transaction.objects.create(
            user=user, status=status, datetime=timezone.now()
        )
        return "{} {}".format(user.first_name, user.last_name), obj.pk

    def recognition_process(self, input_image, employees_images: list, emp_identification_codes: list):
        return recognition(input_image, employees_images, emp_identification_codes)

    def sentiment_analysis_process(self, transaction_pk, images_path: list):
        get_emotion_recognition(images_path, transaction_pk)

    def save_images(self):
        images_path = []

        for i in range(6):
            fs = FileSystemStorage()
            image = self.validated_data[f"image{i+1}"]
            filename = fs.save(image.name, image)
            image_path = os.path.join(settings.MEDIA_ROOT, filename)
            images_path.append(image_path)

        return images_path

    def print_images_name(self):
        print(self.validated_data["image1"])
        print(self.validated_data["image2"])
        print(self.validated_data["image3"])
        print(self.validated_data["image4"])
        print(self.validated_data["image5"])
        print(self.validated_data["image6"])

    def save(self, **kwargs):
        self.print_images_name()
        images_path = self.save_images()
        image = self.validated_data["image1"]
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        emp_images, emp_identification_codes = self.fetch_data_from_db()
        result, identification_code = self.recognition_process(
            image_path, emp_images, emp_identification_codes)
        if result is True:
            status = self.validated_data["status"]
            full_name, transaction_pk = self.create_transaction(
                identification_code, status)
            threading.Thread(
                target=self.sentiment_analysis_process, args=(transaction_pk, images_path)).start()
            return result, full_name
        return result, identification_code
