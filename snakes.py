import curses
import random
import string

class Snake:

    def __init__(self, srow, scol, dir, color, size, fill, ai):
        self.body = [[fill,0,0] for i in range(size)]
        self.body[0][1] = srow
        self.body[0][2] = scol
        self.color = color
        self.fill = fill
        self.direction = dir
        self.ai = ai
        self.needgrow = 0
        self.collision = 0

    def reset(self):
    

    def death(self):


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

def key_pressed(char, dir):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W"): return 
    elif char == ord("a") or char == ord("A"): return 
    elif char == ord("s") or char == ord("S"): return 
    elif char == ord("d") or char == ord("D"): return 

def food_spawn():
    return ["%",random.randint(1,rows),random.randint(1,cols)]

screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(0)
screen.nodelay(1)
screen.erase()

SNAKE_NUMBER = 6

presskey = -2
direction = random.choice(list(dir.values()))
food = food_spawn()
snakes = [Snake(random.randint(1,rows),random.randint(1,cols),random.choice(list(dir.values())),1,30,random.choice(string.ascii_uppercase),1) for i in range(SNAKE_NUMBER)]

rows, cols = screen.getmaxyx()

dir = {"U":0,"L":1,"D":2,"R":3}

presskey = -1
food = []
snakes = []
direction = 0

game_start()

while presskey != 0:

    presskey = key_pressed(screen.getch(), direction)
    
    for i in range(0,len(snakes)-1):
        snakes[i].move(snakes[i].direction)
    
    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()