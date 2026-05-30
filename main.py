from tkinter import *
import pandas
import random

try:
    words = pandas.read_csv('words_to_learn.csv')
except FileNotFoundError:
    words = pandas.read_csv('1000words.csv')
words_dict = {row.spanish:row.english for (index, row) in words.iterrows()}
words_list = [x for x in words_dict.keys()]
random.shuffle(words_list)
# ---------------------------- CONSTANTS ------------------------------- #
ORANGE = '#F8CBAD'
BLACK = '#000000'
WHITE = '#FFFFFF'
FONT_NAME = 'Century Gothic'
RANDOM_SPANISH_WORD = random.choice(words_list)
CORRECT_GUESSES = []
# ---------------------------- FUNCTIONS ------------------------------- #
# Takes corresponding english translation from previous spanish word and displays it on flashcard
def flip():
    global RANDOM_SPANISH_WORD
    canvas.itemconfig(unflipped_flash, image=flashcard__white_img)
    canvas.itemconfig(spanish_text, text='English', fill=BLACK)
    canvas.itemconfig(vocab_text, text=words_dict[RANDOM_SPANISH_WORD], fill=BLACK)

# Picks random spanish word from list of dictionary keys and displays it on the "front" of a flashcard. After 3 seconds,
# the function flip is called to "flip" the card, revealing the english translation
# Also checks for "learned" spanish terms and removes them from the list of words if randomly chosen again
def new_card():
    global RANDOM_SPANISH_WORD
    global CORRECT_GUESSES
    RANDOM_SPANISH_WORD = random.choice(words_list)
    if RANDOM_SPANISH_WORD in CORRECT_GUESSES:
        words_list.remove(RANDOM_SPANISH_WORD)
        new_card()
    canvas.itemconfig(unflipped_flash, image=flashcard__red_img)
    canvas.itemconfig(spanish_text, text='Spanish', fill=WHITE)
    canvas.itemconfig(vocab_text, text=RANDOM_SPANISH_WORD, fill=WHITE)
    window.after(3000, flip)

# Command tied to the check button. When activated, will add the spanish term to a list that will be used to
# separate unlearned vs learned words. Then it activates the function new card to pull a new card with a new term
def verified():
    global CORRECT_GUESSES
    global RANDOM_SPANISH_WORD
    CORRECT_GUESSES.append(RANDOM_SPANISH_WORD)
    new_card()


# Window Setup
window = Tk()
window.title(f'{' ' * 100}Flashy')
window.minsize(width=600, height=400)
window.config(padx=80, pady=100, bg= ORANGE)

# Flashcard Setup using white and red images
canvas = Canvas(width=550, height=320, bg=ORANGE, highlightthickness=0)
flashcard__white_img = PhotoImage(file='flashcard1.png')
flashcard__red_img = PhotoImage(file='flashcard2.png')
unflipped_flash = canvas.create_image(280, 140, image=flashcard__red_img)
spanish_text = canvas.create_text(280, 80, text='Spanish', font=(FONT_NAME, 24, 'italic'), fill=WHITE)
vocab_text = canvas.create_text(280, 160, text= RANDOM_SPANISH_WORD, font=(FONT_NAME, 35, 'bold'), fill=WHITE)
canvas.grid(column=0, row=0, columnspan=2)

# Check Button w/ image
check_button_img = PhotoImage(file='check_box.png')
check_button = Button(image=check_button_img, bg=ORANGE, width=100, height=100, relief='flat', borderwidth=0, command=verified)
check_button.grid(column=1, row=1)

# X Button w/ image
x_button_img = PhotoImage(file='x_box.png')
x_button = Button(image=x_button_img, bg=ORANGE, width=100, height=100, relief='flat', borderwidth=0, command=new_card)
x_button.grid(column=0, row=1)

# Initial Card
window.after(5000, flip)
window.mainloop()

print(words_dict)
print(CORRECT_GUESSES)
# Creates dictionary with list of unlearned spanish words and list of corresponding english translation
words_to_learn_dict = {
    'spanish': [key for key in words_dict.keys() if key not in CORRECT_GUESSES],
    'english': [words_dict[key] for key in words_dict.keys() if key not in CORRECT_GUESSES]
}
# Converts dictionary of unlearned words to dataframe
Data = pandas.DataFrame(words_to_learn_dict)
# Saves dataframe of unlearned words as csv to use for the next time the GUI is called
Data.to_csv('words_to_learn.csv', index=False) 