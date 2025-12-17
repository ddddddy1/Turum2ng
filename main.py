import tkinter as tk
#import matplotlib as plt
#import numpy as np
from PIL import Image, ImageTk
import random

#Muutujad
päev = 1
raha = 1000

#Aktsiaturg
#Nt: {"aktsia nimi": {"hind": 00.00, "TVL": 0, "muster": "HNS", "samm": 5, "firmatüüp": "MID"}}
stocks = {}

with open("aktsiad.txt", "r", encoding = "UTF-8") as fail:
    for rida in fail:
        jrj = rida.strip().split(";")
        stocks[jrj[0]] = {"hind": float(jrj[1]),
                          "TVL": int(jrj[2]),
                          "muster": jrj[3],
                          "samm": int(jrj[4]),
                          "firmatüüp": jrj[5]}
        
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
    
def samm_protsendiks(firmatüüp: str, samm):
    if samm == 2:
        return 0.0
    
    tvl, ekstreem = samm
    l, h = protsendid[firmatüüp][ekstreem]
    protsent = random.randint(l, h)
    return protsent if tvl == 1 else -protsent
    
def ekstreemne(firmatüüp):
    if firmatüüp == "LARGE":
        rand = random.randint(1, 500)
    elif firmatüüp == "MID":
        rand = random.randint(1, 200)
    elif firmatüüp == "SMALL":
        rand = random.randint(1, 100)
    elif firmatüüp == "PENNY":
        rand = random.randint(1, 33)
    if rand == 17:
        rand_ex = random.randint(1, 4)
        if rand_ex == 1:
            return "EX1"
        elif rand_ex == 2:
            return "EX1_LITE"
        elif rand_ex == 3:
            return "EX2"
        elif rand_ex == 4:
            return "EX2_LITE"
    else:
        return None
    
def leiainfo(muster, samm):
    max_samm = mustripikkus.get(muster)

    if samm >= max_samm:
        samm = 0
        muster = random.choice(järgminemuster[muster])
    else:
        samm += 1
    return muster, samm

def hinnamuutus(aktsiad):
    for el in aktsiad:
        nimi = aktsiad[el]
        hind = nimi["hind"]
        tvl = nimi["TVL"]
        muster = nimi["muster"]
        samm = nimi["samm"]
        firmatüüp = nimi["firmatüüp"]
        
        extrm = ekstreemne(firmatüüp)
        if extrm != None:
            muster = extrm
            samm = 0
        
        muster, samm = leiainfo(muster, samm)
            
        mustri_samm = mustrid[muster][samm]
        protsent = samm_protsendiks(firmatüüp, mustri_samm)
        uushind = round(hind * (1 + protsent / 100), 2)
        
        if uushind >= hind:
            tvl = 1
        else:
            tvl = 0
        
        nimi["hind"] = uushind
        nimi["TVL"] = tvl
        nimi["muster"] = muster
        nimi["samm"] = samm
            
    return aktsiad
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

protsendid = {
"LARGE": [(1, 4), (5, 10)],
"MID": [(2, 6), (7, 15)],
"SMALL": [(3, 10), (10, 20)],
"PENNY": [(20, 50), (50, 60)]
}

#[(TVL/jääb samaks(2), väike/suur muutus)]
mustrid = {
#Tõus + langus
"HNS": [(1, 0), (0, 0), (1, 1), (0, 1), (1, 0), (0, 0)], #6 nädalat
"DBT": [(1, 1), (0, 0), (1, 0), (0, 1)], #4 nädalat
#Langus + tõus - 4 nädalat
"CNH": [(0, 1), 2, (1, 1), (0, 0)],
"DBB": [(0, 1), (1, 0), (0, 0), (1, 1)],
#Tõus + tõus - 5 nädalat
"F": [(1, 1), (0, 0), (1, 0), (0, 0), (1, 1)],
"AST": [(1, 1), (0, 0), (1, 0), (0, 0), (1, 0)],
#Langus + langus - 5 nädalat
"W": [(0, 1), (1, 0), (0, 0), (1, 0), 2],
"DST": [(0, 1), (1, 0), (0, 0), 2, 2],
#Ekstreemne tõus + langus (+laugem) - 2 nädalat
"EX1": [(1, 1), (0, 1)],
"EX1_LITE": [(1, 1), (0, 0)],
#Ekstreemne langus + tõus (+laugem) - 2 nädalat
"EX2": [(0, 1), (1, 1)],
"EX2_LITE": [(0, 1), (1, 0)]
}

mustripikkus = {
    "HNS": 5,
    "DBT": 3,
    "CNH": 3,
    "DBB": 3,
    "F":   4,
    "AST": 4,
    "W":   4,
    "DST": 4,
    "EX1": 1,
    "EX1_LITE": 1,
    "EX2": 1,
    "EX2_LITE": 1,
}

järgminemuster = {
    "HNS": ["CNH", "DBB", "W", "DST"],
    "DBT": ["CNH", "DBB", "W", "DST"],
    "CNH": ["HNS", "DBT", "F", "AST"],
    "DBB": ["HNS", "DBT", "F", "AST"],
    "F":   ["F", "AST", "HNS", "DBT"],
    "AST": ["F", "AST", "HNS", "DBT"],
    "W":   ["W", "DST", "CNH", "DBB"],
    "DST": ["W", "DST", "CNH", "DBB"]
}
    
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