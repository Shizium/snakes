import curses
import random
import string
import classes

                
def key_pressed(char):
    if char == ord("q"): return -1
    elif char == ord("w") or char == ord("W") or char == curses.KEY_UP: return 0
    elif char == ord("a") or char == ord("A") or char == curses.KEY_LEFT: return 1
    elif char == ord("s") or char == ord("S") or char == curses.KEY_DOWN: return 2
    elif char == ord("d") or char == ord("D") or char == curses.KEY_RIGHT: return 3

#Constant
SNAKE_NUMBER = 2
FOOD_NUMBER = 2

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

level = LevelManager(SNAKE_NUMBER, FOOD_NUMBER, gameboard, scoreboard)

while presskey != -1:

    presskey = key_pressed(screen.getch())
    
    level.update()

    curses.napms(100)
    
curses.echo()
curses.curs_set(1)
curses.endwin()