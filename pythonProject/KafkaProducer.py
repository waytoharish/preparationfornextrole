from kafka import KafkaProducer

topic = 'spark_topic'
bootstrap_servers = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Generate 100 messages
for _ in range(100):
    msg = f'Kontext kafka msg: {_}'
    future = producer.send(topic, msg.encode('utf-8'))
    print(f'Sending msg: {msg}')
    result = future.get(timeout=60)

metrics = producer.metrics()
print(metrics)