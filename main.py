import machine
from esp8266_i2c_lcd import I2cLcd
from uMenu import MenuElement, uMenu

# 2x16 LCD setup 
DEFAULT_I2C_ADDR = 0x27
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# joystick setup
# x-axis for moving left and right
x_axis = machine.ADC(machine.Pin(32))
x_axis.atten(machine.ADC.ATTN_11DB)
x_axis.width(machine.ADC.WIDTH_9BIT)

# y-axis for moving up and down
y_axis = machine.ADC(machine.Pin(33))
y_axis.atten(machine.ADC.ATTN_11DB)
y_axis.width(machine.ADC.WIDTH_9BIT)

# joystick button for selection
p5 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

# built-in led for demo
led=machine.Pin(2,machine.Pin.OUT)


# MenuElement instances represent menu items        
my_element1 = MenuElement("menu1")
# my_element1.set_action(toggle_led) # an alternative to decorator
my_element2 = MenuElement("menu2")
my_element3 = MenuElement("menu3")
my_element1_1 = MenuElement("menu1_1")
my_element1_1_1 = MenuElement("menu1_1_1")
my_element1_1_2 = MenuElement("menu1_1_2")
my_element1_2 = MenuElement("menu1_2")
my_element3_1 = MenuElement("menu3_1")
my_element3_2 = MenuElement("menu3_2")

# uMenu is a state machine which controls the flow of menu according to user input
my_menu = uMenu()

# lcd functions and joystick setup are specified
my_menu.set_text_writer(lcd.move_to, lcd.putstr)
my_menu.set_controls(r_key = x_axis.read, r_val = 500,
                     l_key = x_axis.read, l_val = 200,
                     u_key = y_axis.read, u_val = 200,
                     d_key = y_axis.read, d_val = 500,
                     s_key = p5.value,    s_val = 0)

# construction of menu 
menu1 = my_menu.add_menu(my_element1)
menu1_1 = my_menu.add_childmenu(my_element1_1, menu1)
menu1_1_1 = my_menu.add_childmenu(my_element1_1_1, menu1_1)
menu1_1_2 = my_menu.add_childmenu(my_element1_1_2, menu1_1)
my_menu.add_childmenu(my_element1_2, menu1)
menu2 = my_menu.add_menu(my_element2)
menu3 = my_menu.add_menu(my_element3)
my_menu.add_childmenu(my_element3_1, menu3)
my_menu.add_childmenu(my_element3_2, menu3)

# toggle_led function is called, if joystick button is pushed, when menu focus is on my_element1
@my_element1.set_action
def toggle_led():
    if led.value() == 0:
        led.value(1)
    else:
        led.value(0)

# starts state machine
my_menu.run_uMenu()
    
