from machine import Pin, PWM, I2C, ADC
from time import sleep
from ssd1306 import SSD1306_I2C

# Motor Initialization
def initialize_motor_pins():
    pin1 = Pin(14, Pin.OUT)  # IN1
    pin2 = Pin(12, Pin.OUT)  # IN2
    enable = Pin(13, Pin.OUT)  # ENA (Enable)
    enable.value(1)  # Set the enable pin high to enable the motor
    return pin1, pin2

def initialize_pwm():
    pwm = PWM(Pin(13), freq=15000)  # PWM on ENA pin
    pwm.duty(0)  # Start with 0 duty cycle (motor stopped)
    return pwm

def forward(speed, motor_pins, pwm):
    pwm.duty(speed)
    motor_pins[0].value(1)
    motor_pins[1].value(0)

def stop(motor_pins, pwm):
    pwm.duty(0)
    motor_pins[0].value(0)
    motor_pins[1].value(0)

# OLED Initialization
i2c = I2C(scl=Pin(5), sda=Pin(4))  # ESP8266: SCL -> D1 (GPIO5), SDA -> D2 (GPIO4)
oled_width = 128
oled_height = 32
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Motor and Sensor Initialization
motor_pins = initialize_motor_pins()
pwm = initialize_pwm()
soil_sensor = ADC(0)  # Soil sensor connected to A0

# Main Loop
while True:
    soil_moisture = soil_sensor.read()
    print("Soil Moisture:", soil_moisture)
    
    if soil_moisture > 400:  # If soil moisture exceeds 400, water the plant
        oled.fill(0)
        oled.text("Need Water!", 0, 0)
        oled.show()
        
        # Turn on motor
        forward(1024, motor_pins, pwm)
        
        # Display a loading bar on the OLED
        for i in range(0, oled_width, 8):
            oled.fill_rect(0, 16, i, 8, 1)  # Draw a rectangle to simulate loading
            oled.show()
            sleep(0.5)
        
        # Stop motor after 4 seconds
        stop(motor_pins, pwm)
        
        sleep(4)
        
        # Clear the screen after watering
        oled.fill(0)
        oled.text("Watering Done", 0, 0)
        oled.show()
        sleep(2)
    
    # Small delay before next reading
    sleep(1)
