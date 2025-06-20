**Possible changes**
1. Field is renamed  ( isn't it considered as a new field, meaning old field is removed , new field is added)
2. Existing field is missing ( is there any clause for mandatory field -> check in respect to JSON , avro and protobuf) 
3. New field is added
4. Data Type of existing field is changed


## **Backward compatibility**
- it ensures new data is read by old code 
- New schema can write data that old consumers can still read
- ✅ 1. Backward Compatibility (Most common in production)
- `
**🔁 New schema can write data that old consumers can still read**

Version	Change
V1	{ "name": "Alice" }
V2	{ "name": "Alice", "age": 30 } with default age

💡 Safe Change Example:

```json

// V1
{ "name": "string" }

// V2
{ "name": "string", "age": ["null", "int"], "default": null }
```
----> schema is evolving with no change in consumer code , consumer should not break
Schema ---> [v1,v2,v3]
Code -----> [v1]

**✅ 2. Forward Compatibility**
🔁 Old schema wrote data that new consumers can still read

Version	Change
V1	{ "name": "Alice" }
V2	{ "name": "Alice", "age": 30 } — tries to read V1 data

💡 New reader must handle missing age (e.g., by checking for null/defaults).

----> schema is evolving with consumer code is evolving , consumer should not break
Schema ---> [v1,v2,v3]
Code -----> [v1 , v2]
code v2 should be able to read schema version v1 with 

1. Design Principlas for schema evolution

**Json Schema**

Defines an object with two properties: id (integer) and name (string)
Only id is required
```json
{
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "name": { "type": "string" }
  },
  "required": ["id"]
}
```

Sample Data
```json
{
  "id": 1,
  "name": "Alice"
}
```

**Avro Schema**
Defines a record named User with two fields: id and name

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    { "name": "id", "type": "int" },
    { "name": "name", "type": "string" }
  ]
}
```

**Proto schema**
Defines a User message with id (field 1) and name (field 2)

```jsom
syntax = "proto3";

message User {
  int32 id = 1;
  string name = 2;
}
```

| Feature           | JSON Schema              | Avro Schema                   | Protobuf                      |
|-------------------|--------------------------|-------------------------------|-------------------------------|
| Human-readable    | Yes                      | Yes (JSON format)             | Less so (compiled binary)     |
| Requires defaults | No                       | Yes (for compatibility)       | No (but optional fields help) |
| Used in           | REST APIs, validation    | Kafka, streaming              | gRPC, compact serialization   |
| Type              | Descriptive schema       | Self-describing data records  | Strongly typed ID-based       |



**Schema Evolution Lifecycle:**

1. Design Principles for Schema Evolution
a. Schema Compatibility Contracts
Follow backward-compatible or forward-compatible schema evolution.

Protobuf, Avro, and Thrift support versioning and compatibility rules (e.g., adding optional fields, avoiding deletions).

b. Schema as Code
Define schemas in version-controlled repositories.

Use Pull Request (PR) workflows for schema changes.

Example: GitHub repo containing .proto or .avsc files.

🧰 2. Schema Registry (Core for Evolution)
Industry-standard tools like:

Confluent Schema Registry (for Avro/Protobuf/JSON)

AWS Glue Schema Registry

Apicurio (Open-source)

Key Benefits:
Central store of all schema versions

Enforces compatibility rules (backward, forward, full)

Enables schema validation at write time or read time


🧪 3. Enforcing Contracts Between Producers and Consumers
a. Data Contract Testing
Teams must validate schema changes before publishing data.

Use frameworks like:

Propan, Spectral, or Data Contract CLI

Custom CI/CD checks using avro-tools or protobuf compilers

b. Pre-deployment CI/CD Hooks
Block deployment if schema compatibility fails

Example: a new field added to Kafka topic must be optional or have a default

🧯 4. Change Management Process
a. Breaking vs. Non-breaking Changes
Change Type	Impact	Best Practice
Add new optional field	Non-breaking	👍 Allowed
Remove field	Breaking	🚫 Avoid
Rename field	Breaking	🚫 Avoid
Change data type	Breaking	🚫 Avoid



TODO:
Things to try:

⚙️ ✅ Setup Overview
Stack:
Kafka (Confluent Platform)

Schema Registry

Avro (used for demonstration)

Python or Java producer/consumer

Docker Compose for local services

🧪 Step-by-Step: Simulate Schema Evolution Locally
🔧 1. Docker Compose Setup for Kafka + Schema Registry
Create a file: docker-compose.yml

yaml
Copy
Edit
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on:
      - kafka
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: PLAINTEXT://kafka:9092
Start the services:

bash
Copy
Edit
docker-compose up -d
📄 2. Define Initial Avro Schema
user_v1.avsc:

json
Copy
Edit
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "name", "type": "string" },
    { "name": "age", "type": "int" }
  ]
}
Later, evolve it with a new optional field:

user_v2.avsc:

json
Copy
Edit
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "name", "type": "string" },
    { "name": "age", "type": "int" },
    { "name": "email", "type": ["null", "string"], "default": null }
  ]
}
🐍 3. Python Producer and Consumer (Optional Java Version Available)
Install dependencies:
bash
Copy
Edit
pip install confluent_kafka avro-python3
Producer with Avro
python
Copy
Edit
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro import loads

value_schema = loads(open("user_v1.avsc").read())

producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
}, default_value_schema=value_schema)

producer.produce(topic='user-topic', value={"name": "Alice", "age": 25})
producer.flush()
Later, test schema evolution by switching to user_v2.avsc and:

python
Copy
Edit
value_schema = loads(open("user_v2.avsc").read())
producer = AvroProducer({...}, default_value_schema=value_schema)
producer.produce(topic='user-topic', value={"name": "Bob", "age": 30, "email": "bob@example.com"})
🧾 4. Test Consumer for Backward Compatibility
python
Copy
Edit
from confluent_kafka.avro import AvroConsumer

consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group',
    'schema.registry.url': 'http://localhost:8081',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['user-topic'])

while True:
    msg = consumer.poll(1.0)
    if msg:
        print("Received: ", msg.value())
🧪 5. Try Schema Evolution Scenarios
✅ Add optional field (Backward Compatible)
Works without consumer change

❌ Remove a field or change data type (Breaking)
Consumer may crash or receive nulls

Schema Registry will block publishing if compatibility mode is set

🛠️ 6. Set Schema Compatibility Mode
Use Schema Registry REST API:

bash
Copy
Edit
# Check current compatibility
curl -X GET http://localhost:8081/config

# Set compatibility for a subject
curl -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"compatibility": "BACKWARD"}' \
    http://localhost:8081/config/user-topic-value
✅ Recap: What You Achieve
Local environment simulating a production-like setup

Schema versioning and evolution using Schema Registry

Kafka topic producers/consumers validating schema compatibility

Confidence in evolving data contracts in multi-team setups

Would you like:

A GitHub repo template for this setup?

Java version instead of Python?

Or do you use formats like Protobuf, JSON, or Delta/Iceberg?
