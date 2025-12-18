#TÜTT - Tartu Ülikooli Tudengi Turg
#Autorid: Juhan Simm, Tormi Arne Raidvere
#Mäng, mis simuleerib vähendatud ja lihtsustatud kujul aktsiaturgu.
#Mängu temaatika põhineb TÜ informaatika tudengile tuttavatel kohtadel ja õppeainetel.
#Kasutatud allikad: aktsiate tavalisemad muuttüübid/mustrid, firmade väärtuspõhised tüübid, w3schools (Tkinter), copilot ja mõõdukas koguses AI'd.

import tkinter as tk
#import matplotlib as plt
#import numpy as np
from PIL import Image, ImageTk
import random

def algus():
    #hiljem graafika???
    print("TÜTT - Juhan & Tormi")
    algscreen.pack_forget()
    main_screen.pack(fill="both", expand = True)
    
def järgmine_nädal():
    global nädal
    nädal += 1
    nädala_text.config(text=f"Nädal: {nädal}")
    hinnamuutus(stocks)
    uuenda_listi()
    
def show_main_screen():
    # eemaldame kõik vidinad
    for widget in root.winfo_children():
        widget.pack_forget()
    main_screen.pack(fill="both", expand=True)
    uuenda_listi()
#uuendame main sreeni aktsiate listi
def uuenda_listi():
    def vali_värv(esimene, teine):
        if esimene < teine:
            return "green"
        elif esimene > teine:
            return "red"
        else:
            return "white"
    global stocks, alg_portfoolio_väärtus
    for widget in veerg1.winfo_children():
        widget.destroy()
    for widget in veerg2.winfo_children():
        widget.destroy()
    #portfoolio väärtus nali
    portfoolio_väärtus_label.config(
    text=f"Portfoolio väärtus: {round(arvuta_portfoolio_väärtus(), 2)}€"
    )

    # võrdlus + värvimine
    uus_väärtus = arvuta_portfoolio_väärtus()
    portfoolio_väärtus_label.config(text=f"Portfoolio väärtus: {round(uus_väärtus, 2)}€")
    värv = vali_värv(alg_portfoolio_väärtus, uus_väärtus)
    portfoolio_väärtus_label.config(fg=värv)
    #jagame ja kirjutame aktsiad kahte veergu
    i = 0
    for el in stocks:
        if i % 2 == 0:
            veerg = veerg1
        else:
            veerg = veerg2
        värv = vali_värv(0, stocks[el]["protsent"])
        nimi = stocks[el]
        hind = nimi["hind"]
        kastike = tk.Label(
            veerg,
            borderwidth=1,
            relief="solid",
            bg = "#1A1A1A",
            fg = värv,
            height=4,
            width=25,
            text=f"{el}: {hind}€"
        )
        kastike.pack(pady=(16, 0))
        i += 1
    portfoolio_väärtus_label.config(text=f"{round(arvuta_portfoolio_väärtus(), 2)}€")
def samm_protsendiks(firmatüüp: str, samm):
    if samm == 2:
        return 0.0
    
    tvl, ekstreem = samm
    l, h = protsendid[firmatüüp][ekstreem]
    protsent = random.randint(l, h)
    return protsent if tvl == 1 else -protsent

#Leiab võimaluse, et ekstreemne muutus hinnas juhtub
def ekstreemne(firmatüüp):
    if firmatüüp == "LARGE":
        rand = random.randint(1, 500)
    elif firmatüüp == "MID":
        rand = random.randint(1, 200)
    elif firmatüüp == "SMALL":
        rand = random.randint(1, 100)
    elif firmatüüp == "PENNY":
        rand = random.randint(1, 50)
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
        protsent = nimi["protsent"]
        
        extrm = ekstreemne(firmatüüp)
        if extrm != None:
            muster = extrm
            samm = 0
            
        mustri_samm = mustrid[muster][samm]
        protsent = samm_protsendiks(firmatüüp, mustri_samm)
        uushind = round(hind * (1 + protsent / 100), 2)
        
        muster, samm = leiainfo(muster, samm)
        
        if uushind >= hind:
            tvl = 1
        else:
            tvl = 0
        if el in portfolio:
            portfolio[el]["Väärtus"] = round(portfolio[el]["Kogus"] * uushind, 2)
            portfolio[el]["protsent"] = protsent
        nimi["protsent"] = protsent
        nimi["hind"] = uushind
        nimi["TVL"] = tvl
        nimi["muster"] = muster
        nimi["samm"] = samm
            
    return aktsiad
