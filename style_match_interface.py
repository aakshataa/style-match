from tkinter import *
from tkinter.tix import Balloon

import requests
from tkinter import filedialog
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import pandas as pd
import time
from tkinter import Tk, font

import tkinter as tk
from tkinter import Label
from tkinter import filedialog

# source: https://dev.to/jairajsahgal/creating-a-file-uploader-in-python-18e0
# source: https://www.youtube.com/watch?v=TuLxsvK4svQ&t=455s

# widgets = GUI elements: buttons, textboxes, labels, images
# windows = serves as a container to hold these widgets

window = Tk()  # instantiate an instance of a window
window.geometry("800x800")
window.title("StyleMatch")
window.configure(bg='#e1e5e6')
label = Label(window,
              text="StyleMatch",
              fg="#293366",
              font=('Avenir Next', 80, 'bold'),
              anchor='center',
              justify='center',
              bg='white',
              padx=20,
              pady=20)

label.pack(padx=50, pady=60)

select_file = Label(window,
                    text="Please select your file. Must be type .jpg, .jpeg, or .png",
                    fg="#293366",
                    font=('Avenir Next Thin', 20),
                    anchor='center',
                    justify='center',
                    padx=20,
                    pady=60)

def play_select_file():
    select_file.pack()
    time.sleep(0.1)
    browse()
def browse():

    time.sleep(0.1)
    filelocation = askopenfilename()
    file_name = filelocation.split("/")[-1]
    print(filelocation)

    files = {
        'file': (file_name, open(filelocation, 'rb')),
    }
    response = requests.post('https://file.io/', files=files)

    data = json.loads(response.text)

    if data["success"]:
        print("One use hyperlink with your file -> ", data["link"], " copied to your clipboard")
        print(filelocation)
        # img.save(file_name.split(".")[0] + ".png")
        df = pd.DataFrame([data["link"]])
        df.to_clipboard(index=False, header=False)


browse_button = Button(window,
                       text="Browse Image",
                       command=play_select_file,
                       font=("Avenir Next", 30),
                       fg="#293366"
                       )

browse_button.pack()


"""save_button = Button(window,
                text="Upload",
                command=click,
                font=("Arial", 30),
                fg= "#293366",
                width=50
                )"""
window.mainloop()  # place window on computer screen, listen for events
