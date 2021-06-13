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


class Date():
    r_key = x_axis.read
    r_val = 500
    l_key = x_axis.read
    l_val = 200
    u_key = y_axis.read
    u_val = 200
    d_key = y_axis.read
    d_val = 500
    def __init__(self, txt, x=3, y=1, d=None, m=None, yr=None):
        self.text = txt
        self._x = x
        self._y = y
        self.x = x
        self.y = y
        if d is not None:
            self.d = d
            self.date = d+"."
        else:
            self.d = "00"
            self.date = "DD."
        if m is not None:
            self.m = m
            self.date = self.date+m+"."
        else:
            self.m = "00"
            self.date = self.date+"MM."
        if yr is not None:
            self.yr = yr
            self.date = self.date+yr
        else:
            self.yr = "0000"
            self.date = self.date+"YYYY"

        self._prep_disp()
    def _prep_disp(self):
        lcd.move_to(0, 0)
        lcd.putstr(self.text)
        lcd.move_to(self._x, self._y)
        lcd.putstr(self.date)
        lcd.move_to(self._x, self._y)
        lcd.show_cursor()
#         lcd.blink_cursor_on()
        self._set_date()
    def _set_date(self):
        lim_x_l = self._x
        lim_x_r = self._x+9
        while True:
            if Date.l_key() <= Date.l_val and self.x > lim_x_l is not None:
                db.reader = Date.l_key
                db.val = Date.l_val
                db.check_r()
                if db.status == "r":
                    if self.x == self._x+3 or self.x == self._x+6: 
                        self.x -= 2
                    else:
                        self.x -= 1
                    lcd.move_to(self.x, self.y)     
            elif Date.r_key() >= Date.r_val and self.x < lim_x_r is not None:
                db.reader = Date.r_key
                db.val = Date.r_val
                db.check_f()
                if db.status == "f":
                    if self.x == self._x+1 or self.x == self._x+4: 
                        self.x += 2
                    else:
                        self.x += 1
                    lcd.move_to(self.x, self.y)
            elif Date.u_key() <= Date.u_val:
                db.reader = Date.u_key
                db.val = Date.u_val
                db.check_r()
                if db.status == "r":
                    ind = self.x - self._x
                    char = self.date[ind]
                    if ind<2: #DD
                        pass
                    elif ind<5: #MM
                        pass
                    elif ind>5: #YYYY
                        pass
#                     if char == "D" or char == "M" or char == "Y":
#                         
#                         lcd.putstr("0")
#                         lcd.move_to(self.x, self.y)
#                     else:
                        
                        

db = deBounce()
date = Date("asdf")
        
    
    




