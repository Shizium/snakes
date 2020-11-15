import curses
import random
import string

class Snake:

    def __init__(self, foods, board=None, ai=0, srow=None, scol=None, direction=None, color=1, size=5, fill=None):
        self.size = size
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
        self.target = None #Переменная для хранения ближайшей еды

    def reset(self,srow=None,scol=None):
        self.body = [[0,0] for i in range(self.size)]
        self.body[0][0] = srow if srow is not None else random.randint(self.board.miny,self.board.maxy - 1)
        self.body[0][1] = scol if scol is not None else random.randint(self.board.minx,self.board.maxx - 1)
        self.collision = 0

    def death(self):
        self.score -= 100
        for i in range(len(self.body)-1):
            self.board.drawch(self.body[i][0], self.body[i][1], " ")
        self.reset()

    def move(self):
        row = self.body[0][0]
        col = self.body[0][1]

        #Если установлен флаг автоматического управлений движением змейки
        if self.ai == 1:
            #Проверяем где самая ближняя еда по направлению
            #Только если у нас нет текущей цели еды, к которой мы встретимся или еду уже съели
            if (self.target == None) or (self.board.checkch(self.target[0],self.target[1]) not in string.punctuation):
                    i = random.randint(0,len(self.foods)-1)
                    self.target = [0,0]
                    self.target[0] = self.foods[i].row
                    self.target[1] = self.foods[i].col

            #Простейший интеллект
            #Если вертикаль не совпадает, то если движется по горизонтали, то меняем направление на движение по вертикали
            #в зависимости где ближе: сверху или снизу
            if self.body[0][0] != self.target[0]:
                if self.direction == 1 or self.direction == 3:
                    self.direction = 0 if self.body[0][0] > self.target[0] else 2
            #Если горизонталь не совпадает, то если движется по вертикали, то меняем направление на движение по горизонтали
            #в зависимости где ближе: справа или слева
            elif self.body[0][1] != self.target[1]:
                if self.direction == 0 or self.direction == 2:
                    self.direction = 1 if self.body[0][1] > self.target[1] else 3

        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            row += 1
            if row >= self.board.maxy - 1:
                row = self.board.miny 
        elif self.direction == 2:
            row -= 1
            if row <= self.board.miny:
                row = self.board.maxy - 1 
        elif self.direction == 1:
            col -= 1
            if col <= self.board.minx:
                col = self.board.maxx - 1
        elif self.direction == 3:
            col += 1
            if col >= self.board.maxx - 1:
                col = self.board.minx

        #Проверяет нет ли коллизии
        if self.collision != 1:
            self.body.insert(0, [row,col])
            self.board.drawch(row, col, self.fill)
            if not self.needgrow:
                self.body.pop(len(self.body) - 1)
                self.board.drawch(self.body[-1][0], self.body[-1][1], " ")
            else:
                self.needgrow = 0
        else:
           self.death()
    
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
            if self.board.checkch(self.row,self.col) == " ":
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

    def checkch(self,row,col):
        return chr((self.board.inch(row,col)) & 0xFF)
    

class LevelManager:

    def __init__(self,snakecount, foodcount):
        self.snakecount = int (snakecount + 1)
        self.foodcount = int (foodcount + 1)
        self.foods = [Food(gameboard) for i in range(self.foodcount)]
        self.snakes = [Snake(self.foods,gameboard,1) for i in range(self.snakecount)]
    
    def check_collision(self):
        for i in range(self.snakecount-1):
            for j in range(self.snakecount-1):
                if self.snakes[i].body[0] in self.snakes[j].body and self.snakes[i].fill != self.snakes[j].fill:
                    self.snakes[i].collision = 1

    def catch_food(self):
        for i in range(self.snakecount-1):
            for j in range(self.foodcount-1):
                if self.snakes[i].body[0][0] == self.foods[j].row and self.snakes[i].body[0][1] == self.foods[j].col:
                    self.snakes[i].needgrow = 1
                    self.snakes[i].score += 10
                    self.snakes[i].target = None
                    self.foods[j].spawn()
    
    def gamemove(self, gboard, sboard):
        for i in range(self.foodcount-1):
            self.foods[i].draw()

        for i in range(self.snakecount-1):
            self.snakes[i].move()
            self.check_collision()
            self.catch_food()
            sboard.drawstr(2+i, 2, "===[ " + self.snakes[i].fill + " => " + str(self.snakes[i].score) + " ]===" )
        
        sboard.refresh()

        gboard.drawwin()
        gboard.drawstr(0,35,"WANNA PLAY WITH SNAKES?")
        gboard.refresh()

                
def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
    elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
    elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
    elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

#Constant
SNAKE_NUMBER = 5
FOOD_NUMBER = 10

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

level = LevelManager(SNAKE_NUMBER, FOOD_NUMBER)

while presskey != -1:

    presskey = key_pressed(screen.getch())
    
    level.gamemove(gameboard, scoreboard)

    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()