from turtle import *
import colorsys

# Fix screen creation
screen = Screen()  # Changed from Turtle.Screen()
screen.title("happy diwali")
screen.setup(width=500, height=500)  # Set window size

# Set background color
color = colorsys.hsv_to_rgb(0.6, 0.05, 0.95)
screen.bgcolor(color)  # Changed tsr to screen

# Setup turtle
t = Turtle()
t.shape("circle")
colist = ["red", "orange", "yellow", "green", "blue", "purple"]
col2=colorsys.hsv_to_rgb(0.83333,1.0,1.0)

t.fillcolor(col2)
t.penup()
t.goto(0, -150)
t.pendown()
t.begin_fill()
t.circle(150)
t.end_fill()
t.penup()
t.goto(0, 0)
t.pendown()
# Fix class structure
class Mandala:
    def draw(self):
        for col in colist:
            t.fillcolor(col)
            t.begin_fill()
            for j in range(2):
                    t.forward(100)
                    t.left(60)
                    t.forward(100)
                    t.left(120)
            t.end_fill()    
            t.left(60)

# Create and draw mandala
mandala = Mandala()
mandala.draw()
t.hideturtle()
t.penup()
t.goto(0, 200)
t.pendown()
t.write("Happy Diwali!", align="center", font=("Arial", 24, "bold"))
# Keep window open
screen.mainloop()
