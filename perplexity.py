import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Rainbow Spiral Vortex")

# Create the turtle
vortex = turtle.Turtle()
vortex.speed(0)
vortex.pensize(2)
vortex.hideturtle()

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Draw the spiral vortex
for i in range(200):
    vortex.color(colors[i % len(colors)])
    vortex.forward(15 + i*2)
    vortex.left(61)
    vortex.forward(8 + i)
    vortex.left(120)
    vortex.forward(8 + i)
    vortex.left(61)
    vortex.forward(15 + i*2)
    vortex.right(181)

turtle.done()
