import machine
from esp8266_i2c_lcd import I2cLcd
from machine import Timer

DEFAULT_I2C_ADDR = 0x27
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

x_axis = machine.ADC(machine.Pin(33))
x_axis.atten(machine.ADC.ATTN_11DB)
x_axis.width(machine.ADC.WIDTH_9BIT)

state = 0
def check_state():
    global state
    if x_axis.read() > 500:
        state = 1
    elif x_axis.read() < 100:
        state = -1
    else:
        state = 0
    print(state)




    
    
