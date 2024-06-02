from celery import shared_task
from AI.emotion_recognition.main_ER import main
from facecheckin.models import Transaction


@shared_task
def get_emotion_recognition(images: list, transaction_pk: int):
    emotion = main(images)
    try:
        obj = Transaction.objects.get(pk=transaction_pk)
        obj.sentiment = emotion
        obj.save()
    except Transaction.DoesNotExist:
        print("There is an error of a transaction that does not exist.")
