from rest_framework import serializers
from .models import Transaction
from AI.recognition import recognition
from users.models import CustomUser
from django.conf import settings
from facecheckin_backend.settings import env
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, F
from django.db.models.functions import TruncDate
from django.utils import timezone
import os
from .tasks import get_emotion_recognition
import threading
from datetime import datetime


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
            user=user, status=status, created_at=timezone.now())
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


class ActivityByManagerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate_user_id(self, value):
        if not CustomUser.objects.filter(pk=value).exists():
            raise serializers.ValidationError("This user is not exists.")
        return value

    def sentiment_table(self, user_id: int, start_date, end_date, status):
        objects = Transaction.objects.filter(
            user__pk=user_id,
            status=status,
            created_at__range=(start_date, end_date),
        ).values("sentiment").annotate(count=Count("sentiment"))

        message = {
            item['sentiment']: item['count'] for item in objects}

        return message

    def avg_hour_table(self, user_id: int, start_date, end_date, status):
        transactions = Transaction.objects.filter(
            user__pk=user_id,
            status=status,
            created_at__range=(start_date, end_date),
        )

        objects = transactions.annotate(
            date=TruncDate("created_at"),
            time=F("created_at")
        ).values("date", "time", "sentiment")

        data = []
        for object in objects:
            extracted_date = object["date"]
            extracted_time = object["time"].time()
            data.append({
                "date": extracted_date,
                "time": extracted_time,
                "sentiment": object["sentiment"],
            })

        return data

    def save(self, **kwargs):
        user_id = self.validated_data["user_id"]
        start_date = self.validated_data["start_date"]
        end_date = self.validated_data["end_date"]

        return {
            "enter_sentiment_table": self.sentiment_table(
                user_id, start_date, end_date, Transaction.TransactionStatus.ENTER),
            "exit_sentiment_table": self.sentiment_table(
                user_id, start_date, end_date, Transaction.TransactionStatus.EXIT),
            "enter_avg_hour_table": self.avg_hour_table(
                user_id, start_date, end_date, Transaction.TransactionStatus.ENTER),
            "exit_avg_hour_table": self.avg_hour_table(
                user_id, start_date, end_date, Transaction.TransactionStatus.EXIT),
        }


class ActivityByUserSerializer(serializers.ModelSerializer):
    delay_penalty = serializers.SerializerMethodField()
    overtime = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ("status", "created_at", "delay_penalty", "overtime")

    def get_delay_or_overtime(self, obj, reference_time_key, threshold_key, status_check):
        if not obj.status == status_check:
            return None

        reference_time_str = env(reference_time_key)
        reference_time = datetime.strptime(reference_time_str, "%H:%M").time()

        transaction_time = obj.created_at.time()

        delay = datetime.combine(
            datetime.min, transaction_time) - datetime.combine(datetime.min, reference_time)
        delay_minutes = delay.total_seconds() / 60

        if delay_minutes >= env(threshold_key, cast=int):
            return delay_minutes
        return 0

    def get_delay_penalty(self, obj):
        return self.get_delay_or_overtime(
            obj,  "ENTER_TIME", "PENALTY_THRESHOLD", Transaction.TransactionStatus.ENTER)

    def get_overtime(self, obj):
        return self.get_delay_or_overtime(
            obj, "EXIT_TIME", "OVERTIME_THRESHOLD",  Transaction.TransactionStatus.EXIT)
