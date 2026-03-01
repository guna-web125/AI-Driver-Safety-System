import socket
import time
import requests
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
from RPLCD.i2c import CharLCD

# ================= TELEGRAM =================
BOT_TOKEN = "8310467812:AAFEVSWLMuyuH5_fDxbH-mzTJvwqPhIfYpI"
CHAT_ID = "1549780379"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": message})


# ================= GPIO =================
TRIG = 23
ECHO = 24
VIB = 17
BUZZER = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(VIB, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)


# ================= LCD =================
lcd = CharLCD('PCF8574', 0x27)

# ================= MPU =================
mpu = mpu6050(0x68)


# ================= SOCKET SERVER =================
HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting AI connection...")
conn, addr = server.accept()
print("Connected:", addr)


# ================= FUNCTIONS =================

def buzzer_on():
    GPIO.output(BUZZER, 1)

def buzzer_off():
    GPIO.output(BUZZER, 0)


def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    stop = time.time()

    timeout = time.time() + 0.04

    while GPIO.input(ECHO) == 0:
        start = time.time()
        if start > timeout:
            return 100

    while GPIO.input(ECHO) == 1:
        stop = time.time()
        if stop > timeout:
            return 100

    dist = (stop - start) * 34300 / 2
    return dist


def check_tilt():
    accel = mpu.get_accel_data()
    if abs(accel['x']) > 2 or abs(accel['y']) > 2:
        return True
    return False


# ================= MAIN LOOP =================

while True:

    # ===== Laptop AI input =====
    try:
        data = conn.recv(1024).decode()

        if data == 'D':
            print("Drowsy Detected")

            lcd.clear()
            lcd.write_string("DROWSY DRIVER")

            buzzer_on()
            send_telegram("⚠ DRIVER DROWSY DETECTED!")

            time.sleep(2)
            buzzer_off()
            lcd.clear()

        elif data == 'U':
            print("Drunk Detected")

            lcd.clear()
            lcd.write_string("DRUNK DRIVER")

            buzzer_on()
            send_telegram("⚠ DRIVER DRUNK DETECTED!")

            time.sleep(2)
            buzzer_off()
            lcd.clear()

    except:
        pass


    # ===== Ultrasonic =====
    dist = distance()
    print("Distance:", dist, "cm")

    # ===== Obstacle Detection =====
    if dist < 20:
        print("Obstacle Detected")

        lcd.clear()
        lcd.write_string(f"Obstacle {int(dist)}cm")

        buzzer_on()
        send_telegram(f"⚠ OBSTACLE AT {int(dist)} cm")

        time.sleep(2)
        buzzer_off()
        lcd.clear()


    # ===== Tilt Detection =====
    if check_tilt():
        print("Crash/Tilt Detected")

        lcd.clear()
        lcd.write_string("Crash Detected")

        buzzer_on()
        send_telegram("🚨 VEHICLE CRASH DETECTED!")

        time.sleep(2)
        buzzer_off()
        lcd.clear()


    # ===== Vibration Detection =====
    if GPIO.input(VIB):
        print("Impact Detected")

        lcd.clear()
        lcd.write_string("Impact!")

        buzzer_on()
        send_telegram("🚨 IMPACT DETECTED!")

        time.sleep(2)
        buzzer_off()
        lcd.clear()


    # ===== Normal Display =====
    lcd.clear()
    lcd.write_string(f"Dist:{int(dist)}cm")

    time.sleep(1)
