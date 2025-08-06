package com.example.kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.config.SaslConfigs;

import java.util.Collections;
import java.util.Properties;
import java.util.Set;
import java.util.concurrent.ExecutionException;

public class ListKafkaTopics {

    private static final String BOOTSTRAP_SERVERS= "b-1.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098,b-2.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098";
    public static final String SASL_JAAS_CONFIG = String.format("software.amazon.msk.auth.iam.IAMLoginModule required;");




    public static void main(String[] args) throws ExecutionException, InterruptedException {
        // Create a Properties object to hold the configuration for the KafkaConsumer
        Properties props = new Properties();
        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(SaslConfigs.SASL_JAAS_CONFIG, SASL_JAAS_CONFIG);
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");



        Admin admin = Admin.create(props);

        Set<String> topicList = admin.listTopics().names().get();

        for (String topic : topicList){
            System.out.println(topic);
        }



    }
}
 
