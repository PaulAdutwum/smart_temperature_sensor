# 🏠 Smart Home Temperature Monitor (IoT + Edge AI)

A Raspberry Pi–based edge-AI system that continuously reads from a DS18B20 temperature sensor, runs on-device ML inference for overheat detection, and publishes data & alerts securely to AWS IoT Core. When a high-temperature event is detected, it uses the OpenAI API to generate notifications delivered via MQTT or SNS/email.

---

![Smart Home Temperature Monitor](https://github.com/user-attachments/assets/e5a75dd9-f340-449a-b49a-5b04045d810b)

---

## 🔑 Key Features

- **Real-time sensing**  
  Readings from DS18B20 1-Wire sensor at configurable intervals (default: 1 Hz).  
- **Edge inference**  
  LSTM or pickled Random Forest model on Raspberry Pi (TensorFlow Lite runtime) to predict overheating events.  
- **Secure MQTT**  
  Publishes JSON messages over TLS to AWS IoT Core with device certificates.  
- **Natural-language alerts**  
  Uses the OpenAI API to craft clear, actionable alert messages.  
- **Cloud storage & rules**  
  Routes sensor data and anomaly flags into DynamoDB or S3; triggers SNS/email notifications.  
- **Resilient service**  
  Managed by systemd with automatic restart on reboot or failure.  

---

## 🎯 Prerequisites

### Hardware

- **Raspberry Pi** (Model 3/4/Zero W) with Raspberry Pi OS (Lite or Desktop).  
- **DS18B20 1-Wire temperature sensor** wired to:  
  - DATA → GPIO 4 (pin 7)  
  - VCC → 3.3 V (pin 1)  
  - GND → GND (pin 6)  
- **4.7 kΩ pull-up resistor** between DATA and 3.3 V rail.  

### Software & Accounts

- **Python 3.7+** with `pip` & virtual-env support.  
- **AWS account** with IAM permissions for:  
  - IoT Core (Thing registry + certificates)  
  - DynamoDB OR S3 (for data storage)  
  - SNS (for alerts)  
- **OpenAI API key** (for natural-language alert generation).  

---

## 🚀 Installation & Configuration

1. **System setup & dependencies**  
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3 python3-pip python3-venv git mosquitto
