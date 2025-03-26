from kafka import KafkaConsumer
from kafka.structs import TopicPartition


KAFKA_TOPIC = "spark_topic"
KAFKA_SERVER = "localhost:9092"


consumer = KafkaConsumer(
    KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER, auto_offset_reset='earliest')

partitions = consumer.partitions_for_topic(KAFKA_TOPIC)
for p in partitions:
    topic_partition = TopicPartition(KAFKA_TOPIC, p)
    # Seek offset 0
    consumer.seek(partition=topic_partition, offset=0)
    for msg in consumer:
        print(msg.value.decode("utf-8"))