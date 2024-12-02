import random
from tkinter import *
import  pandas


BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
data_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")

else:
    data_dict = data.to_dict(orient="records")


####----------------------------------------------------------------
def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill= "black")
    canvas.itemconfig(card_word, text=current_card["French"], fill= "black")
    canvas.itemconfig(card_background, image= card_front)
    flip_timer = window.after(2000, flip_card)


def flip_card():

    canvas.itemconfig(card_title, text="English", fill= "white")
    canvas.itemconfig(card_word, text=current_card["English"], fill= "white")
    canvas.itemconfig(card_background, image= card_back)

def is_known():
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/words_to_learn", index=False)
    next_card()

###-----------------------------------------------------------------



window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(2000, flip_card)

canvas = Canvas(width=800, height=526)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front)

card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command=next_card)
unknown_button.grid(row=1, column=0)


check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()