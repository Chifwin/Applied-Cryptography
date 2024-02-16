import turtle

def draw_heart():
    t = turtle.Turtle()
    t.color("red")
    t.pensize(5)
    t.begin_fill()
    t.fillcolor("red")
    t.left(50)
    t.forward(133)
    t.circle(50, 200)
    t.right(140)
    t.circle(50, 200)
    t.forward(133)
    t.end_fill()
    t.hideturtle()

def print_love_message():
    love_message = '''Милому Олегу ♥♥♥'''
    turtle.penup()
    turtle.goto(0, -180)
    turtle.pendown()
    turtle.color("black")
    turtle.write(love_message, align="center", font=("Courier New", 24, "normal"))

if __name__ == "__main__":
    draw_heart()
    print_love_message()
    turtle.done()
