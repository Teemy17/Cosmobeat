from gpiozero import Button, PWMLED, Buzzer
from mpu6050 import mpu6050

class Hardware:
    def __init__(self):
        # GPIO setup for buttons and LEDs
        self.button_1 = Button(17)
        self.button_2 = Button(26)
        
        self.buzzer = Buzzer(4)
        
        self.led_1 = PWMLED(12)
        self.led_2 = PWMLED(16)
        self.led_3 = PWMLED(20)
        self.led_4 = PWMLED(21)
        # MPU6050 sensor setup
        self.sensor = mpu6050(0x68)
