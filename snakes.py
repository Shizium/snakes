import curses
import random
import string

class Snake:

    def __init__(self, srow=None, scol=None, direction=None, color=None, size=None, fill=None, ai=None, window=None):
        self.size = self.size = size if size is not None else random.randint(2,20)
        self.direction = self.direction = direction if direction is not None else random.choice(list(dirdict.values()))
        self.color = color if color is not None else 1
        self.fill = fill if fill is not None else random.choice(string.ascii_uppercase)
        self.ai = ai if ai is not None else 0
        self.window = window if window is not None else screen
        self.collision = 0
        self.needgrow = 0
        self.score = 0
        self.reset(srow if srow is not None else None, scol if scol is not None else None)

    def reset(self,srow=None,scol=None):
        brows, bcols = self.window.getbegyx()
        frows, fcols = self.window.getmaxyx()
        frows = frows - 1
        fcols = fcols - 1
        self.body = [[self.fill,0,0] for i in range(self.size)]
        self.body[0][1] = srow if srow is not None else random.randint(brows,frows)
        self.body[0][2] = scol if scol is not None else random.randint(bcols,fcols)
        self.collision = 0

    def death(self):
        self.score -= 100
        for i in range(0,len(self.body)-1):
            self.window.addch(self.body[i][1], self.body[i][2], " ")
        self.reset()

    def move(self):
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

        brows, bcols = self.window.getbegyx()
        frows, fcols = self.window.getmaxyx()
        frows = frows - 1
        fcols = fcols - 1

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
            self.score += 1
            if not self.needgrow:
                self.score += 10
                self.body.pop(len(self.body) - 1)
                self.window.addch(self.body[-1][1], self.body[-1][2], " ")
            else:
                self.needgrow = 0
        else:
           self.death()

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
    
    def __init__(self, price=None, view=None, window=None):
        self.price = price if price is not None else 10
        self.view = view if view is not None else random.choice(string.punctuation)
        self.window = window if window is not None else screen
        self.row = 0
        self.col = 0

    def spawn(self):
        brows, bcols = self.window.getbegyx()
        frows, fcols = self.window.getmaxyx()
        frows = frows - 1
        fcols = fcols - 1
        
        while True:
            self.row = random.randint(brows,frows)
            self.col = random.randint(bcols,fcols)
            attrs = self.window.inch(self.row,self.col)
            ch = chr(attrs & 0xFF)
            if ch == " ":
                break
        
        self.window.addch(self.row, self.col, self.view)

def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
    elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
    elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
    elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

#Constant
SNAKE_NUMBER = 6

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
gameboard = curses.newwin(30,90,0,0)
gameboard.nodelay(True)
scoreboard = curses.newwin(20,30,0,93)
scoreboard.box(curses.A_VERTICAL,curses.A_HORIZONTAL)
scoreboard.addstr(0,9,"SCORE BOARD:")
scoreboard.refresh()

#Object defined
food = Food()
snakes = snakes = [Snake(None,None,None,None,None,None,1,gameboard) for i in range(SNAKE_NUMBER)]

while presskey != -1:

    presskey = key_pressed(gameboard.getch())
    
    for i in range(0,len(snakes)-1):
        snakes[i].move()
        scoreboard.addstr (2+i, 2, "===[ " + snakes[i].fill + " - " + str(snakes[i].score) + " ]===" )


    gameboard.box(curses.A_VERTICAL,curses.A_HORIZONTAL)
    gameboard.addstr(0,35,"WANNA PLAY WITH SNAKES?")
    scoreboard.refresh()

    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()