from abc import ABCMeta, abstractmethod
import curses
import random
import string
import pygame
import os
import constants

class Graphics(metaclass=ABCMeta):

    @abstractmethod
    def drawwin(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def checkcell(self,x,y):
        pass

class Input(metaclass=ABCMeta):

    @abstractmethod
    def key_pressed(self):
        pass

class ConsoleInput(Input):

    def __init__(self, screen):
        
        self.screen = screen

    def key_pressed(self):
        
        char = self.screen.getch()
        
        if char == ord("q"): return -1
        elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
        elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
        elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
        elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

class GraphicsInput(Input):

    def __init__(self):
        pass
    
    def key_pressed(self):
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    return 0
                elif i.key == pygame.K_DOWN:
                    return 2
                elif i.key == pygame.K_LEFT:
                    return 1
                elif i.key == pygame.K_RIGHT:
                    return 3
                elif i.key == pygame.K_q:
                    return -1

class TerminalGraphics(Graphics):

    def __init__(self, x, y):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.curs_set(0)
        self.screen.nodelay(True)
        self.screen.erase()

    def drawwin(self, x, y, startx=0, starty=0, label=None):
        win = curses.newwin(y, x, starty, startx)
        self.redrawwin(win, label)
        return win

    def redrawwin(self, win, label=None):
        win.box(curses.A_VERTICAL, curses.A_HORIZONTAL)
        if label != None:
            y, x = win.getmaxyx()
            x = ( (x // 2) - (len(label) // 2) )
            win.addstr(0, x, label)

    def draw(self, win, x, y, fill):
        win.addch(y, x, fill)        
            
    def drawtext(self, win, x, y, st):
        win.addstr(y, x, st)

    def refresh(self, win, x=None, y=None):
        win.refresh()
        curses.napms(50)

    def checkcell(self,x,y):
        if chr((self.screen.inch(y,x)) & 0xFF) != " ":
            return 1
        else:
            return 0

class PygameGraphics(Graphics):

    def __init__(self, x, y):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((constant.WIN_WIDTH, constant.WIN_HEIGHT))
        self.font = pygame.font.SysFont('arial', 20)
        pygame.font.init()

    def drawwin(self):
        win = pygame.Surface((GAME_WIN_WIDTH,GAME_WIN_HEIGHT))

    def draw(self, row, col, ch=" ", color=1):
        pass

    def refresh(self, win, x, y):
        self.screen.blit(win, x, y)

    def checkcell(self,x,y):
        pass

class Board:

    def __init__(self, painter, x, y, startx=0, starty=0, label=None):
        self.painter = painter
        self.x = x
        self.y = y
        self.startx = startx
        self.starty = starty
        self.label = label
        self.drawwin()

    def drawwin(self):
        self.win = self.painter.drawwin(self.x,self.y,self.startx,self.starty,self.label)

    def redrawwin(self):
        self.painter.redrawwin(self.win,self.label)

    def checkcell(self, x, y):
        return self.painter.checkcell(x,y)

    def draw(self, x, y, fill=" "):
        self.painter.draw(self.win, x, y, fill)

    def drawtext(self, x, y, st):
        self.painter.drawtext(self.win, x, y, st)

    def refresh(self):
        self.redrawwin()
        self.painter.refresh(self.win, self.startx, self.starty)

class LevelManager:

    def __init__(self, painter="G"):
        if painter == "G":
            self.painter = PygameGraphics(constants.WIN_WIDTH, constants.WIN_HEIGHT)
            self.gameboard = Board(self.painter,
                                    constants.GAME_WIN_WIDTH,
                                    constants.GAME_WIN_HEIGHT,
                                    0,0, constants.GAME_LABEL)
            self.scoreboard = Board(self.painter,
                                    constants.SCORE_WIN_WIDTH,
                                    constants.SCORE_WIN_HEIGHT,
                                    constants.GAME_WIN_WIDTH,0,
                                    constants.SCORE_LABEL)
            self.input = GraphicsInput()
        elif painter == "T":
            self.painter = TerminalGraphics(constants.WIN_ROW_COUNT, constants.WIN_COL_COUNT)
            self.gameboard = Board(self.painter,
                                    constants.GAME_COL_COUNT,
                                    constants.GAME_ROW_COUNT,
                                    0,0, constants.GAME_LABEL)
            self.scoreboard = Board(self.painter,
                                    constants.SCORE_COL_COUNT,
                                    constants.SCORE_ROW_COUNT,
                                    constants.GAME_COL_COUNT,0,
                                    constants.SCORE_LABEL)
            self.input = ConsoleInput(self.painter.screen)
        self.foods = [Food(self.gameboard) for i in range(constants.FOOD_NUMBER)]
        self.snakes = [Snake(self.foods,self.gameboard,1) for i in range(constants.SNAKE_NUMBER)]
        
    def check_collision(self):
        for snake1 in self.snakes:
            for snake2 in self.snakes:
                if snake1.head() in snake2.body and snake1.fill != snake2.fill:
                    snake1.collision = 1

    def catch_food(self):
        for snake in self.snakes:
            for food in self.foods:
                if snake.head() == [food.x,food.y]:
                    snake.needgrow = 1
                    food.spawn()
    
    def update(self):
        
        for food in self.foods:
            food.draw()
        
        i = 0

        for snake in self.snakes:
            snake.update()
            self.check_collision()
            self.catch_food()
            self.scoreboard.drawtext(2, 2+i, "===[ " + snake.fill + " => " + str(snake.score) + " ]===" )
            i += 1
        
        self.scoreboard.refresh()
        self.gameboard.refresh()

    def loop(self):
        
        presskey = 0

        while presskey != -1:

            presskey = self.input.key_pressed()
            
            self.update()

class Snake:

    def __init__(self, foods, board, ai=0, x=None, y=None, direction=None, color=1, fill=None):
        dirdict = {"U":0,"L":1,"D":2,"R":3}
        self.foods = foods
        self.fill = fill if fill is not None else random.choice(string.ascii_uppercase)
        self.direction = direction if direction is not None  else random.choice(list(dirdict.values()))
        self.color = color
        self.ai = ai
        self.board = board
        self.collision = 0
        self.needgrow = 0
        self.score = 0
        self.reset(x,y)

    def head(self):
        return self.body[0]
    
    def reset(self,x=None,y=None):
        self.size = random.randint(1,5)
        self.body = [[0,0] for i in range(self.size)]
        self.body[0][0] = x if x is not None else random.randint(self.board.startx + 1, self.board.x - 1)
        self.body[0][1] = y if y is not None else random.randint(self.board.starty + 1, self.board.y - 1)
        self.collision = 0
        self.needgrow = 0
        self.target = None

    def death(self):
        self.score -= 100
        for cell in self.body:
            self.board.draw(cell[0], cell[1])
        self.reset()

    def update(self):

        if self.collision == 1:
            self.death()

        x, y = self.head()
      
        #Если установлен флаг автоматического управлений движением змейки
        if self.ai == 1:
            #Проверяем где самая ближняя еда по направлению
            #Только если у нас нет текущей цели еды, к которой мы встретимся или еду уже съели
            if self.target is None: 
                self.target = random.choice(list(self.foods))
            elif self.board.checkcell(self.target.x,self.target.y):
                self.target = random.choice(list(self.foods))

            #Простейший интеллект
            #Если вертикаль не совпадает, то если движется по горизонтали, то меняем направление на движение по вертикали
            #в зависимости где ближе: сверху или снизу
            if y != self.target.y:
                if self.direction == 1 or self.direction == 3:
                    self.direction = 0 if y > self.target.y else 2
            #Если горизонталь не совпадает, то если движется по вертикали, то меняем направление на движение по горизонтали
            #в зависимости где ближе: справа или слева
            elif x != self.target.x:
                if self.direction == 0 or self.direction == 2:
                    self.direction = 1 if x > self.target.x else 3

        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            y -= 1
            if y <= self.board.starty:
                y = self.board.y - 1
        elif self.direction == 2:
            y += 1
            if y >= self.board.y - 1:
                y = self.board.starty
        elif self.direction == 1:
            x -= 1
            if x <= self.board.startx:
                x = self.board.x - 1
        elif self.direction == 3:
            x += 1
            if x >= self.board.x - 1:
                x = self.board.startx

        self.body.insert(0, [x, y])
        self.board.draw(x, y, self.fill)
        if self.needgrow == 0:
            self.body.pop(len(self.body) - 1)
            self.board.draw(self.body[-1][0], self.body[-1][1])
        else:
            self.needgrow = 0
            self.score += 10
            self.size += 1
            self.target = None

class Food:

    def __init__(self, board, view=None, price=10):
        self.price = price
        self.view = view if view is not None else random.choice(string.punctuation)
        self.board = board
        self.spawn()

    def spawn(self):
        while True:
            self.x = random.randint(self.board.startx + 1, self.board.x - 1)
            self.y = random.randint(self.board.starty + 1, self.board.y - 1)
            if self.board.checkcell(self.x, self.y) == 0:
                break

    def draw(self):
        self.board.draw(self.x, self.y, self.view)


