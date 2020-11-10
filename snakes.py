import curses
import random
import string

class Snake:

    def __init__(self, srow=None, scol=None, direction=None, color=None, size=None, fill=None, ai=None, window=None):
        if size is not None: self.size = size
        else: self.size = random.randint(2,20)
        if direction is not None: self.direction = dir
        else: self.direction = random.choice(list(dirdict.values()))
        if color is not None: self.color = color 
        else: self.color = 1
        if fill is not None: self.fill = fill
        else: self.fill = random.choice(string.ascii_uppercase)
        if ai is not None: self.ai = ai
        else: self.ai = 0
        self.body = [[self.fill,0,0] for i in range(self.size)]
        if window is not None: self.window = window
        else: self.window = screen
        brows, bcols = self.window.getbegyx()
        frows, fcols = self.window.getmaxyx()
        if srow is not None: self.body[0][1] = srow
        else: self.body[0][1] = random.randint(brows+1,frows-1)
        if scol is not None: self.body[0][2] = scol
        else: self.body[0][2] = random.randint(bcols+1,fcols-1)
        self.needgrow = 0
        self.collision = 0
        self.score = 0

    #def reset(self):

    #def death(self):

    def move(self, dir):
        row = self.body[0][1]
        col = self.body[0][2]

        #Если установлен флаг автоматического управлений движением змейки
        if self.ai == 1:
            #10% на случайный поворот
            if random.randint(1,100) <= 20:
                #Если двигались по вертикали
                if self.direction % 2 == 0:
                    #Поворачиваемся по горизонтали (вправо или влево)
                    self.direction = random.choice([1,3])
                else:
                    #Иначе поворачиваемся по вертикали (вверх или вниз)
                    self.direction = random.choice([0,2])
        #Если ручное управление
        else:
            self.direction = dir   

        brows, bcols = self.window.getmaxyx()
        brows, bcols = brows + 1, bcols + 1
        frows, fcols = self.window.getmaxyx()
        frows, fcols = frows - 1, fcols - 1

        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            row += 1
            if row >= frows:
                row = brows
        elif self.direction == 2:
            row -= 1
            if row <= brows:
                row = frows
        elif self.direction == 1:
            col -= 1
            if col <= bcols:
                col = fcols
        elif self.direction == 3:
            col += 1
            if col >= fcols:
                col = bcols

        #Проверяет нет ли коллизии
        if self.check_collision(row,col) == 0 and self.collision != 1:
            self.body.insert(0, [self.fill,row,col])
            self.window.addch(row, col, self.body[0][0])
            if not self.needgrow:
                self.body.pop(len(self.body) - 1)
                self.window.addch(self.body[-1][1], self.body[-1][2], " ")
            else:
                self.needgrow = 0
        else:
            self.collision = 1

    def check_collision(self,row,col):
        attrs = self.window.inch(row,col)
        ch = chr(attrs & 0xFF)
        if ch in list(string.ascii_uppercase):
            return 1
        else:
            return 0
    
    def catchfood(self,row,col):
        if self.body[0][1] == row and self.body[0][2] == col:
            self.needgrow = 1
            return 1
        else:
            return 0

class Food:
    
    def __init__(self, row=None, col=None, price=None, view=None):
        if price is not None: self.price = price
        else: self.price = 10
        if view is not None: self.view = random.choice(string.punctuation)
        else: self.view = view
        if row is not None: self.row = 0
        else: self.row  = row
        if col is not None: self.col = 0
        else: self.col  = col

    def spawn():
        while True:
            self.row = random.randint(1,curses.LINES)
            self.col = random.randint(1,curses.COLS)
            attrs = screen.inch(row,col)
            ch = chr(attrs & 0xFF)
            if ch == " ":
                break
             
        screen.addch(self.row, self.col, self.view)

def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
    elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
    elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
    elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

#Constant
SNAKE_NUMBER = 3

#Init values
dirdict = {"U":0,"L":1,"D":2,"R":3}
presskey = 0

#Curse init
screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(0)
screen.erase()

#Create window
gameboard = curses.newwin(30,90,0,3)
gameboard.nodelay(True)
gameboard.box("|","=")
gameboard.addstr(0,30,"WANNA PLAY WITH SNAKES?")
gameboard.refresh()

scoreboard = curses.newwin(20,30,0,93)
scoreboard.box("|","=")
scoreboard.addstr(0,10,"SCORE BOARD:")
scoreboard.refresh()

#Object defined
food = Food()
snakes = snakes = [Snake(None,None,None,None,None,None,1,gameboard) for i in range(SNAKE_NUMBER+1)]

while presskey != -1:

    presskey = key_pressed(gameboard.getch())
    
    for i in range(0,len(snakes)-1):
        snakes[i].move(snakes[i].direction)
    
    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()