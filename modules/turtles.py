from turtle import Turtle, Screen, Terminator
import sys
from math import ceil

TURTLE_SPEED = 9
RED_BAR_COLOR = '#f73737'
GREEN_BAR_COLOR = '#3ba010'
BASE_BAR_COLOR = '#383354'
TURTLE_PEN_SIZE = 10
TURTLE_FONT_SIZE = 10
TURTLE_PEN_COLOR = 'white'
TURTLE_ROUND_CORNER_RADIUS = 0


def drawBar(turtle, startPos, height, color, width, edgeColor=TURTLE_PEN_COLOR, radius=TURTLE_ROUND_CORNER_RADIUS):
    turtle.color(edgeColor)
    turtle.fillcolor(color)
    turtle.penup()
    turtle.setpos(startPos)
    turtle.pendown()
    turtle.begin_fill()
    turtle.setheading(90)
    turtle.forward(height-radius)
    turtle.circle(-radius,90)
    turtle.setheading(0)
    turtle.forward(width-radius)
    turtle.circle(-radius, 90)
    turtle.setheading(-90)
    turtle.forward(height-radius)
    turtle.penup()
    turtle.end_fill()

def showTurtleChart(names, baseBar, greenBar, redBar, y):
    
    turtle = Turtle()
    turtle.speed(TURTLE_SPEED)
    turtle._tracer(False)
    
    wn = Screen()
    wn.bgcolor("#232130")
    wn.setup(1200,600)

    
    maxheight = max(y+redBar)
    border = ceil(maxheight/10)
    numbars = len(y)
    width = border*5
    wn.setworldcoordinates(0-border,0-3*border,(border+width)*numbars+2*border,maxheight+2*border)

    barStartPositions = []

    turtle.penup()
    turtle.setheading(0)
    turtle.forward(border)
    turtle.pendown()
    turtle.hideturtle()
    turtle.color(TURTLE_PEN_COLOR)
    barStartPositions += [turtle.pos()]
    
    for _ in range(1, len(y)):
        turtle.forward(border+width)
        barStartPositions += [turtle.pos()]
    turtle.forward(width)

    for i in range(len(y)):
        if greenBar[i] == 0:
            if not redBar[i] == 0:
                drawBar(turtle, barStartPositions[i], redBar[i]+baseBar[i], RED_BAR_COLOR, width)
        elif redBar[i] == 0:
            if not greenBar[i] == 0:
                drawBar(turtle, barStartPositions[i], greenBar[i]+baseBar[i], GREEN_BAR_COLOR, width)
        if not baseBar[i] == 0:
            drawBar(turtle, barStartPositions[i], baseBar[i], BASE_BAR_COLOR, width)
    
    for i in range(len(names)):
        turtle.penup()
        turtle.goto((i+1)*border+width*(i+1/2),-1*border)
        turtle.pendown()
        turtle.write(names[i][-15:-10],align='center',font=('Arial',10,'normal'))        
        turtle.penup()
        turtle.goto((i+1)*border+width*(i+1/2),-1.5*border)
        turtle.pendown()
        turtle.write(names[i][-10:],align='center',font=('Arial',10,'normal'))        
        turtle.penup()
        
    turtle.pensize(2)
    turtle.pencolor('#938db9')
    turtle._tracer(True)
    turtle.goto(border+width/2,y[0])
    turtle.pendown()
    for i in range(1,len(y)):
        turtle.goto((i+1)*border+width*(i+1/2),y[i])

    turtle.pencolor('white')
    turtle.pendown()
    turtle._tracer(False)
    for i in range(len(y)):
        turtle.goto((i+1)*border+width*(i+1/2),y[i])
        turtle.write(str(y[i]),align='center',font=('Arial',11,'bold')) 

    wn.exitonclick()

names = []
baseBar = []
greenBar = []
redBar = []
y = []

length = int(sys.argv[1])

for i in range(2,2+length):
    names += [sys.argv[i]]

for i in range(2+length, 2+2*length):
    baseBar += [float(sys.argv[i])]

for i in range(2+2*length, 2+3*length):
    greenBar += [float(sys.argv[i])]

for i in range(2+3*length, 2+4*length):
    redBar += [float(sys.argv[i])]

for i in range(2+4*length, 2+5*length):
    y += [float(sys.argv[i])]

showTurtleChart(names, baseBar, greenBar, redBar, y)