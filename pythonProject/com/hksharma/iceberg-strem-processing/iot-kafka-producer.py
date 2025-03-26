import time
import datetime
import json
import sys
import random
from kafka import KafkaProducer

topic = "KafkaGlueIcebergTopic"
client_id = "raspberrypi"


def collect_and_send_data():
    publish_count = 0
    while True:
        humidity = random.randint(0, 120)
        temp = random.randint(0, 60)
        pressure = random.randint(0, 1600)
        orientation = {"pitch": "sample", "roll": "demo", "yaw": "test"}
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(' %Y - %m - % d % H: % M: %S')
        message = {
            "client_id": client_id,
            "timestamp": timestamp,
            "humidity": humidity,
            "temperature": temp,
            "pressure": pressure,
            "pitch": orientation['pitch'],
            "roll": orientation['roll'],
            "yaw": orientation['yaw'],
            "count": publish_count
        }
        print("Publishing message to topic ‘{}’: {}".format(topic, message))
        kafka_producer(message)
        time.sleep(1)
        publish_count += 1

def kafka_producer(message):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: json.dumps(m).encode('utf - 8'))
    future = producer.send('KafkaGlueIcebergTopic', value=message, partition=0)
    future.get(timeout=10)


if __name__ == '__main__':
    collect_and_send_data()
