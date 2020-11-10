import curses
import random
import string

class Snake:

    def __init__(self, srow=None, scol=None, direction=None, color=None, size=None, fill=None, ai=None):
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
        
        if srow is not None: self.body[0][1] = srow
        else: self.body[0][1] = random.randint(1,rows)
        
        if scol is not None: self.body[0][2] = scol
        else: self.body[0][2] = random.randint(1,cols)
        
        self.needgrow = 0
        self.collision = 0

    #def reset(self):

    #def death(self):

    def move(self, dir):
        row = self.body[0][1]
        col = self.body[0][2]

        #Если установлен флаг автоматического управлений движением змейки
        if self.ai == 1:
            #10% на случайный поворот
            if random.randint(1,100) <= 10:
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
            
        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            row += 1
            if row >= rows:
                row = 1
        elif self.direction == 2:
            row -= 1
            if row <= 0:
                row = rows - 1
        elif self.direction == 1:
            col -= 1
            if col < 1:
                col = cols - 1
        elif self.direction == 3:
            col += 1
            if col >= cols:
                col = 1
    
        #Проверяет нет ли коллизии
        if self.check_collision(row,col) == 0 and self.collision != 1:
            self.body.insert(0, [self.fill,row,col])
            screen.addch(row, col, self.body[0][0])
            if not self.needgrow:
                self.body.pop(len(self.body) - 1)
                screen.addch(self.body[-1][1], self.body[-1][2], " ")
            else:
                self.needgrow = 0
        else:
            self.collision = 1

    def check_collision(self,row,col):
        attrs = screen.inch(row,col)
        ch = chr(attrs & 0xFF)
        if ch in list(string.ascii_uppercase):
            return 1
        else:
            return 0
    
    def catchfood(self,frow,fcol):
        if self.body[0][1] == frow and self.body[0][2] == fcol:
            self.needgrow = 1
            return 1
        else:
            return 0

def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W"): return 0
    elif char == ord("a") or char == ord("A"): return 1
    elif char == ord("s") or char == ord("S"): return 2
    elif char == ord("d") or char == ord("D"): return 3

def food_spawn():
    return ["%",random.randint(1,rows),random.randint(1,cols)]

screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(0)
screen.nodelay(1)
screen.erase()

SNAKE_NUMBER = 6

rows,cols = screen.getmaxyx()
presskey = -2
food = food_spawn()
dirdict = {"U":0,"L":1,"D":2,"R":3}
presskey = 0
food = []
snakes = []

snakes = [Snake(1) for i in range(SNAKE_NUMBER)]

while presskey != -1:

    presskey = key_pressed(screen.getch())
    
    for i in range(0,len(snakes)-1):
        snakes[i].move(snakes[i].direction)
    
    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()