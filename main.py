import tkinter as tk
from PIL import Image, ImageTk
import random

#Muutujad
päev = 1
raha = 1000

#Aktsiaturg
stocks = {
    "Test": {
        "hind": 10,
    },
    
    
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
def osta_aktsiaid():
    osta_aken = tk.Toplevel(root)
    osta_aken.title("Osta aktsiaid")
    osta_aken.geometry("400x300")
    
    info_label = tk.Label(osta_aken, text="Vali aktsia ja sisesta kogus:")
    info_label.pack(pady=10)
    
    stock_var = tk.StringVar(osta_aken)
    stock_var.set(list(stocks.keys())[0])
    
    stock_menu = tk.OptionMenu(osta_aken, stock_var, *stocks.keys())
    stock_menu.pack(pady=10)
    
    quantity_label = tk.Label(osta_aken, text="Kogus:")
    quantity_label.pack(pady=10)
    
    quantity_entry = tk.Entry(osta_aken)
    quantity_entry.pack(pady=10)
    
    def osta():
        global raha
        valitud_aktsia = stock_var.get()
        kogus = int(quantity_entry.get())
        hind = stocks[valitud_aktsia]["hind"]
        kokku_hind = hind * kogus
        
        if kokku_hind > raha:
            viga_label.config(text="Sul pole piisavalt raha!")
        else:
            raha -= kokku_hind
            raha_kogus.config(text=f"Raha: {raha}€")
            portfolio[valitud_aktsia] = portfolio.get(valitud_aktsia, 0) + kogus
            osta_aken.destroy()
    
    osta_nupp = tk.Button(osta_aken, text="Osta", command=osta)
    osta_nupp.pack(pady=10)
    
    viga_label = tk.Label(osta_aken, text="", fg="red")
    viga_label.pack(pady=10)
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
raha_kogus = tk.Label(main_screen, text=f"Raha: {raha}€", font=("Arial", 16))
raha_kogus.pack(anchor="nw", padx = 10, pady = 10)
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
#Osta nupp
osta_nupp = tk.Button(
    main_screen,
    text = "Osta",
    font = ("Arial", 18),
    width = 20,
    height = 20,
    command = osta_aktsiaid
    )
osta_nupp.pack(anchor = "sw", padx = 10, pady = 10)
root.mainloop()