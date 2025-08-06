package com.example.kafka;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.common.config.SaslConfigs;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class DeleteKafkaTopic {

    private static final String BOOTSTRAP_SERVERS= "b-1.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098,b-2.uatfleetwiseincomingt.txogb6.c2.kafka.ap-south-1.amazonaws.com:9098";
    public static final String SASL_JAAS_CONFIG = String.format("software.amazon.msk.auth.iam.IAMLoginModule required;");


    public static void main(String[] args) throws ExecutionException, InterruptedException {

        Properties props = new Properties();
        props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(SaslConfigs.SASL_JAAS_CONFIG, SASL_JAAS_CONFIG);
        props.put(SaslConfigs.SASL_MECHANISM, "AWS_MSK_IAM");
        props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        props.put(SaslConfigs.SASL_CLIENT_CALLBACK_HANDLER_CLASS, "software.amazon.msk.auth.iam.IAMClientCallbackHandler");

        Admin admin = Admin.create(props);

        List<String> topicsToDelete = new ArrayList<>();
        topicsToDelete.add("test-topic-0608");

        admin.deleteTopics(topicsToDelete).all().get();
    }
}
 
