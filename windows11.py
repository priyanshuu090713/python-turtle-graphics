from turtle import *
import time

# Setup
screen = Screen()
screen.setup(width=1000, height=1000)
screen.bgcolor("black")
screen.title("windows 11 logo")
screen.tracer(0)

speed(0)

bgcolor("black")

color("blue")
fillcolor("blue")

pensize(0)
begin_fill()
for i in range(4):
    forward(100)
    circle(10,90)
end_fill()

penup()

goto(120,-55)
right(180)
pensize(5)
color("black")

pendown()
forward(200)
penup()
goto(52.5,0)
left(90)
pendown()
forward(200)

done()    
    
