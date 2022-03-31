import random
import turtle
import time

# יצירת לוח מישחק
screen = turtle.Screen()
screen.title('Snake Game')
screen.setup(width=700, height=700)
screen.tracer(0)
screen.bgcolor('#1d1d1d')

#יצירת לוח משחק וגבולות
turtle.speed(5)
turtle.pensize(4)
turtle.penup()
turtle.goto(-310, 250)
turtle.pendown()
turtle.color('blue')
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.right(90)
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.penup()
turtle.hideturtle()

# תוצא
score = 0
# מהירות של הנחש
delay = 0.1

# יצירת נחש
snake = turtle.Turtle()
snake.speed()
snake.shape('square')
snake.color('green')
snake.penup()
snake.goto(0, 0)
snake.direction = 'stop'

#האוכל
fruit = turtle.Turtle()
fruit.speed(0)
fruit.shape('square')
fruit.color('white')
fruit.penup()
fruit.goto(30, 30)

old_fruit = []

# תוצא
scoring = turtle.Turtle()
scoring.speed(0)
scoring.color('white')
scoring.penup()
scoring.hideturtle()
scoring.goto(0, 300)
scoring.write('score: ', align='center', font=('courier', 24, 'bold'))


# (חצים) תנוע של הנחש
def snake_go_up():
    if snake.direction != 'down':
        snake.direction = 'up'

def snake_go_down():
    if snake.direction != 'up':
        snake.direction = 'down'


def snake_go_left():
    if snake.direction != 'right':
        snake.direction = 'left'


def snake_go_right():
    if snake.direction != 'left':
        snake.direction = 'right'

def snake_move():
    if snake.direction == 'up':
        y = snake.ycor()
        snake.sety(y + 20)
    if snake.direction == 'down':
        y = snake.ycor()
        snake.sety(y - 20)
    if snake.direction == 'left':
        x = snake.xcor()
        snake.setx(x - 20)
    if snake.direction == 'right':
        x = snake.xcor()
        snake.setx(x + 20)


screen.listen()
screen.onkeyrelease(snake_go_up, "Up")
screen.onkeyrelease(snake_go_down, "Down")
screen.onkeyrelease(snake_go_left, "Left")
screen.onkeyrelease(snake_go_right, "Right")

# לולאר ראשית
while True:
    screen.update()

    # המיקום של הנחש והאוכל
    if snake.distance(fruit) < 20:
        x = random.randint(-290, 270)
        y = random.randint(-240, 240)
        fruit.goto(x, y)
        scoring.clear()
        score += 1
        scoring.write('score: {}'.format(score), align='center', font=('courier', 24, 'bold'))
        delay -= 0.001

        # יצירת אוכל חדש
        new_fruit = turtle.Turtle()
        new_fruit.speed(0)
        new_fruit.shape('square')
        new_fruit.color('red')
        new_fruit.penup()
        old_fruit.append(new_fruit)


    # הגדלה של הגול של הנחש
    for index in range(len(old_fruit) -1, 0, -1):
        a = old_fruit[index - 1].xcor()
        b = old_fruit[index - 1].ycor()

        old_fruit[index].goto(a, b)

    if len(old_fruit) > 0:
        a = snake.xcor()
        b = snake.ycor()
        old_fruit[0].goto(a, b)
    snake_move()

    # הנחש והמיקום של הלוח
    if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
        time.sleep(1)
        screen.clear()
        screen.bgcolor('turquoise')
        scoring.goto(0, 0)
        scoring.write('game over \n your score is {}'.format(score), align='center', font=('courier', 30, 'bold'))

    # התנגשויות נחשים  (סוף משחק)
    for food in old_fruit:
        if food.distance(snake) < 20:
            time.sleep(1)
            screen.clear()
            screen.bgcolor('turquoise')
            scoring.goto(0, 0)
            scoring.write('Game over \n Your score is {}'.format(score), align='center', font=('courier', 30, 'bold'))


    time.sleep(delay)

turtle.Turtle()