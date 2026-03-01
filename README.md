## 🎥 Project Demo

📺 Watch the full working video here:  
https://youtu.be/tCWYuVwcb4w?si=Ytv0KomVGu7AT5Kc# 🚗 AI-Based Smart Driver Safety System using Raspberry Pi

An intelligent real-time driver monitoring and vehicle safety system using:
- Computer Vision (Eye Drowsiness Detection)
- Raspberry Pi
- Ultrasonic Sensor
- MPU6050 (Tilt/Crash Detection)
- Vibration Sensor
- Telegram Alerts
- LCD Display

---

## 📌 Project Overview

This system detects:

✔ Driver Drowsiness (using MediaPipe FaceMesh)  
✔ Drunk Driver (optional signal input)  
✔ Obstacle Detection  
✔ Crash / Tilt Detection  
✔ Impact Detection  

If any dangerous condition is detected:

- 🔊 Buzzer Alert
- 📟 LCD Notification
- 📲 Telegram Alert Message

---

## 🧠 Technologies Used

### AI (Laptop Side)
- Python
- OpenCV
- MediaPipe FaceMesh
- NumPy
- Socket Programming

### Raspberry Pi Side
- Python
- RPi.GPIO
- MPU6050
- Ultrasonic Sensor (HC-SR04)
- I2C LCD (PCF8574)
- Telegram Bot API

---

## 🏗 System Architecture

Laptop (AI Processing)
        │
        │  Socket Communication
        ▼
Raspberry Pi (Hardware Control)
        │
        ├── Ultrasonic Sensor
        ├── MPU6050
        ├── Vibration Sensor
        ├── LCD Display
        ├── Buzzer
        └── Telegram Alerts

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/AI-Driver-Safety-System.git
cd AI-Driver-Safety-System
