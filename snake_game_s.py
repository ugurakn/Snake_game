#Snake Game small screen version (%20 smaller)

from tkinter import *
import random


# game constants
C_WIDTH   = 480
C_HEIGHT  = 480
GRID_SIZE = 20
SPEED     = 80
BODY_PARTS= 3
SNAKE_CLR = "green"
FOOD_CLR  = "orange"
BG_CLR    = "white"

assert C_WIDTH % GRID_SIZE == 0 and C_HEIGHT % GRID_SIZE == 0, "grid system does not fit into canvas"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coords  = []
        self.squares = []
    

        for i in range(0, BODY_PARTS):
            self.coords.append([0,0])

        for x,y in self.coords:
            square = c.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill=SNAKE_CLR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, ((C_WIDTH / GRID_SIZE) -1)) * GRID_SIZE
        y = random.randint(0, ((C_HEIGHT / GRID_SIZE) -1)) * GRID_SIZE

        self.coords = [x,y]

        self.square = c.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill=FOOD_CLR, outline="", tag="food")



def turn(snake, food, dirc):
    global direction
    
    # if-elif makes sure snake can't make a 180 turn into itself
    if direction[2] == "left" or direction[2] == "right":
        if (direction[0] + dirc[0]) == 0:
            direction = dirc

    elif direction[2] == "up" or direction[2] == "down":
        if (direction[1] + dirc[1]) == 0:
            direction = dirc
    
    x = snake.coords[0][0] + direction[0]
    y = snake.coords[0][1] + direction[1]
    

    square = c.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill=SNAKE_CLR, tag="snake")
    snake.squares.insert(0, square)
    
    snake.coords.insert(0, [x,y])

    dirc = direction

    if snake.coords[0] == food.coords:
        
        #delete eaten food and create another one
        c.delete(food.square)
        food = Food()

        global score
        score += 1
        score_l.config(text=f"score: {score}")

    else:
        c.delete(snake.squares[-1])
        del snake.squares[-1]
        
    # check collision (if True, game over)
    if check_collision():
        game_over()
        return
        

    win.after(SPEED, turn, snake, food, dirc)


def direct(event):
    global direction
    
    if event == "left":
        if direction[2] != "right":
            direction = [(-GRID_SIZE), 0, "left"]
        
    elif event == "right":
        if direction[2] != "left":
            direction = [GRID_SIZE, 0, "right"]

    elif event == "up":
        if direction[2] != "down":
            direction = [0, (-GRID_SIZE), "up"]

    elif event == "down":
        if direction[2] != "up":
            direction = [0, GRID_SIZE, "down"]


def check_collision():
    x = snake.coords[0][0]
    y = snake.coords[0][1]
    
    # check game_over state (snake eating itself)
    for i in range(len(snake.squares)):
        if snake.coords[0] == snake.coords[i+1]:
            return True

    # check if snake is within the canvas
    if x not in range(0, (C_WIDTH-GRID_SIZE+1)) or y not in range(0,(C_HEIGHT-GRID_SIZE+1)):
        return True

            

def game_over():
    x = int(C_WIDTH / 2)
    y = int(C_HEIGHT / 2)

    #c.delete(ALL)
    c.create_text(x, y, text=f"GAME OVER!\nfinal score: {score}", font=("Arial", 50), fill="red")

        
        



# other variables
direction = [0, GRID_SIZE, "down"]
score = 0



# main window
win = Tk()
win.title("Snake game")
win.resizable(False, False)

# center window on screen
win.update()
scr_width = win.winfo_screenwidth()
scr_height = win.winfo_screenheight()
width  = 550
height = 600
x_pos = int((scr_width / 2) - (width / 2))
y_pos = int((scr_height / 2) - (height / 2)) - 50
win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

win.config(bg="black")

# create scoreboard
score_l = Label(win, text=f"score: {score}", font=("Arial", 24), bg="black", fg="white")
score_l.pack(pady=(5,0))

# create canvas
c = Canvas(win, height=C_HEIGHT, width=C_WIDTH, bg=BG_CLR)
c.pack(pady=10)

# bind keys to window to move snake
win.bind("a", lambda event:direct("left"))
win.bind("d", lambda event:direct("right"))
win.bind("w", lambda event:direct("up"))
win.bind("s", lambda event:direct("down"))

# create snake and food instances
snake = Snake()
food = Food()





if __name__ == "__main__":

    turn(snake, food, direction)

    win.mainloop()

