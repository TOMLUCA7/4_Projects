from tkinter import *
import random
# פונקציה לתור הבא שמגיעה או בשורות או בעמודות
def next_turn(row, column):

    global player

    if buttons[row][column]['text'] == "" and check_winner() is False:
        # בדיקה של המשחקן באינדקס 0 תור/נצחון/תקו (X)
        if player == players[0]:

            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[1]
                label.config(text=(players[1]+" turn"))

            elif check_winner() is True:
                label.config(text=(players[0]+" wins"))

            elif check_winner() == "Tie":
                label.config(text="Tie!")
        # בדיקה של המשחקן באינדקס 1 תור/נצחון/תקו (O)
        else:

            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[0]
                label.config(text=(players[0]+" turn"))

            elif check_winner() is True:
                label.config(text=(players[1]+" wins"))

            elif check_winner() == "Tie":
                label.config(text="Tie!")
# פונקציה של נצחון של שתיי השחקנים
def check_winner():

    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True
    # במקרה שיש תקו
    elif empty_spaces() is False:

        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "Tie"

    else:
        return False

#כפתורים רקים על המסך גם בשורות וגם בעמודות כול פעם שלוחצים על כפתור השטח יורד ב 1
def empty_spaces():

    spaces = 9

    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1

    if spaces == 0:
        return False
    else:
        return True

def new_game():

    global player

    player = random.choice(players)

    label.config(text=player+" turn")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="",bg="#F0F0F0")

# חלון המשחק
window = Tk()
# כותרת
window.title("Tic-Tac-Toe")
# שחקנים (אפשר לשנות אם רוצים)
players = ["X","O"]
# האפשרויות של השחקן . שחקנים בצורה רנדומלית
player = random.choice(players)
# לוח משחק
buttons = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
# הצגת בתור פלןס השחקן שתורו לשחק בראש חלון המשחק
label = Label(text=player + " turn", font=('consolas', 40))
label.pack(side="top")

# כפרור איתחול (איפוס) המשחק בראש העמוד
reset_button = Button(text="restart", font=('consolas', 20), command=new_game)
reset_button.pack(side="top")

# אחרי על סידור המיקום של המלבנים במשחק
frame = Frame(window)
frame.pack()

# לקיחה של הלוח והתאמה של כול כפתור ללוח לכול נקודה בשורות ועמודות
for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="",font=('consolas', 40), width=5, height=2,
                                      command= lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

window.mainloop()