def arvuta_portfoolio_väärtus():
    väärtus = 0
    for el in portfolio:
        väärtus += portfolio[el]["Väärtus"]
    return väärtus
def müü_aktsiaid():
    global taustapilt2_tk
    main_screen.pack_forget()
    taustapilt2 = Image.open("ekraan.png").resize((1280, 720), Image.Resampling.LANCZOS)
    taustapilt2_tk = ImageTk.PhotoImage(taustapilt2)

    kõik = tk.Canvas(root,
                    width=1280,
                    height=720,
                    borderwidth=1,
                    relief="solid")
    kõik.pack(fill="both", expand=True)
    kõik.create_image(0, 0, anchor='nw', image=taustapilt2_tk)

    info_label = tk.Label(kõik, text="Vali aktsia ja sisesta kogus:", bg="black", fg="white")
    info_label.pack(pady=(100, 0))

    protfoolio_var = tk.StringVar(root)
    try:
        protfoolio_var.set(list(portfolio.keys())[0])
    except IndexError:
        show_main_screen()
        #error popup
        viga_popup = tk.Toplevel(root)
        viga_popup.title("Viga")
        viga_label = tk.Label(viga_popup, text="Sul pole müüdavaid aktsiaid!", anchor="center")
        viga_label.pack(pady=20, padx=20)
        #okei nupp
        okei_nupp = tk.Button(viga_popup, text=":(", command=viga_popup.destroy)
        okei_nupp.pack(pady=10)
        return

    portfoolio_menu = tk.OptionMenu(kõik, protfoolio_var, *portfolio.keys())
    portfoolio_menu.pack(pady=10)
    portfoolio_menu.config(bg="black", fg="white", activebackground="grey", activeforeground="white")
    kogus = tk.Label(kõik, text="Kogus:", bg="black", fg="white")
    kogus.pack(pady=10)

    koguse_sisestus = tk.Entry(kõik)
    koguse_sisestus.pack(pady=10)

    viga = tk.Label(kõik, text="",bg="black", fg="red")
    viga.pack(pady=10)

    def müü():
        global raha, alg_portfoolio_väärtus
        valitud_aktsia = protfoolio_var.get()
        kogus = int(koguse_sisestus.get())
        hind = stocks[valitud_aktsia]["hind"]
        kokku_hind = hind * kogus

        if valitud_aktsia not in portfolio or kogus > portfolio[valitud_aktsia]["Kogus"]:
            viga.config(text="Sul pole piisavalt aktsiaid!")
        else:
            raha += kokku_hind
            raha_kogus.config(text=f"Raha: {round(raha, 2)}€")
            portfolio[valitud_aktsia]["Kogus"] -= kogus
            portfolio[valitud_aktsia]["Väärtus"] -= kokku_hind
            viga.config(text="Müük edukas!", fg="green")
            if portfolio[valitud_aktsia]["Kogus"] == 0:
                del portfolio[valitud_aktsia]
            alg_portfoolio_väärtus = arvuta_portfoolio_väärtus()
            show_main_screen()

    müü_nupp = tk.Button(kõik,bg="black", fg="white", text="Müü", command=müü)
    müü_nupp.pack(pady=10)

    tagasi_nupp = tk.Button(kõik, text="Tagasi",bg="black",fg="white", command=show_main_screen)
    tagasi_nupp.pack(pady=10)

