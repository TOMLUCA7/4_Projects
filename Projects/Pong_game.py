import pygame
pygame.init()

# שרושמים משתנה עם אותיות גדולות הכוונה שלא רוצים להחליף את אותו הערך של המשתנה
# גודל החלון שמשחקים
WIDTH, HEIGHT = 700, 500
# הצגה של החלון
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# שם של המשחק מופיעה בראש בחלון של המשחק
pygame.display.set_caption("Pong")

# פריים לשניה (מהיאות של הכדור)
FPS = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# גודל הפדלים
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
# גודל הכדור
BALL_RADIUS = 7

# הצגת התוצאות של השחקנים על החלון של המשחק
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# עד אזה תוצא משחקים
WINNING_SCORE = 5

# מחקלה של הפדלים
class Paddle:
    COLOR = WHITE
    VEL = 4
    # לכול פדל יש מיקום שונה ואןתם מעבירים לפונקציה
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        #  הצגה של הפדלים כמלבנים ומעבירים אליו את המיקום אורך ורוחב וצבע
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))
    # פונקציה להזזת הפדלים למטה ולמעלה
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# מחקלה של הכדור
class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    #  כיוונים שהכדור נעה בניהם
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    # יצירה של הכדור בצורת עיגול
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    # איך  שמוזיזים את הכדור
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # איפוס של הכדור מרגע שהוא יוצא מהחלון
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    # הצגת הכתוביות בלוח
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)

    # מיקום של הכתוביות על הלוח
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    # יצירת קן הפקדה בעמצא הלוח (ע״י יצירה של מבנים)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

# פונקציה איפה הכדור פוגע ולאן הוא ממשיך מאותה הפיעה
def handle_collision(ball, left_paddle, right_paddle):
    # הןפך את הכיוון של בכדור
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # בדיקה שפוגעיה בפדל שמאלי
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    # בדיקה שפוגעיה בפדל הימיני
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# פונקציה של הכפרותים חצים לשחקן ימיני w,s לשחקן השמאלי
def handle_paddle_movement(keys, left_paddle, right_paddle):
    # הדיקה שהפדל לא יוצאים מהלוח
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # בדיקה שהפדל לא יוצא מהלוח
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

 # הלולטה הראשית שמניעה את המשחק שמאפשרת לנו להוזיז את הפדלים ואת הכדור
def main():
    run = True
    clock = pygame.time.Clock()
    # מיקום של הפדל השמאלי וימיני ומיקום הדכור
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # משתנים לתוצאות
    left_score = 0
    right_score = 0

    # לולאה שמאפשרת לנו להוזיז את העכבר לבגור את חלון המשחק וכו
    while run:
        # דואג שהמחשב לא ירוץ יותר מהר ממש שהוגדר לו
        clock.tick(FPS)
        # הצגת החלון ,הפדל ימיני השמאלי, הכדור תןצא של השחקן ימיני והשחקן השמאלי
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        # בדיקה אם השחקן סגר את החלון אם כן יוצאים מהלולאה
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        # כפתורים להזזת הפדלים
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        # קריאה לפונקציה הוזזת הכדור
        ball.move()
        # קריאה לפונקציה(בדיקת פגיעה של הכדור בפדלי )
        handle_collision(ball, left_paddle, right_paddle)

        # ביקה לאזה צד מגיע נקודה
        # וקריאה לפונקציה שמאפסת את הכדור
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # בדיקה של נצחון
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        # הצגה של מי שניצח בעמצא כול החון
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                            2, HEIGHT//2 - text.get_height()//2))
            # עידכון של ההצג
            pygame.display.update()

            # השעיה של 5 שניות של מי שניצח
            pygame.time.delay(5000)

            # איפוס המשחק
            ball.reset()

            # איפוס התוצא של השחקן השמאלי
            left_paddle.reset()

            # איפוב התוצאה של השחקן הימיני
            right_paddle.reset()

            # איפוב המשתנים
            left_score = 0
            right_score = 0

    pygame.quit()

# קריאה לפונקציה הראשית שמתחילה את המשחק
if __name__ == '__main__':
    main()
