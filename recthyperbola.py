import turtle


# Setup the screen and turtle
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
t.color("blue")
t.pensize(2)

# Parameter 'a' controls the parabola width
# a = 20

# Move to the starting point (vertex)
t.penup()
t.goto(0, 0)
t.pendown()

# Draw the upper curve (solid line)
for x in range(1, 400):
    y =300/x
    t.goto(x, y)


# Keep window open
turtle.done()
