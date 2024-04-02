from tkinter import *
from tkinter.filedialog import askopenfilename
import time
from tkinter import Tk
from tkinter import Label
import filitering_and_synonym as f
import graph as g
from PIL import ImageTk, Image
import urllib.request
import io

from urllib.request import urlopen
import webbrowser

#
# def display_imgs(imgs: list) -> None:
#     """"""
#     for img in imgs:
#         imagelab = Label(window, image=img)
#         imagelab.pack()


def find_similar(description: str) -> list:
    """Find similar clothing items based on description and return the top 5 most similar as a
    list of Weighted Vertices."""
    global items  #TODO

    graph = g.load_clothing_items("data/store_zara_small_women.csv")
    user_vertex = graph.create_clothing_item(description)

    for vertex in graph.vertices:
        g.create_edge(graph, user_vertex.item_id, graph.vertices[vertex].item_id)

    top_items = user_vertex.get_ordered_neighbours()[:5]

    print([x.urls[0] for x in top_items])
    print([x.item_name for x in top_items])

    items = top_items
    return top_items


def start_program(filelocation: str) -> list:
    """Runs program."""
    global items   #TODO
    desc = f.user_image_description(filelocation)
    print(desc)
    items = find_similar(desc)
    update_labels()


def play_select_file():
    """Calls browse function with a delay"""
    time.sleep(0.1)
    browse()


def display_instructions():
    """Generates label that displays isntructions"""
    f = Frame(window, bg="#293366", width=30, height=30)
    f.pack()
    instruction = Label(f,
                        text="Welcome to StyleMatch! Upload a file of a clothing item\n"
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
    global items  # TODO: tempo

    time.sleep(0.1)
    filelocation = askopenfilename()
    try:
        with open(filelocation) as fl:
            file_name = filelocation.split("/")[-1]
            print(filelocation)
            """files = {
                'file': (file_name, open(filelocation, 'rb')),
            }
            response = requests.post('https://file.io/', files=files)

            data = json.loads(response.text)"""

            """if data["success"]:
                print("One use hyperlink with your file -> ", data["link"], " copied to your clipboard")
                print(filelocation)
                # img.save(file_name.split(".")[0] + ".png")
                df = pd.DataFrame([data["link"]])
                df.to_clipboard(index=False, header=False)"""

            start_program(filelocation)


    except FileNotFoundError:
        error.pack()

def update_labels() -> None:
    """

    """
    global items        # TODO
    global website_buttons
    global find_buttons
    global images

    for i in website_buttons:

        website_buttons[i].configure(text="smth" + str(i), command=lambda: open_website(items[i].website))
        open_website(items[i].website)
        print(items[i].website)

    for i in range(len(find_buttons)):
        find_buttons[i].config(command=lambda: find_similar(items[i].item_description))

    for i in range(len(find_buttons)):
        print(items[i].urls[1])
        data = urlopen(items[i].urls[1][1:])
        image = ImageTk.PhotoImage(data=data.read())
        image_width = image.width() // 10
        image_height = image.height() // 10
        image = ImageTk.getimage(image)
        image = image.resize((image_width, image_height))
        image = ImageTk.PhotoImage(image)

        label = images[i]
        label.config(image=image)
        label.image = image


def open_website(url: str):
    """
    take in website url and open it for the user
    """
    webbrowser.open_new_tab(url)


# if __name__ == "__main__":
# components/widgets
# video we used to learn tkinter: https://www.youtube.com/watch?v=TuLxsvK4svQ&t=455s

window = Tk()  # instantiate an instance of a window

window.geometry("800x800")
window.title("StyleMatch")
window.configure(bg='#e1e5e6')

items = []
website_buttons = {}
find_buttons = []
images = {}

frame1 = Frame(window)

for i in range(2):
    images[i] = Label(frame1, text="image"+str(i))
    website_buttons[i] = Button(frame1, text="button" + str(i))
    find_buttons.append(Button(frame1, text="find similar" + str(i)))
    images[i].pack(side=LEFT)
    website_buttons[i].pack(side=RIGHT)
    find_buttons[i].pack(side=LEFT)

frame1.pack()


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
