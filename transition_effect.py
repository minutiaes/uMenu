import machine
import time
from esp8266_i2c_lcd import I2cLcd
from db2 import deBounce

DEFAULT_I2C_ADDR = 0x27

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

x_axis = machine.ADC(machine.Pin(32))
x_axis.atten(machine.ADC.ATTN_11DB)
x_axis.width(machine.ADC.WIDTH_9BIT)

y_axis = machine.ADC(machine.Pin(33))
y_axis.atten(machine.ADC.ATTN_11DB)
y_axis.width(machine.ADC.WIDTH_9BIT)

menu_1 = "     menu1      "
menu_1_1 = "    menu1_1     "
menu_2 = "     menu2      "
menu_2_2 = "    menu2_1     "


lcd.move_to(0, 0)
lcd.putstr(menu_1)
lcd.move_to(0, 1)
lcd.putstr(menu_1_1)

for i in range(16):
    lcd.move_to(0, 0)
    lcd.putstr(menu_1[i:15]+menu_2[:i+1])
    lcd.move_to(0, 1)
    lcd.putstr(menu_1_1[i:15]+menu_2_2[:i+1])
    time.sleep(0.05)
    


