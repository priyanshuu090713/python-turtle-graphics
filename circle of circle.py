import turtle as t
t.bgcolor("black")
t.speed(-1)
col=["red","green","blue"]
while True :
     for i in col:
          t.color(i)
          t.fillcolor(i)
          t.begin_fill()
          t.circle(50)
          t.end_fill()
          t.right(5)
     t.forward(1)
