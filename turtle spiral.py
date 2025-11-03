import turtle as t

s = t.Screen()
s.bgcolor("black")
s.title("circle spiral")

r = 10
cl = ["red", "green", "blue"]

t = t.Turtle()
t.speed(0)

while True:
    for c in cl:
        t.pencolor(c)
        t.fillcolor(c)
        t.begin_fill()
        t.circle(r)
        t.end_fill()
        t.right(r)
        t.forward(10)
        r += 1
