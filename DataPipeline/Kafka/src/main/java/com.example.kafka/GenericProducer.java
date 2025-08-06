package com.example.kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.config.SaslConfigs;

import java.util.Properties;

public class GenericProducer {

    private static final String BOOTSTRAP_SERVERS= "b-1.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098,b-2.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098";
    public static final String SASL_JAAS_CONFIG = String.format("software.amazon.msk.auth.iam.IAMLoginModule required;");


    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");

        props.put(SaslConfigs.SASL_JAAS_CONFIG, SASL_JAAS_CONFIG);
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        KafkaProducer<String,String> kafkaProducer = new KafkaProducer<>(props);

        String key1 = "user1";
        String value1 = "given the value of user1";
        String topic1 = "test-topic-0608";

        ProducerRecord<String,String> producerRecord1 = new ProducerRecord<>(topic1,key1, value1);

        kafkaProducer.send(producerRecord1);


        kafkaProducer.send(producerRecord1, (metadata, exception) -> {
            if (exception == null) {
                System.out.printf("Sent record to topic %s, partition %d, offset %d%n",
                        metadata.topic(), metadata.partition(), metadata.offset());
            } else {
                exception.printStackTrace();  // shows any connection/auth issues
            }
        });
        kafkaProducer.flush();
        kafkaProducer.close();
    }
}
 
