from machine import Pin, PWM
from time import sleep

# پایه‌های ENA و ENB (PWM)
ENA = PWM(Pin(22), freq=1000)  # برای موتور 1
ENB = PWM(Pin(23), freq=1000)  # برای موتور 2

# مقداردهی اولیه پین‌های موتور 1 (سمت راست)
def initialize_motor_pins_1():
    pin1 = Pin(5, Pin.OUT)   # IN1
    pin2 = Pin(18, Pin.OUT)  # IN2
    return pin1, pin2

# مقداردهی اولیه پین‌های موتور 2 (سمت چپ)
def initialize_motor_pins_2():
    pin1 = Pin(19, Pin.OUT)  # IN3
    pin2 = Pin(21, Pin.OUT)  # IN4
    return pin1, pin2

# توابع حرکت
def forward(motor_pins):
    motor_pins[0].value(1)
    motor_pins[1].value(0)

def backward(motor_pins):
    motor_pins[0].value(0)
    motor_pins[1].value(1)

def stop_motor(motor_pins):
    motor_pins[0].value(0)
    motor_pins[1].value(0)

# تابع تغییر سرعت (0 تا 1023 در ESP32)
def set_speed(motor, speed):
    motor.duty(speed)

# راه‌اندازی موتور
motor_pins_1 = initialize_motor_pins_1()
motor_pins_2 = initialize_motor_pins_2()

# سنسور چپ و راست
left_sensor = Pin(26, Pin.IN)   # GPIO26
right_sensor = Pin(25, Pin.IN)  # GPIO25



# حرکت به راست
def right():
    print('right')
    set_speed(ENA, 500)  # سرعت کمتر
    set_speed(ENB, 500)
    forward(motor_pins_1)
    backward(motor_pins_2)

# حرکت به چپ
def left():
    print('left')
    set_speed(ENA, 500)
    set_speed(ENB, 500)
    forward(motor_pins_2)
    backward(motor_pins_1)

# حرکت مستقیم
def run():
    print('run')
    set_speed(ENA, 400)  # مثلا 40% توان
    set_speed(ENB, 400)
    forward(motor_pins_1)
    forward(motor_pins_2)

# توقف
def stop():
    print('stop')
    stop_motor(motor_pins_1)
    stop_motor(motor_pins_2)
    set_speed(ENA, 0)
    set_speed(ENB, 0)

# حلقه اصلی
while True:
    left_value = left_sensor.value()
    right_value = right_sensor.value()
    print('Left:', left_value, '| Right:', right_value)
    
    if left_value == 0 and right_value == 1 and left_value == 0:
        right()
        sleep(0.1)
        stop()
        
    elif right_value == 0 and left_value == 1:
        left()
        sleep(0.1)
        stop()

    elif right_value == 0 and left_value == 0:
        stop()

    elif right_value == 1 and left_value == 1:
        run()
        sleep(0.1)
        stop()

    sleep(0.1)