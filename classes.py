from abc import ABCMeta, abstractmethod

class Board(metaclass=ABCMeta):

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
    def checkregion(self):
        pass

class Input(metaclass=ABCMeta):

    @abstractmethod
    def key_pressed(self,char)
        pass

class ConsoleInput(Input):

    def key_pressed(self,char)
        pass

class GraphicsInput(Input):
    def key_pressed(self,char)
        pass


class ConsoleBoard(Board):

    def __init__(self, x, y):
        self.board = curses.newwin(0, 0, y, x)
        self.miny, self.minx = self.board.getbegyx()
        self.maxy, self.maxx = self.board.getmaxyx()

    def drawwin(self):
        self.board.box(curses.A_VERTICAL, curses.A_HORIZONTAL)

    def draw(self, row, col ch=" ", color=1):
        if len(ch) > 1:
            self.board.addstr(row, col, st)
        else:
            self.board.addch(row, col, ch)

    def refresh(self):
        self.board.refresh()

    def checkregion(self,row,col):
        return chr((self.board.inch(row,col)) & 0xFF)

class GraphicsBoard(Board):

    def __init__(self, x, y):
        

    def drawwin(self):
        

    def draw(self, row, col ch=" ", color=1):
        

    def refresh(self):
        

    def checkregion(self,row,col):
        

class Snake:

    def __init__(self, foods, board, ai=0, x=None, y=None, direction=None, color=1, size=5, fill=None):
        self.size = size
        self.fill = fill if fill is not None else random.choice(string.ascii_uppercase)
        self.direction = direction if direction is not None  else random.choice(list(dirdict.values()))
        self.color = color
        self.ai = ai
        self.board = board
        self.foods = foods
        self.collision = 0
        self.needgrow = 0
        self.score = 0
        self.reset(x,y)

    def head(self):
        return self.body[0]
    
    def reset(self,x=None,y=None):
        self.body = [[0,0] for i in range(self.size)]
        self.body[0][0] = x if x is not None else random.randint(self.board.minx,self.board.maxx - 1)
        self.body[0][1] = y if y is not None else random.randint(self.board.miny,self.board.maxy - 1)
        self.collision = 0
        self.needgrow = 0
        self.target = None

    def death(self):
        self.score -= 100
        for i in range(len(self.body)-1):
            self.board.draw(self.body[i][0], self.body[i][1], " ")
        self.reset()

    def update(self):

        if snake.collision == 1:
            self.death()

        y, x = self.head()
      
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
            if y != self.target[0]:
                if self.direction == 1 or self.direction == 3:
                    self.direction = 0 if y > self.target[0] else 2
            #Если горизонталь не совпадает, то если движется по вертикали, то меняем направление на движение по горизонтали
            #в зависимости где ближе: справа или слева
            elif x != self.target[1]:
                if self.direction == 0 or self.direction == 2:
                    self.direction = 1 if x > self.target[1] else 3

        #Совершаем движение на один шаг в выбранном направлении
        if self.direction == 0:
            y += 1
            if y >= self.board.maxy - 1:
                y = self.board.miny
        elif self.direction == 2:
            y -= 1
            if y <= self.board.miny:
                y = self.board.maxy - 1
        elif self.direction == 1:
            x -= 1
            if x <= self.board.minx:
                x = self.board.maxx - 1
        elif self.direction == 3:
            x += 1
            if x >= self.board.maxx - 1:
                x = self.board.minx

        self.body.insert(0, [y, x])
        self.board.draw(y, x, self.fill)
        if self.needgrow == 0:
            self.body.pop(len(self.body) - 1)
            self.board.draw(self.body[-1][0], self.body[-1][1], " ")
        else:
            self.needgrow = 0
            self.score += 10
            self.target = None

class Food:

    def __init__(self, board, view=None, price=10):
        self.price = price
        self.view = view if view is not None else random.choice(string.punctuation)
        self.board = board
        self.spawn()

    def spawn(self):
        while True:
            self.x = random.randint(self.board.minx, self.board.maxx - 1)
            self.y = random.randint(self.board.miny, self.board.maxy - 1)
            if self.board.checkch(self.x, self.y) == " ":
                break

    def draw(self):
        self.board.draw(self.x, self.y, self.view)


class LevelManager:

    def __init__(self,snakecount, foodcount, gameboard, scoreboard):
        self.snakecount = snakecount
        self.foodcount = foodcount
        self.foods = [Food(gameboard) for i in range(self.foodcount)]
        self.snakes = [Snake(self.foods,gameboard,1) for i in range(self.snakecount)]
        self.gameboard = gameboard
        self.scoreboard = scoreboard
   
    def check_collision(self):
        for snake1 in self.snakes:
            for snake2 in self.snakes:
                if snake1.head() in snake2.body and snake1.fill != snake2.fill:
                    snake1.collision = 1

    def catch_food(self):
        for snake in self.snakes:
            for food in self.foods:
                if snake.head() == [food.row,food.col]:
                    snake.needgrow = 1
                    food.spawn()
    
    def update(self):
        for food in self.foods:
            food.draw()

        i = 0

        for snake in self.snakes:
            self.snake.update()
            self.check_collision()
            self.catch_food()
            self.scoreboard.drawstr(2+i, 2, "===[ " + snake.fill + " => " + str(snake.score) + " ]===" )
            i += 1
        
        self.scoreboard.refresh()

        self.gameboard.drawwin()
        self.gameboard.drawstr(0,35,"WANNA PLAY WITH SNAKES?")
        self.gameboard.refresh()
