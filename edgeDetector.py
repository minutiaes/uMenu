from machine import Timer


class edgeDetector():
    def __init__(self):
        self.reader = None
        self.val = None
        
        self.tim0 = Timer(0)
        self.prv_state = 0
        self.state = 0
        self.status = " "
        # "r": rising / "f": falling / "h": hold / "dc": don't care
        self.fired = 0
        
    def set_cond(self, btn_rdr, con):
        self.reader = btn_rdr
        self.val = con
        
    def tim_callback_f(self, tim):
        if self.state > self.val and self.prv_state == 1:
            self.status = "h"
            self.prv_state = 1
            self.set_timer_f()
        elif self.state > self.val and self.prv_state == 0:
            self.status = "r"
            self.prv_state = 1
            self.set_timer_f()
        elif self.state < self.val and self.prv_state == 1:
            self.status = "f"
            self.prv_state = 0
        else:
            self.status = "dc"
            self.prv_state = 0
#         print(self.status)
#         print("-------")
        self.fired = 0
        return self.status
    
    def tim_callback_r(self, tim):
        if self.state < self.val and self.prv_state == 1:
            self.status = "h"
            self.prv_state = 1
            self.set_timer_r()
        elif self.state < self.val and self.prv_state == 0:
            self.status = "f"
            self.prv_state = 1
            self.set_timer_r()
        elif self.state > self.val and self.prv_state == 1:
            self.status = "r"
            self.prv_state = 0
        else:
            self.status = "dc"
            self.prv_state = 0
#         print(self.status)
#         print("-------")
        self.fired = 0
        return self.status
    
    def tim_callback_sw_r(self, tim):
        if self.state == self.val and self.prv_state == 1:
            self.status = "h"
            self.prv_state = 1
            self.set_timer_sw_r()
        elif self.state == self.val and self.prv_state == 0:
            self.status = "f"
            self.prv_state = 1
            self.set_timer_sw_r()
        elif self.state == (not self.val) and self.prv_state == 1:
            self.status = "r"
            self.prv_state = 0
        else:
            self.status = "dc"
            self.prv_state = 0
#         print(self.status)
#         print(self.state)
#         print(self.prv_state)
#         print("-------")
        self.fired = 0
        return self.status
        
    def check_f(self):
        self.prv_state = 0
        while True:
            self.state = self.reader()
            if self.state > 500 and self.fired == 0:
                self.fired = 1
                self.status = "r"
                self.set_timer_f()
            if self.status == "f":
                return 1
            
    def check_r(self):
        self.prv_state = 0
        while True:
            self.state = self.reader()
            if self.state < 200 and self.fired == 0:
                self.fired = 1
                self.status = "f"
                self.set_timer_r()
            if self.status == "r":
                return 1
        
    def check_sw_r(self):
        self.prv_state = 0
        while True:
            self.state = self.reader()
            if self.state == 0 and self.fired == 0:
                self.fired = 1
                self.status = "f"
                self.set_timer_sw_r()
            if self.status == "r":
                return 1
            
    def set_timer_f(self):
        self.tim0.init(period=100, mode=Timer.ONE_SHOT, callback=self.tim_callback_f)
    def set_timer_r(self):
        self.tim0.init(period=100, mode=Timer.ONE_SHOT, callback=self.tim_callback_r)
    def set_timer_sw_r(self):
        self.tim0.init(period=100, mode=Timer.ONE_SHOT, callback=self.tim_callback_sw_r)    
        

if __name__ == "__main__":
    import machine
    from esp8266_i2c_lcd import I2cLcd
    
    DEFAULT_I2C_ADDR = 0x27
    i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    x_axis = machine.ADC(machine.Pin(33))
    x_axis.atten(machine.ADC.ATTN_11DB)
    x_axis.width(machine.ADC.WIDTH_9BIT)
    
    ed = edgeDetector()
    ed.reader = x_axis.read
    ed.val = 500
    ed.check_state()

