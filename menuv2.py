import machine
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

class MenuElement():
    def __init__(self, txt):
        self.text = MenuElement.align_center(txt)
    
    @staticmethod
    def align_center(txt):
        l = len(txt)
        if l%2 == 0:
            return int((16 - l)/2)*" "+txt+int((16 - l)/2)*" "
        else:
            return (int((16 - l+1)/2))*" "+txt+(int((16 - l-1)/2))*" "
            
        

class State():
    _r_key = None
    _r_val = None
    _l_key = None
    _l_val = None
    _u_key = None
    _u_val = None
    _d_key = None
    _d_val = None
    _s_key = None
    _s_val = None
    
    _focus_line = 0
    _focus_dir = 0 # l-r: 0, u:1, d:2
    def __init__(self, menu: MenuElement, left = None, right = None, down = None, up = None, push = None):
        self.left = left
        self.right = right
        self.down = down
        self.up = up
        self.push = push

        self.menu = menu

        self.last_childstate = None
        self._set_transition()
        
    def _set_transition(self):
        if self.left is not None:
            self.left.right = self
        if self.right is not None:
            self.right.left = self
        if self.down is not None:
            self.down.up = self
        if self.up is not None:
            self.up.down = self
            self.up.last_childstate = self
            

    def _printer(self):
        print(self.menu.text)
        txt = self.menu.text
        if (State._focus_line == 0 and State._focus_dir == 0) or (State._focus_line == 1 and State._focus_dir == 2): # at 0, l-r OR at 1, d
            if self.left is not None:
                txt = "<" + txt[1:]
            if self.right is not None:
                txt = txt[:-1] + ">"
            my_menu.writer(0, 0, txt)
            if(self.down is not None):
                my_menu.writer(0, 1, self.down.menu.text)
            else:
                my_menu.writer(0, 1, " "*16)
            State._focus_line = 0
        elif State._focus_line == 1 and State._focus_dir == 0: # at 1, l-r
            if self.left is not None:
                txt = "<" + txt[1:]
            if self.right is not None:
                txt = txt[:-1] + ">"
            my_menu.writer(0, 1, txt)
            State._focus_line = 1
        elif State._focus_line == 0 and State._focus_dir == 2: # at 0, d
            my_menu.writer(0, 0, " ")
            my_menu.writer(15, 0, " ")
            if self.right is not None:
                my_menu.writer(15, 1, ">")
            State._focus_line = 1
        elif State._focus_line == 1 and State._focus_dir == 1: # at 1, u
            my_menu.writer(0, 1, " ")
            my_menu.writer(15, 1, " ")
            if self.right is not None:
                my_menu.writer(15, 0, ">")
            if self.left is not None:
                my_menu.writer(0, 0, "<")
            State._focus_line = 0
        elif State._focus_line == 0 and State._focus_dir == 1: # at 0, u
            if self.left is not None:
                txt = "<" + txt[1:]
            if self.right is not None:
                txt = txt[:-1] + ">"
            my_menu.writer(0, 1, txt)
            if(self.up is not None):
                my_menu.writer(0, 0, self.up.menu.text)
            else:
                my_menu.writer(0, 0, " "*16)
            State._focus_line = 1
            
    def _action(self):
        self._printer()
        next_state = self._transition()
        next_state._action()

    def _transition(self):
        while True:
            if State._l_key() <= State._l_val and self.left is not None:
                db.reader = State._l_key
                db.val = State._l_val
                db.check_r()
                if db.status == "r":
                    db.status == "dc"
                    State._focus_dir = 0
                    return self.left
            if State._r_key() >= State._r_val and self.right is not None:
                db.reader = State._r_key
                db.val = State._r_val
                db.check_f()
                if db.status == "f":
                    db.status == "dc"
                    State._focus_dir = 0
                    return self.right
            elif State._u_key() <= State._u_val and self.up is not None:
                db.reader = State._u_key
                db.val = State._u_val
                db.check_r()
                if db.status == "r":
                    db.status == "dc"
                    State._focus_dir = 1
                    return self.up
            elif State._d_key() >= State._d_val and self.down is not None:
                db.reader = State._d_key
                db.val = State._d_val
                db.check_f()
                if db.status == "f":
                    db.status == "dc"
                    State._focus_dir = 2
                    return self.down

