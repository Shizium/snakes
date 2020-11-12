import curses
import random
import string

class Snake:

    def __init__(self, foods, board=None, ai=0, srow=None, scol=None, direction=None, color=1, size=None, fill=None):
        self.size = size if size is not None  else random.randint(2,20)
        self.fill = fill if fill is not None else random.choice(string.ascii_uppercase)
        self.direction = direction if direction is not None  else random.choice(list(dirdict.values()))
        self.color = color
        self.ai = ai
        self.board = board if board is not None else screen
        self.foods = foods
        self.collision = 0
        self.needgrow = 0
        self.score = 0
        self.reset(srow,scol)

    def reset(self,srow=None,scol=None):
        self.body = [[self.fill,0,0] for i in range(self.size)]
        self.body[0][1] = srow if srow is not None else random.randint(self.board.miny,self.board.maxy - 1)
        self.body[0][2] = scol if scol is not None else random.randint(self.board.minx,self.board.maxx - 1)
        self.collision = 0

    def death(self):
        self.score -= 100
        for i in range(0,len(self.body)-1):
            self.board.drawch(self.body[i][1], self.body[i][2], " ")
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

        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            row += 1
            if row >= self.board.maxy -1:
                row = self.board.miny
        elif self.direction == 2:
            row -= 1
            if row <= self.board.miny:
                row = self.board.maxy
        elif self.direction == 1:
            col -= 1
            if col <= self.board.minx:
                col = self.board.maxx
        elif self.direction == 3:
            col += 1
            if col >= self.board.maxx - 1:
                col = self.board.minx

        #Проверяет нет ли коллизии
        if self.check_collision(row,col) == 0 and self.collision != 1:
            self.body.insert(0, [self.fill,row,col])
            self.board.drawch(row, col, self.body[0][0])
            self.score += 1
            self.catchfood(row,col)
            if not self.needgrow:
                self.body.pop(len(self.body) - 1)
                self.board.drawch(self.body[-1][1], self.body[-1][2], " ")
            else:
                self.needgrow = 0
        else:
           self.death()

    def check_collision(self,row,col):
        if self.board.checkchar(row,col) in list(string.ascii_uppercase):
            return 1
        else:
            return 0
    
    def catchfood(self,row,col):
        for i in range(0,len(self.foods)-1):
            if self.body[0][1] == self.foods[i].row and self.body[0][2] == self.foods[i].col:
                self.needgrow = 1
                self.score += 10
                self.foods[i].spawn()

class Food:
    
    def __init__(self, board=None, view=None, price=None):
        self.price = price if price is not None else 10
        self.view = view if view is not None else random.choice(string.punctuation)
        self.board = board if board is not None else screen
        self.row = 0
        self.col = 0
        self.spawn()

    def spawn(self):
        while True:
            self.row = random.randint(self.board.miny,self.board.maxy - 1)
            self.col = random.randint(self.board.minx,self.board.maxx - 1)
            if self.board.checkchar(self.row,self.col) == " ":
                break
    
    def draw(self):
        self.board.drawch(self.row, self.col, self.view)

class Board:

    def __init__(self,rows,cols,srow,scol):
        self.board = curses.newwin(rows,cols,srow,scol)
        self.miny, self.minx = self.board.getbegyx()
        self.maxy, self.maxx = self.board.getmaxyx()
    
    def drawwin(self):
        self.board.box(curses.A_VERTICAL,curses.A_HORIZONTAL)

    def drawch(self,row,col,ch=" ",color=1):
        self.board.addch(row, col, ch)

    def drawstr(self,row,col,st=" ",color=1):
        self.board.addstr(row, col, st)
    
    def refresh(self):
        self.board.refresh()

    def checkchar(self,row,col):
        return chr((self.board.inch(row,col)) & 0xFF)

def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
    elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
    elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
    elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

#Constant
SNAKE_NUMBER = 1
FOOD_NUMBER = 6

#Init values
dirdict = {"U":0,"L":1,"D":2,"R":3}
presskey = 0

screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(0)
screen.nodelay(True)
screen.erase()

#Create window
gameboard = Board(30,90,0,0)
scoreboard = Board(20,30,0,93)

scoreboard.drawwin()
scoreboard.drawstr(0,9,"SCORE BOARD:")

#Object defined
foods = [Food(gameboard) for i in range(int(FOOD_NUMBER+1))]
snakes = [Snake(foods,gameboard,1) for i in range(int(SNAKE_NUMBER+1))]

while presskey != -1:

    presskey = key_pressed(screen.getch())
    
    for i in range(0,len(foods)-1):
        foods[i].draw()

    for i in range(0,len(snakes)-1):
        snakes[i].move()
        scoreboard.drawstr(2+i, 2, "===[ " + snakes[i].fill + " => " + str(snakes[i].score) + " ]===" )

    gameboard.drawwin()
    gameboard.drawstr(0,35,"WANNA PLAY WITH SNAKES?")
    gameboard.refresh()
    scoreboard.refresh()

    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()