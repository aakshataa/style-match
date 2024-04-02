import tkinter as tk
import urllib.request
#import base64
import io
from PIL import ImageTk, Image

root = tk.Tk()
root.title("Weather")

link = "https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png"

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image

img = WebImage(link).get()
imagelab = tk.Label(root, image=img)
imagelab.grid(row=0, column=0)

root.mainloop()
