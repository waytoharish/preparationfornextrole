# Connecting Physical device locally 

![image](https://github.com/user-attachments/assets/45c944b9-8acb-415c-a9a2-91b7478b0701)

```pgsql
[Bulb/ESP32] ←→ [Local WiFi] ←→ [Laptop]
   192.168.1.100        192.168.1.5
   
Simple HTTP or MQTT:
- Basic authentication (if needed)
- Username/password is enough
- Same network communication

```

# Basic analogy of AWS IOT core

### Key Points:

1. AWS IoT SDK = MQTT Client Library + AWS specific features (certs, reconnect, shadows)
2. AWS IoT Core = Managed Mosquitto Broker + AWS Features (rules, security, scaling)

### Think of it as:

1. Mosquitto = Basic email server you manage
2. AWS IoT Core = Gmail with extra features (managed, secure, scalable)

# Comparison in differnt clouds

all three cloud providers have similar IoT solutions. Here's a comparison:

```pgsql
AWS IoT:

    
[Device] → [AWS IoT SDK] → [AWS IoT Core (MQTT Broker)] → [AWS Services]

    

    
Azure IoT:

    
[Device] → [Azure IoT SDK] → [Azure IoT Hub (MQTT Broker)] → [Azure Services]

    

    
Google Cloud IoT:

    
[Device] → [Google IoT SDK] → [Cloud IoT Core (MQTT Broker)] → [GCP Services]

    
```
    
### Common Features Across All:

1. Device Management
2. Security/Certificates
3. Message Routing
4. Cloud Integration

### Key Differences in Names:

    
Feature          | AWS          | Azure        | GCP
-----------------|--------------|--------------|-------------
Core Service     | IoT Core     | IoT Hub      | Cloud IoT Core*
Device State     | Device Shadow| Device Twin  | Device State
Rules Engine     | Rules Engine | Message Routes| Cloud Functions


# AWS IOT core onboarding steps


Here's a checklist for onboarding a physical bulb to AWS IoT Core:

1. Device Setup:

    
Hardware:
- Microcontroller (ESP32/Arduino)
- WiFi capability
- Power supply
- LED/Bulb component

    

    
2. AWS IoT Core Setup:

    
   In AWS Console:
   1. Create Thing
   2. Generate Certificates:
      - Device certificate
      - Private key
      - Root CA certificate
   3. Create Policy
      - Allow MQTT connect/publish/subscribe

    

    
3. Device Programming:

    
Required Libraries:
- AWS IoT SDK
- WiFi library
- MQTT library

Required Configuration:
- AWS IoT endpoint
- WiFi credentials
- Certificates

    

    
4. Testing Connection:

    
Verify:
1. Device connects to WiFi
2. Device connects to AWS IoT Core
3. MQTT messages flowing
4. Device shadow updates

    

    
Step by Step Commands:

    
# 1. Create Thing
aws iot create-thing --thing-name "MySmartBulb"

# 2. Create Certificates
aws iot create-keys-and-certificate

# 3. Attach Policy
aws iot attach-policy --policy-name "BulbPolicy" --target "arn:aws:iot:..."

# 4. Attach Certificate to Thing
aws iot attach-thing-principal --thing-name "MySmartBulb" --principal "arn:aws:iot:..."

Example
```bash

Relationship Flow:
[Thing] ← attached to → [Certificate] ← attached to → [Policy]


# Create components
aws iot create-thing --thing-name "MyBulb"
aws iot create-keys-and-certificate --set-as-active  # Creates certificate
aws iot create-policy --policy-name "BulbPolicy"

# Attach relationships
aws iot attach-thing-principal \
    --thing-name "MyBulb" \
    --principal <certificate-arn>    # Attach cert to thing

aws iot attach-policy \
    --policy-name "BulbPolicy" \
    --target <certificate-arn>       # Attach policy to cert

Policy example

{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "iot:Connect",
            "iot:Publish",
            "iot:Subscribe",
            "iot:Receive"
        ],
        "Resource": [
            "arn:aws:iot:region:account:client/${iot:Connection.Thing.ThingName}"
        ]
    }]
}

```

