from tkinter import *
import requests
from tkinter.filedialog import askopenfilename
import json
import pandas as pd
import time
from tkinter import Tk, font
from tkinter import Label
import filitering_and_synonym as f
from PIL import Image, ImageTk
import graph as g


# video we used to learn tkinter: https://www.youtube.com/watch?v=TuLxsvK4svQ&t=455s

window = Tk()  # instantiate an instance of a window
window.geometry("800x800")
window.title("StyleMatch")
window.configure(bg='#e1e5e6')


def play_select_file():
    """Calls browse function with a delay"""
    time.sleep(0.1)
    browse()


def display_instructions():

    """Generates label that displays isntructions"""
    f = Frame(window, bg="#293366", width=30, height=30)
    f.pack()
    instruction = Label(f,
                        text="Welcome to StyleMatch! Upload a file of a clothing item "
                             "you want to find a similar item for. ",
                        fg="#bf4343",
                        font=('Avenir Next', 20),
                        anchor='w',
                        justify='center',
                        bg="#e1e5e6",
                        padx=20,
                        pady=40)
    instruction.pack()


def browse():
    """
    source: https://dev.to/jairajsahgal/creating-a-file-uploader-in-python-18e0
    """
    time.sleep(0.1)
    filelocation = askopenfilename()
    try:
        with open(filelocation) as fl:
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
                start_program(filelocation)

    except FileNotFoundError:
        error.pack()


# components/widgets
title = Label(window,
              text="StyleMatch",
              fg="#293366",
              font=('Avenir Next', 80, 'bold'),
              anchor='center',
              justify='center',
              bg='white',
              padx=20,
              pady=20)

title.pack(padx=50, pady=60)

select_file = Label(window,
                    text="Please select your file. Must be type .jpg, .jpeg, or .png",
                    fg="#293366",
                    font=('Avenir Next Thin', 20),
                    anchor='center',
                    justify='center',
                    padx=20,
                    pady=60,
                    bg="#e1e5e6")

browse_button = Button(window,
                       width=15,
                       text="Browse Image",
                       command=play_select_file,
                       font=("Avenir Next", 30),
                       fg="#293366",
                       justify='left',
                       padx=-30,
                       )

instructions = Button(window,
                      width=15,
                      text="Instructions",
                      command=display_instructions,
                      font=("Avenir Next", 30),
                      fg="#293366",
                      justify='right',
                      padx=-30,
                      )

browse_button.pack(), instructions.pack()
select_file.pack()
error = Label(window,
              text="File not valid. Please try again!",
              fg="#bf4343",
              font=('Avenir Next', 20),
              anchor='center',
              justify='center',
              bg="#e1e5e6",
              padx=20,
              pady=40)



"""save_button = Button(window,
                text="Upload",
                command=click,
                font=("Arial", 30),
                fg= "#293366",
                width=50
                )"""

window.mainloop()  # place window on computer screen, listen for events


def start_program(filelocation: str):
    """Runs program."""
    graph = g.load_clothing_items("data/store_zara_small_women.csv")
    desc = f.user_image_description(filelocation)
    user_vertex = graph.create_clothing_item(desc)

    for vertex in graph.vertices:
        g.create_edge(graph, user_vertex.item_id, graph.vertices[vertex].item_id)

    top_items = user_vertex.get_ordered_neighbours()[:5]
    [print(x.item_description) for x in top_items]
