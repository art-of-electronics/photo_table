from machine import Pin, ADC, PWM
from time import sleep

led = Pin(15, Pin.OUT)
led.off()

adc = ADC(Pin(3))
adc.atten(ADC.ATTN_11DB)

lr_dir = Pin(7, Pin.IN, Pin.PULL_UP)
run = Pin(9, Pin.IN, Pin.PULL_UP)
mode = Pin(11, Pin.IN, Pin.PULL_UP)

en = Pin(5, Pin.OUT)
en.on()
ms1 = Pin(35, Pin.OUT)
ms1.off()
ms2 = Pin(33, Pin.OUT)
ms2.off()
dr = Pin(12, Pin.OUT)
pwm = PWM(Pin(18), duty = 0)

class cnt:
    global sw1
    global sw2
    global sw3
    global ms_mode
    global f
    sw1 = False
    sw2 = False
    sw3 = False
    ms_mode = 0
    f = 1000

def toggle_led():
    led.value(led.value()^1)
    en.value(en.value()^1)
    if en.value() == 0:
        pwm.duty(512)
    else:
        pwm.duty()

def key_dir():
    global sw1
    last_sw = sw1
    sw1 = lr_dir.value()
    if last_sw and not sw1:
        dr.value(dr.value()^1)
       
def key_run():
    global sw2
    last_sw = sw2
    sw2 = run.value()
    if last_sw and not sw2:
        toggle_led()
       
def key_mode():
    global sw3
    global ms_mode
    last_sw = sw3
    sw3 = mode.value()
    if last_sw and not sw3:
        ms_mode += 1
        if ms_mode == 1:
            ms1.on()
            ms2.on()
        elif ms_mode == 2:
            ms1.on()
            ms2.off()
        elif ms_mode == 3:
            ms1.off()
            ms2.on()
        else:
            ms1.off()
            ms2.off()
            ms_mode = 0

while True:
    f = 500 + ((int(adc.read()/100))*20)
    pwm.freq(f)
    key_dir()
    key_run()
    key_mode()
    sleep(0.01)