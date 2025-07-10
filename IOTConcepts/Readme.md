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

    

    
#### Step by Step Commands:

 ```bash   
# 1. Create Thing
aws iot create-thing --thing-name "MySmartBulb"

# 2. Create Certificates
aws iot create-keys-and-certificate

# 3. Attach Policy
aws iot attach-policy --policy-name "BulbPolicy" --target "arn:aws:iot:..."

# 4. Attach Certificate to Thing
aws iot attach-thing-principal --thing-name "MySmartBulb" --principal "arn:aws:iot:..."

Example


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

# AWS Fleetwise onboarding 

### AWS Setup:

```bash    
# 1. Create Vehicle (Thing)
aws iot create-thing --thing-name "MyVehicle"

# 2. Create & Register Certificates
aws iot create-keys-and-certificate
aws iot attach-thing-principal

# 3. Create FleetWise Vehicle
aws iotfleetwise create-vehicle \
    --vehicle-name "MyVehicle"

 ```   

    
### Signal Catalog Setup:

 ```json   
{
    "name": "vehicle-signal-catalog",
    "nodes": [
        {
            "branch": {
                "fullyQualifiedName": "Vehicle",
                "description": "Vehicle Signals"
            }
        },
        {
            "sensor": {
                "fullyQualifiedName": "Vehicle.Speed",
                "dataType": "DOUBLE"
            }
        }
    ]
}
```
    

    
### Vehicle Model:

``bash    
# Define vehicle model
aws iotfleetwise create-decoder-manifest
aws iotfleetwise create-vehicle-model
``
    

    
### On Vehicle Setup:

    
1. Install FleetWise Agent on TCU:
   - Configure credentials
   - Set endpoint
   - Configure CAN bus interfaces

2. Configure Data Collection:
   - Signal mappings
   - Collection schemes
   - Upload rules

    

    
###  Campaign Setup:

`bash    
# Create campaign for data collection
aws iotfleetwise create-campaign \
    --name "MyDataCollection" \
    --signal-catalog-arn "arn:..." \
    --target-arn "arn:..."
`
    

    
## Complete Flow:

`bash    
[Vehicle Hardware]
        ↓
[Install FW Agent on TCU]
        ↓
[AWS IoT Core Setup]
        ↓
[Signal Catalog Definition]
        ↓
[Vehicle Model Creation]
        ↓
[Campaign Creation]
        ↓
[Data Collection Starts]

`  

    
### Key Components to Configure:

1. Vehicle Registration
2. Signal Catalog
3. Decoder Manifest
4. Vehicle Model
5. FleetWise Agent
6. Collection Schemes
7. Campaigns


# Overall Setup 

### One time setup ( Fleet level)
1. Signal Catalog Definition
2. Vehicle Model Creation
3. Decoder Manifest
4. Collection Schemes (base templates)


### Pervehicle Setup 
1. Vehicle Registration:
   aws iot create-thing --thing-name "Vehicle123"
   aws iotfleetwise create-vehicle --vehicle-name "Vehicle123"

2. Certificate Creation & Assignment:
   
   aws iot create-keys-and-certificate
   aws iot attach-thing-principal

4. FleetWise Agent Installation on TCU:
   - Install agent
   - Configure certificates
   - Set endpoint
   - Configure CAN mappings

5. Associate Vehicle with Model:
   
   aws iotfleetwise associate-vehicle-fleet

# Relation between Thing and Vehicle

```bash
# 1. Create Thing
aws iot create-thing --thing-name "MyThing123"

# 2. Create Certificate
aws iot create-keys-and-certificate --set-as-active
    # This generates:
    # - Certificate
    # - Private key
    # - Certificate ARN

# 3. Create Vehicle
aws iotfleetwise create-vehicle --vehicle-name "Vehicle456"

# 4. The actual mapping happens in FleetWise Agent Configuration:
{
    "endpoint": "xxxxx.iot.region.amazonaws.com",
    "thing_name": "MyThing123",        # <-- This is where mapping happens
    "vehicle_name": "Vehicle456",
    "certificate_path": "/path/to/cert.pem",
    "private_key_path": "/path/to/private.key"
}

    

    
The Connection Flow:

    
[FleetWise Agent]
      ↓
Uses Thing name ("MyThing123") for IoT Core connection
      ↓
Uses Vehicle name ("Vehicle456") for FleetWise data mapping

    

    
Think of it as:

Thing name = Login credential
Vehicle name = Profile identifier
The Agent configuration ties them together

```
