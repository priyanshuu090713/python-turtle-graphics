from turtle import *
import time
#other unnecessary programmes
speed(1)
screensize(1000,1000)
turtlesize(1)

#base/ground
penup()
left(225)
forward(100)
right(225)
pendown()
fillcolor("brown")
begin_fill()
for i in range(2) :
 forward(160)
 right(90)
 forward(10)
 right(90)
end_fill()

#mountains
fillcolor("grey")

#mountain1
begin_fill()
penup()
forward(2)
pendown()
left(80)
forward(200)
right(80*2)
forward(200)
right(80)

#mountain2
penup()
forward(2)
pendown()
left(80*3)
forward(200)
right(80*2)
forward(200)
right(80)

end_fill()
time.sleep(10)
turtles.done()
