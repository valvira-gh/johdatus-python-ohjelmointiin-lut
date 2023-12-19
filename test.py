# This imports all from said libraries and also
# automatically translates good ol' tk.widgets to modern ttk.widgets
from tkinter import *
from tkinter.ttk import *


# Global dictionary
border_effects = {
    'flat': FLAT,
    'sunken': SUNKEN,
    'raised': RAISED,
    'groove': GROOVE,
    'ridge': RIDGE
    }


window = Tk() # Initialize root screen component

size = "400x200" # Width x Height
window.geometry(size) # Adjust the size of the screen component 'window'

# Print a message when the button is clicked
def print_message(message):
    print("Message:", message)


button = Button(window,
                text="Click me",
                command=print_message(border_effects.items())
                )


for relief_name in border_effects.items():
    continue


window.mainloop()

