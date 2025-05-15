import turtle

# Window initialization
window = turtle.Screen()
window.title("Retro Pong Game")
window.bgcolor("black")
window.setup(width=1000, height=800)
window.tracer(0)


# GAME OBJECTS

# Score variables
leftScore = 0
rightScore = 0 

# Score Board
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 340)
pen.write("Left Player: 0     |     Right Player: 0", align="center", font=("Courier", 20, "normal"))



# Tennis Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0,0)
# ball movement increment. On both axes it will move with 0.7 pixels
ball.dx = 0.07
ball.dy = 0.07

# Left Paddle
left_paddle = turtle.Turtle()
left_paddle.speed(0)            # Animation Speed, maximum speed (0)
left_paddle.shape("square")
left_paddle.color("white")
left_paddle.shapesize(stretch_wid = 5, stretch_len = 1)
left_paddle.penup()             # this method will disable the line that the shape would otherwise leave behind
left_paddle.goto(-450, 0)

# Right Paddle
right_paddle = turtle.Turtle()
right_paddle.speed(0)            # Animation Speed, maximum speed (0)
right_paddle.shape("square")
right_paddle.color("white")
right_paddle.shapesize(stretch_wid = 5, stretch_len = 1)
right_paddle.penup()             # this method will disable the line that the shape would otherwise leave behind
right_paddle.goto(450, 0)





# GAME MECHANICS

# Left Paddle
def up_motion_left_paddle():
    y_coord = left_paddle.ycor() # .ycor() returns the y coordinates
    y_coord = y_coord + 20       # Increment the coordinate with 20 px (move up 20 px)
    left_paddle.sety(y_coord)    # set the new y coordinate

def down_motion_left_paddle():
    y_coord = left_paddle.ycor() # returns the y coordinate
    y_coord = y_coord - 20       # Decrease the coordinate value so it will go down
    left_paddle.sety(y_coord)    # set the new y coordinate

# Right Paddle
def up_motion_right_paddle():
    y_coord = right_paddle.ycor()
    y_coord = y_coord + 20
    right_paddle.sety(y_coord)

def down_motion_right_paddle():
    y_coord = right_paddle.ycor()
    y_coord = y_coord - 20
    right_paddle.sety(y_coord)


# Keyboard binding - Controls

# Set the window to listen to keyboard inputs from user
window.listen()     

# Left paddle
window.onkeypress(up_motion_left_paddle, "w")   # On key "w" the up motion will be activated for left paddle
window.onkeypress(down_motion_left_paddle, "s")   # On key "s" the up motion will be activated for left paddle

# Right paddle 
window.onkeypress(up_motion_right_paddle, "Up")  
window.onkeypress(down_motion_right_paddle, "Down")

# GAME LOOP - MOTION MECHANICS AND COLLISIONS
while True:
    window.update()

    # Ball Movement Mechanic
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border hitting mechanic
    # up border
    if ball.ycor() > 400:
        ball.sety(400)
        ball.dy = ball.dy * -1
        

    # down border
    if ball.ycor() < -400:
        ball.sety(-400)
        ball.dy = ball.dy * -1
        


    # right border - will restart 
    if ball.xcor() > 500:
        ball.goto(0, 0)
        ball.dx = ball.dx * -1
        leftScore = leftScore + 1
        pen.clear()
        pen.write("Left Player: {}     |     Right Player: {}".format(leftScore, rightScore), align="center", font=("Courier", 20, "normal"))

     # left border - will restart 
    if ball.xcor() < -500:
        ball.goto(0, 0)
        ball.dx = ball.dx * -1
        rightScore = rightScore + 1
        pen.clear()
        pen.write("Left Player: {}     |     Right Player: {}".format(leftScore, rightScore), align="center", font=("Courier", 20, "normal"))

    # Ball and Right Paddle Collision Mechanic 
    # if the ball is in the frame of the right paddle
    if (ball.xcor() > 440 and ball.xcor() < 450) and (ball.ycor() < right_paddle.ycor() + 50 and ball.ycor() > right_paddle.ycor() - 50):
        ball.setx(440)        
        ball.dx = ball.dx * -1
        

    # if the ball is in the frame of the left paddle
    if (ball.xcor() < -440 and ball.xcor() > -450) and (ball.ycor() < left_paddle.ycor() + 50 and ball.ycor() > left_paddle.ycor() - 50):
        ball.setx(-440)        
        ball.dx = ball.dx * -1
        