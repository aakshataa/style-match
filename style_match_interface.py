from tkinter import *
import requests
from tkinter import filedialog
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import pandas as pd
import time

import tkinter as tk
from tkinter import Label
from tkinter import filedialog

# widgets = GUI elements: buttons, textboxes, labels, images
# windows = serves as a container to hold these widgets

window = Tk()  # instantiate an instance of a window
window.geometry("800x800")
window.title("StyleMatch")
label = Label(window,
              text="StyleMatch",
              fg= "#293366",
              font= ('Arial', 40, 'bold'),
              justify='left',
              bg ='white',
              padx=20,
              pady=20)
label.pack()


def browse():
    print("Please select your file")
    time.sleep(1)
    filelocation = askopenfilename()
    file_name = filelocation.split("/")[-1]
    print(file_name)
    files = {
        'file': (file_name, open(filelocation, 'rb')),
    }
    response = requests.post('https://file.io/', files=files)

    data = json.loads(response.text)

    if data["success"]:
        print("One use hyperlink with your file -> ", data["link"], " copied to your clipboard")
        print(filelocation)
        #img.save(file_name.split(".")[0] + ".png")
        df = pd.DataFrame([data["link"]])
        df.to_clipboard(index=False, header=False)


browse_button = Button(window,
                text="Browse Image",
                command=browse,
                font=("Arial", 30),
                fg= "#293366"
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
