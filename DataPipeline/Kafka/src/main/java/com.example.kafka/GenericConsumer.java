package com.example.kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

public class GenericConsumer {

    private static final String BOOTSTRAP_SERVERS= "b-1.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098,b-2.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098";
    public static final String SASL_JAAS_CONFIG = String.format("software.amazon.msk.auth.iam.IAMLoginModule required;");
    private static final String groupId = "test-group";
//    private static final String topic1 = "fw_msk_trip_analytics_telemetry";




    public static void main(String[] args) {

        Properties props = new Properties();
        props.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.setProperty(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(SaslConfigs.SASL_JAAS_CONFIG, SASL_JAAS_CONFIG);
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");
        props.put(ConsumerConfig.CLIENT_ID_CONFIG, "clienID01");

        String topic1 = "test-topic-0608";

        KafkaConsumer<String,String> consumer = new KafkaConsumer<>(props);

        consumer.subscribe(List.of(topic1));

        System.out.println("Subscribed to topic " + topic1);

        while (true) {
            ConsumerRecords<String, String> consumerRecords = consumer.poll(Duration.ofMillis(1000));

            for (ConsumerRecord<String, String> record : consumerRecords) {
                System.out.println("Partition: " + record.partition() + ", Offset: " + record.offset());
                System.out.println("Key: " + record.key());
                System.out.println("Value: " + record.value());
            }
        }








    }
}
 
