import turtle
import math
import tkinter as tk


# Set up screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Parabola y² = 4ax")

# Create one turtle for both axes and parabola
t = turtle.Turtle()
t.speed(0)
t.pensize(2)

def axes():
    t.color("white")

    # Function to draw arrowhead
    def arrow():
        t.begin_fill()
        for _ in range(3):
            t.forward(10)
            t.left(120)
        t.end_fill()

    # Draw X-axis
    t.penup()
    t.goto(-300, 0)
    t.pendown()
    t.setheading(0)
    t.forward(600)
    arrow()

    # X-axis labels
    t.penup()
    t.goto(310, -15)
    t.write("+X", font=("Arial", 12, "bold"), align="center")
    t.goto(-310, -15)
    t.write("-X", font=("Arial", 12, "bold"), align="center")

    # Tick marks on X-axis
    for x in range(-250, 301, 50):
        t.penup()
        t.goto(x, -5)
        t.pendown()
        t.goto(x, 5)

    # Draw Y-axis
    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()
    t.forward(500)
    arrow()

    # Y-axis labels
    t.penup()
    t.goto(15, 260)
    t.write("+Y", font=("Arial", 12, "bold"), align="left")
    t.goto(15, -260)
    t.write("-Y", font=("Arial", 12, "bold"), align="left")

    # Tick marks on Y-axis
    for y in range(-200, 251, 50):
        t.penup()
        t.goto(-5, y)
        t.pendown()
        t.goto(5, y)

    # Mark origin
    t.penup()
    t.goto(0, 0)
    t.dot(8, "red")
    t.write("  O(0,0)", font=("Arial", 10, "bold"))

def parabola():
    t.color("blue")
    a = 20  # Controls width (the larger the a, the wider)

    # Start at vertex
    t.penup()
    t.goto(0, 0)
    t.pendown()

    # Draw y² = 4ax  →  y = ±√(4ax)
    for x in range(0, 200):  # only right side
        y = math.sqrt(4 * a * x)
        t.goto(x, y)
    t.penup()
    t.goto(0, 0)
    t.pendown()
    for x in range(0, 200):
        y = -math.sqrt(4 * a * x)
        t.goto(x, y)

    # Mark vertex
    t.penup()
    t.goto(0, -20)
    t.color("yellow")
    t.write("Vertex (0,0)", font=("Arial", 10, "bold"))

# Draw everything
axes()
parabola()

t.hideturtle()
turtle.done()
