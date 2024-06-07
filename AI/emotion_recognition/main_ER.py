from .emotion_recognition import emotion_recognition
from collections import Counter


images = []


def main(images):
    emotions = []

    for img in images:
        em = emotion_recognition(img)
        emotions.append(em)

    print(emotions)
    label_counts = Counter(emotions)
    the_emotion, count = label_counts.most_common(1)[0]

    return the_emotion