def osta_aktsiaid():
    global taustapilt2_tk
    main_screen.pack_forget()
    taustapilt2 = Image.open("ekraan.png").resize((1280, 720))
    taustapilt2_tk = ImageTk.PhotoImage(taustapilt2)
    kõik = tk.Canvas(root,
                    width=1280,
                    height=720,
                    borderwidth=1,
                    relief="solid")
    kõik.pack(fill="both", expand=True)
    kõik.create_image(0, 0, anchor='nw', image=taustapilt2_tk)

    info_label = tk.Label(kõik, text="Vali aktsia ja sisesta kogus:", bg="black", fg="white")
    info_label.pack(pady=(100, 0))
    
    aktsia_var = tk.StringVar(kõik)
    aktsia_var.set(list(stocks.keys())[0])
    
    menu = tk.OptionMenu(kõik, aktsia_var, *stocks.keys())
    menu.pack(pady=10)
    menu.config(bg="black", fg="white", activebackground="grey", activeforeground="white")
    kogus = tk.Label(kõik, text="Kogus:", bg="black", fg="white")
    kogus.pack(pady=10)
    
    koguse_sisestus = tk.Entry(kõik)
    koguse_sisestus.pack(pady=10)
    
    viga = tk.Label(kõik, text="",bg="black", fg="red")
    viga.pack(pady=10)

    
    def osta():
        global raha, alg_portfoolio_väärtus
        valitud_aktsia = aktsia_var.get()
        kogus = int(koguse_sisestus.get())
        hind = stocks[valitud_aktsia]["hind"]
        kokku_hind = hind * kogus
        
        if kokku_hind > raha:
            viga.config(text="Sul pole piisavalt raha!")
        else:
            raha -= kokku_hind
            raha_kogus.config(text=f"Raha: {round(raha, 2)}€")
            if valitud_aktsia not in portfolio:
                portfolio[valitud_aktsia] = {"Kogus": 0, "Väärtus": 0}
                portfolio[valitud_aktsia]["protsent"] = 0
            portfolio[valitud_aktsia]["Kogus"] += kogus
            portfolio[valitud_aktsia]["Väärtus"] += kokku_hind
            viga.config(text="Ost edukas!", fg="green")
            alg_portfoolio_väärtus = arvuta_portfoolio_väärtus()
            show_main_screen()
    
    osta_nupp = tk.Button(kõik, text="Osta",bg="black", fg="white", command=osta)
    osta_nupp.pack(pady=10)
    tagasi_nupp = tk.Button(kõik, text="Tagasi",bg="black", fg="white", command=show_main_screen)
    tagasi_nupp.pack(pady=10)

def vaata_portfooliot():
    global taustapilt2_tk
    main_screen.pack_forget()
    taustapilt2 = Image.open("ekraan.png").resize((1280, 720))
    taustapilt2_tk = ImageTk.PhotoImage(taustapilt2)
    kõik = tk.Canvas(root, 
                    width=1280,
                    height=720,
                    borderwidth=1,
                    relief="solid")
    kõik.pack(fill="both", expand=True)
    kõik.create_image(0, 0, anchor='nw', image=taustapilt2_tk)
    info_label = tk.Label(kõik, text="Sinu portfoolio:", bg="black", fg="white")
    info_label.pack(pady=(100, 0))
    
    for aktsia, info in portfolio.items():
        kogus = info["Kogus"]
        väärtus = round(info["Väärtus"], 2)
        muut = info["protsent"]
        if muut <= 0:
            muut = f"{abs(muut)}% \u2193"
        elif muut > 0:
            muut = f"{muut}% \u2191"
        aktsia_label = tk.Label(kõik, text=f"{aktsia}: Kogus: {kogus}, Väärtus: {väärtus}€, Muutus: {muut}", bg="black", fg="white")
        aktsia_label.pack()
    
    tagasi_nupp = tk.Button(kõik, text="Tagasi", command=show_main_screen, bg = "black", fg = "white")
    tagasi_nupp.pack(pady=10)
    
#Muutujad
nädal = 1
raha = 1000
net_worth = 0
alg_portfoolio_väärtus = 0

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
                          "firmatüüp": jrj[5],
                          "protsent": 0}
        
#Portfoolio
#Muutujad: {"aktsia nimi": int(hulk)}
portfolio = {}

