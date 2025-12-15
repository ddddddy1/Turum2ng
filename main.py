import tkinter as tk
#import matplotlib as plt
#import numpy as np
from PIL import Image, ImageTk
import random

#Muutujad
päev = 1
raha = 1000

#Aktsiaturg
#Muutujad: {"aktsia nimi": {"hind": 00.00, "TVL": 0, "muster": "HNS", "firmatüüp": "MC"}}
stocks = {}

with open("aktsiad.txt", "r", encoding = "UTF-8") as fail:
    for rida in fail:
        jrj = rida.strip().split(";")
        stocks[jrj[0]] = {"hind": float(jrj[1]),
                          #"TVL": int(jrj[2]),
                          #"muster": jrj[3],
                          #"firmatüüp": jrj[4]
                          }
        
#Portfoolio
#Muutujad: {"aktsia nimi": int(hulk)}
portfolio = {}

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
def show_main_screen():
    # Puhastame ja taastame peamise sisu
    for widget in root.winfo_children():
        widget.pack_forget()
    main_screen.pack(fill="both", expand=True)
    # Võid lisada ka teisi nuppe või sisu vastavalt vajadusele
def osta_aktsiaid():
    main_screen.pack_forget()
    info_label = tk.Label(root, text="Vali aktsia ja sisesta kogus:")
    info_label.pack(pady=10)
    
    stock_var = tk.StringVar(root)
    stock_var.set(list(stocks.keys())[0])
    
    stock_menu = tk.OptionMenu(root, stock_var, *stocks.keys())
    stock_menu.pack(pady=10)
    
    quantity_label = tk.Label(root, text="Kogus:")
    quantity_label.pack(pady=10)
    
    quantity_entry = tk.Entry(root)
    quantity_entry.pack(pady=10)
    
    viga_label = tk.Label(root, text="", fg="red")
    viga_label.pack(pady=10)

    
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
            portfolio[valitud_aktsia] = {"Kogus": 0, "Väärtus": 0}
            portfolio[valitud_aktsia]["Kogus"] += kogus
            portfolio[valitud_aktsia]["Väärtus"] += kokku_hind
            viga_label.config(text="Ost edukas!", fg="green")

            show_main_screen()
    
    osta_nupp = tk.Button(root, text="Osta", command=osta)
    osta_nupp.pack(pady=10)
    tagasi_nupp = tk.Button(root, text="Tagasi", command=show_main_screen)
    tagasi_nupp.pack(pady=10)

def vaata_portfooliot():
    main_screen.pack_forget()
    info_label = tk.Label(root, text="Sinu portfoolio:")
    info_label.pack(pady=10)
    
    for aktsia, info in portfolio.items():
        kogus = info["Kogus"]
        väärtus = info["Väärtus"]
        aktsia_label = tk.Label(root, text=f"{aktsia}: Kogus: {kogus}, Väärtus: {väärtus}€")
        aktsia_label.pack()
    
    tagasi_nupp = tk.Button(root, text="Tagasi", command=show_main_screen)
    tagasi_nupp.pack(pady=10)
#mängu aken

root = tk.Tk()
root.title("TÜTT")
root.geometry("1280x720")

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
#Alumine bar
alumine_bar = tk.Frame(
    main_screen,
    borderwidth=1,
    relief="solid"
    )
alumine_bar.pack(side="bottom", fill="x")
#Alumine vasak
all_vasakul = tk.Frame(
    alumine_bar
)
all_vasakul.pack(side="left", fill="x")
#Ülemine bar
ülemine_bar = tk.Frame(
    main_screen,
    borderwidth=1,
    relief="solid"
    )
ülemine_bar.pack(side = "top", fill="x")
#päev ja raha
päeva_text = tk.Label(ülemine_bar,
    text=f"Päev: {päev}",
    font=("Arial", 16)
    )
päeva_text.pack(side = "right",padx = 10)
raha_kogus = tk.Label(ülemine_bar,
    text=f"Raha: {raha}€",
    font=("Arial", 16)
    )
raha_kogus.pack(side = "left", padx = 10)
#Pilt ülemisel ribal
image = Image.open("logo.png")
image = image.resize((64, 64))
logo_pilt = ImageTk.PhotoImage(image)
logo = tk.Label(ülemine_bar, image = logo_pilt)
logo.pack(anchor = "n")
#Järgmise päeva nupp
järgmine_päev = tk.Button(
    alumine_bar,
    text = "Mine magama",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = järgmine_päev
    )
järgmine_päev.pack(side = "right", padx = 10)
#Osta nupp
osta_nupp = tk.Button(
    all_vasakul,
    text = "Osta aktsiaid",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = osta_aktsiaid
    )
osta_nupp.pack(side = "left", padx = 10)
#Portfoolio nupp
portfoolio_nupp = tk.Button(
    all_vasakul,
    text = "Vaata portfooliot",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = vaata_portfooliot,
)
portfoolio_nupp.pack(side = "right", padx = 10)
root.mainloop()