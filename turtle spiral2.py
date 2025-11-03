import turtle as t

# Setup screen
screen = t.Screen()
screen.bgcolor("black")
screen.title("Organized Chaos")

# Setup turtle
pen = t.Turtle()
pen.speed(0)
pen.width(2)

# Color palette
colors = ["red", "green", "blue", "yellow"]

# Initialize variables
r = 101
ri = 1

# Drawing loop
while True:
    for color in colors:
        pen.pencolor(color)
        pen.circle(ri)
        pen.right(1 - r)
        pen.forward(10 - ri)

        # Update radius values
        r += 1
        ri += 1

        # Reset logic to keep values in range
        if r <= 101:
            r = r + 60  # Prevents negative or small radii
        elif r >= 160:
            r -= 60

