from edgeDetector import edgeDetector

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
        
    def _action(self):
        pass
    def set_action(self, func):
        self._action = func
            
        

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
    _focus_dir = 0 # l-r: 0, u:1, d:2, comeback from action: -1
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
            uMenu.writer(0, 0, txt)
            if(self.down is not None):
                uMenu.writer(0, 1, self.down.menu.text)
            else:
                uMenu.writer(0, 1, " "*16)
            State._focus_line = 0
        elif State._focus_line == 1 and State._focus_dir == 0: # at 1, l-r
            if self.left is not None:
                txt = "<" + txt[1:]
            if self.right is not None:
                txt = txt[:-1] + ">"
            uMenu.writer(0, 1, txt)
            State._focus_line = 1
        elif State._focus_line == 0 and State._focus_dir == 2: # at 0, d
            uMenu.writer(0, 0, " ")
            uMenu.writer(15, 0, " ")
            if self.right is not None:
                uMenu.writer(15, 1, ">")
            State._focus_line = 1
        elif State._focus_line == 1 and State._focus_dir == 1: # at 1, u
            uMenu.writer(0, 1, " ")
            uMenu.writer(15, 1, " ")
            if self.right is not None:
                uMenu.writer(15, 0, ">")
            if self.left is not None:
                uMenu.writer(0, 0, "<")
            State._focus_line = 0
        elif State._focus_line == 0 and State._focus_dir == 1: # at 0, u
            if self.left is not None:
                txt = "<" + txt[1:]
            if self.right is not None:
                txt = txt[:-1] + ">"
            uMenu.writer(0, 1, txt)
            if(self.up is not None):
                uMenu.writer(0, 0, self.up.menu.text)
            else:
                uMenu.writer(0, 0, " "*16)
            State._focus_line = 1
        elif State._focus_dir == -1: #cb from action
            uMenu.writer(0, State._focus_line, self.menu.text)
            if (State._focus_line == 0):
                if self.down is not None:
                    uMenu.writer(0, 1, self.down.menu.text)
            elif(State._focus_line == 1):
                uMenu.writer(0, 0, self.up.menu.text)
            
            
    def _state_transition(self):
        self._printer()
        next_state = self._check_input()
        next_state._state_transition()


    def _action(self):
        self.menu._action()
        self._state_transition() 

    def _check_input(self):
        while True:
            if State._l_key() <= State._l_val and self.left is not None:
                ed.set_cond(State._l_key, State._l_val)
                if ed.check_r() == 1:
                    State._focus_dir = 0
                    return self.left
            if State._r_key() >= State._r_val and self.right is not None:
                ed.set_cond(State._r_key, State._r_val)
                if ed.check_f() == 1:
                    State._focus_dir = 0
                    return self.right
            elif State._u_key() <= State._u_val and self.up is not None:
                ed.set_cond(State._u_key, State._u_val)
                ed.check_r()
                if ed.check_r()== 1:
                    State._focus_dir = 1
                    return self.up
            elif State._d_key() >= State._d_val and self.down is not None:
                ed.set_cond(State._d_key, State._d_val)
                if ed.check_f() == 1:
                    State._focus_dir = 2
                    return self.down
            elif State._s_key() == State._s_val:
                ed.set_cond(State._s_key, State._s_val)
                if ed.check_sw_r() == 1:
                    State._focus_dir = -1
                    self._action()
                

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
    
    def writer(cls):
        print('use "set_text_writer" method')
    
    def set_text_writer(cls, func_move, func_write):
        def text_writer(x, y, text):
            func_move(x, y)
            func_write(text)
        uMenu.writer = text_writer
        
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
        uMenu.states[0]._state_transition()

    
ed = edgeDetector()

