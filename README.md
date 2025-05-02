# Smart Home Temperature Monitor (IoT)

A Raspberry Pi–based edge-AI temperature monitoring system that reads from a DS18B20 sensor, runs on-device inference, and publishes data & alerts to AWS IoT Core. When overheating is detected, it leverages the OpenAI API to generate human-friendly notifications and can fan out through MQTT or SNS/email.

---

![Image](https://github.com/user-attachments/assets/e5a75dd9-f340-449a-b49a-5b04045d810b)
---

## Features

- 🔥 **Real-time sensing** of temperature via the DS18B20 1-Wire sensor  
- 🤖 **Edge inference**: threshold-based or pickled ML model for “overheat” detection  
- ☁️ **Secure MQTT**: publishes JSON to AWS IoT Core over TLS  
- 📨 **Natural-language alerts**: OpenAI-powered alert messages  
- 📊 **Cloud storage & rules**: route readings into DynamoDB/S3, SNS alerts  
- 🔄 **Resilient service**: runs under systemd with auto-restart on reboot/failure  

---

## Prerequisites

- **Hardware**  
  - Raspberry Pi (3/4/Zero W) running Raspberry Pi OS (Lite or Desktop)  
  - DS18B20 1-Wire temperature sensor wired to GPIO 4 + 3.3 V + GND  

- **Software & Accounts**  
  - Python 3.7+ & `pip`  
  - AWS account with: IoT Core Thing + certificates, DynamoDB/S3/SNS permissions  
  - OpenAI API key (for alert generation)  

---

## Installation & Setup

```bash
# 1. Update & install system packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git

# 2. Enable 1-Wire interface
echo "dtoverlay=w1-gpio,gpiopin=4" | sudo tee -a /boot/config.txt
sudo modprobe w1-gpio w1-therm

# 3. Clone project & create venv
git clone https://github.com/<your-username>/temp-monitor.git
cd temp-monitor
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
pip install --upgrade pip
pip install w1thermsensor paho-mqtt boto3 openai
