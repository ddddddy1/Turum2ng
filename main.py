import tkinter as tk
from PIL import Image, ImageTk
import random

#Muutujad
päev = 1
raha = 1000

#Aktsiaturg
stocks = {
    
    
    
}

#Portfolio
portfolio = {
    
    
    
}

def algus():
    #hiljem graafika???
    print("TÜTT - Juhan & Tormi")
    algscreen.pack_forget()
    main_screen.pack(fill="both", expand = True)
def järgmine_päev():
    global päev
    päev += 1
    päeva_text.config(text=f"Päev: {päev}")
    update()
def update(): #refreshib UI (päev, raha, aktsiaturg...)
    pass
#mängu aken
root = tk.Tk()
root.title("TÜTT")
root.geometry("600x400")

#Algne screen
algscreen = tk.Frame(root)
algscreen.pack(fill="both", expand=True)

tervitus  = tk.Label(
    algscreen,
    text="Teretulemast TÜTTi",
    font=("Arial", 18),
    width = 15,
    height = 2,
    )
tervitus.pack(pady=80)

algus_nupp = tk.Button(
    algscreen,
    text="Alusta",
    font=("Arial", 18),
    width = 15,
    height = 2,
    command=algus
    )
algus_nupp.pack(pady=20)
# Main screen
main_screen = tk.Frame(root)
päeva_text = tk.Label(main_screen, text=f"Päev: {päev}", font=("Arial", 16))
päeva_text.pack(anchor="ne",padx = 10, pady = 10)
#Pilt main screenil
image = Image.open("logo.png")
image = image.resize((128, 128))
logo_pilt = ImageTk.PhotoImage(image)
logo = tk.Label(main_screen, image = logo_pilt)
logo.pack(pady=20)
#Järgmise päeva nupp
järgmine_päev = tk.Button(
    main_screen,
    text = "Mine magama",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = järgmine_päev
    )
järgmine_päev.pack(anchor = "se", padx = 10, pady = 10)
root.mainloop()