#Mitu protsenti iga firmatüüpi aktsia hind tõuseb
#[(alampiir, ülempiir), (suur_alampiir, suur_ülempiir)]
protsendid = {
"LARGE": [(1, 4), (5, 10)],
"MID": [(2, 6), (7, 15)],
"SMALL": [(3, 10), (10, 20)],
"PENNY": [(20, 50), (50, 60)]
}

#Formaat: [(TVL/jääb samaks(2), väike/suur muutus)]
mustrid = {
#Tõus + langus (algab tõusuga, lõppeb langusega)
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
"EX2_LITE": [(0, 1), (1, 0)],
#Lihtsalt tõus - 1 nädal
"T6US": [(1,1)],
"T6US_LITE": [(1,0)]
}

#Mitu nädalat kestab muster (5 = 6 nädalat, 0 = 1 nädal)
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
    "T6US": 0,
    "T6US_LITE": 0
}

#Järgmine muster, ehk igale olemasolevale mustrile mustrid, mis võivad järgneda
järgminemuster = {
    "HNS": ["CNH", "DBB", "W", "DST", "T6US", "T6US_LITE"],
    "DBT": ["CNH", "DBB", "W", "DST", "T6US", "T6US_LITE"],
    "CNH": ["HNS", "DBT", "F", "AST", "T6US", "T6US_LITE"],
    "DBB": ["HNS", "DBT", "F", "AST", "T6US", "T6US_LITE"],
    "F":   ["F", "AST", "HNS", "DBT", "T6US", "T6US_LITE"],
    "AST": ["F", "AST", "HNS", "DBT", "T6US", "T6US_LITE"],
    "W":   ["W", "DST", "CNH", "DBB", "T6US", "T6US_LITE"],
    "DST": ["W", "DST", "CNH", "DBB", "T6US", "T6US_LITE"],
    "EX1": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"],
    "EX1_LITE": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"],
    "EX2": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"],
    "EX2_LITE": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"],
    "T6US": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"],
    "T6US_LITE": ["HNS", "DBT", "CNH", "DBB", "F", "AST", "W", "DST", "T6US", "T6US_LITE"]
}
    
#mängu aken

root = tk.Tk()
root.title("TÜTT")
root.geometry("1280x720")
root.resizable(False, False)

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
#Keskmine ala
taustapilt = Image.open("TYTT_taust.png").resize((1280, 600), Image.Resampling.LANCZOS)
taustapilt_tk = ImageTk.PhotoImage(taustapilt)
keskmine_ala = tk.Canvas(
    main_screen,
    width=1280,
    height=600,
    borderwidth=1,
    relief="solid"
)
keskmine_ala.pack(fill="both", expand=True)
keskmine_ala.create_image(0, 0, anchor='nw', image=taustapilt_tk)
#Portfoolio väärtus
portfoolio_väärtus_label = tk.Label(
    keskmine_ala,
    text=f"Portfoolio väärtus: {net_worth}€",
    bg="#1A1A1A",
    fg="white",
    width=21,
    height=4,
)
portfoolio_väärtus_label.pack(side='right', anchor='se', padx=20, pady=185) 
# Esimene veerg
veerg1 = tk.Label(keskmine_ala, bg="#3A322E")
veerg1.pack(side='left', anchor='n', padx=24, pady=5)
# Teine veerg
veerg2 = tk.Label(keskmine_ala, bg="#3A322E")
veerg2.pack(side='left', anchor='n', padx=5, pady=5)
uuenda_listi()
#nädal ja raha
nädala_text = tk.Label(ülemine_bar,
    text=f"Nädal: {nädal}",
    font=("Arial", 16)
    )
nädala_text.pack(side = "right",padx = 10)
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
#Järgmise nädala nupp
järgmine_nädal = tk.Button(
    alumine_bar,
    text = "Mine magama",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = järgmine_nädal
    )
järgmine_nädal.pack(side = "right", padx = 10)
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
# Müü nupp
müü_nupp = tk.Button(
    all_vasakul,
    text = "Müü aktsiaid",
    font = ("Arial", 18),
    width = 15,
    height = 2,
    command = müü_aktsiaid
)
müü_nupp.pack(side = "left", padx = 10)
root.mainloop()
