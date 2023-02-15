from machine import Pin, ADC, PWM
from time import sleep

adc = ADC(0)

led = Pin(2, Pin.OUT)
led.on()

lr_dir = Pin(14, Pin.IN, Pin.PULL_UP)
run = Pin(12, Pin.IN, Pin.PULL_UP)
mode = Pin(13, Pin.IN, Pin.PULL_UP)

en = Pin(16, Pin.OUT)
en.on()
ms1 = Pin(5, Pin.OUT)
ms1.off()
ms2 = Pin(4, Pin.OUT)
ms2.off()
dr = Pin(15, Pin.OUT)
pwm = PWM(Pin(0), duty=0)


class Cnt:
    sw1 = False
    sw2 = False
    sw3 = False
    ms_mode = 0
    f = 1000


last_sw1 = last_sw2 = last_sw3 = 0


def toggle_led():
    led.value(led.value() ^ 1)
    en.value(en.value() ^ 1)
    if en.value() == 0:
        pwm.duty(512)
    else:
        pwm.duty()


def key_dir():
    global last_sw1
    last_sw1 = Cnt.sw1
    Cnt.sw1 = lr_dir.value()
    if last_sw1 and not Cnt.sw1:
        dr.value(dr.value() ^ 1)


def key_run():
    global last_sw2
    last_sw2 = Cnt.sw2
    Cnt.sw2 = run.value()
    if last_sw2 and not Cnt.sw2:
        toggle_led()


def key_mode():
    global last_sw3
    last_sw3 = Cnt.sw3
    Cnt.sw3 = mode.value()
    if last_sw3 and not Cnt.sw3:
        Cnt.ms_mode += 1
        if Cnt.ms_mode == 1:
            ms1.on()
            ms2.on()
        elif Cnt.ms_mode == 2:
            ms1.on()
            ms2.off()
        elif Cnt.ms_mode == 3:
            ms1.off()
            ms2.on()
        else:
            ms1.off()
            ms2.off()
            Cnt.ms_mode = 0


while True:
    f = 500 + ((int(adc.read() / 100)) * 80)
    pwm.freq(f)
    key_dir()
    key_run()
    key_mode()
    sleep(0.01)