class ChildState(State):
    def __init__(self, menu: MenuElement, left=None, right=None, down=None, up=None, push=None):
        super().__init__(menu, left=left, right=right, down=down, up=up, push=push)
    def _set_transition(self):
        if self.left is not None:
            self.left.right = self
        if self.right is not None:
            self.right.left = self
        if self.down is not None:
            self.down.up = self
        if self.up is not None and self.up.last_childstate is None:
            self.up.down = self
            self.up.last_childstate = self
        elif self.up is not None and self.up.last_childstate is not None:
            self.up.last_childstate.right = self
            self.left = self.up.last_childstate
            self.up.last_childstate = self

class uMenu():
    states = []
    last_state = None
    
    def _init__ (self):
        pass
        
    def writer(self):
        print('use "set_text_writer" methor')
    
    def set_text_writer(cls, func_move, func_write):
        def text_writer(x, y, text):
            func_move(x, y)
            func_write(text)
        cls.writer = text_writer
        
    def set_controls(cls, r_key = None, r_val = None, l_key = None, l_val = None,
                     u_key = None, u_val = None, d_key = None, d_val = None,
                     s_key = None, s_val = None):
        State._r_key = r_key
        State._r_val = r_val
        State._l_key = l_key
        State._l_val = l_val
        State._u_key = u_key
        State._u_val = u_val
        State._d_key = d_key
        State._d_val = d_val
        State._s_key = s_key
        State._s_val = s_val
        
    @staticmethod
    def add_menu(menu: MenuElement):
        if uMenu.last_state is not None:
            x = State(menu, left = uMenu.last_state)
            uMenu.states.append(x)
            uMenu.last_state = x
            return x
        else:
            x = State(menu)
            uMenu.states.append(x)
            uMenu.last_state = x
            return x

    @staticmethod        
    def add_childmenu(menu: MenuElement, parent: State):
        x = ChildState(menu, up=parent)
        uMenu.states.append(x)
        return x

    def run_uMenu(self):
        uMenu.states[0]._action()


db = deBounce()
my_element1 = MenuElement("menu1")
my_element2 = MenuElement("menu2")
my_element3 = MenuElement("menu3")
my_element1_1 = MenuElement("menu1_1")
my_element1_1_1 = MenuElement("menu1_1_1")
my_element1_1_2 = MenuElement("menu1_1_2")
my_element1_2 = MenuElement("menu1_2")
my_element3_1 = MenuElement("menu3_1")
my_element3_2 = MenuElement("menu3_2")

my_menu = uMenu()
my_menu.set_text_writer(lcd.move_to, lcd.putstr)
my_menu.writer(0, 0, "000")

my_menu.set_controls(r_key = x_axis.read, r_val = 500,
                     l_key = x_axis.read, l_val = 200,
                     u_key = y_axis.read, u_val = 200,
                     d_key = y_axis.read, d_val = 500)
menu1 = my_menu.add_menu(my_element1)
menu1_1 = my_menu.add_childmenu(my_element1_1, menu1)
menu1_1_1 = my_menu.add_childmenu(my_element1_1_1, menu1_1)
menu1_1_2 = my_menu.add_childmenu(my_element1_1_2, menu1_1)
my_menu.add_childmenu(my_element1_2, menu1)
menu2 = my_menu.add_menu(my_element2)
menu3 = my_menu.add_menu(my_element3)
my_menu.add_childmenu(my_element3_1, menu3)
my_menu.add_childmenu(my_element3_2, menu3)

my_menu.run_uMenu()