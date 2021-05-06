import time
import numpy as np

from okolje import hiperparametri, Okolje
from agent import Agent, MonteCarlo, TD, TDn, AgentLin


class Clovek:
    """
    Predstavlja človeškega igralca v igri.
    """

    def __init__(self, ime):
        self.ime = ime


    def izberi_akcijo(self, legalne, naravno=True):
        """
        Dovoli človeku, da izbere akcijo, ki jo poda kot
        dve številki. Nato preverimo, če je akcija legalna
        in jo igramo.
        """
        while True:
            vrstica = int(input('Izberi vrstico: '))
            stolpec = int(input('Izberi stolpec: '))

            akcija = (vrstica, stolpec)

            if naravno:
                akcija = (vrstica - 1, stolpec - 1)

            if akcija in legalne:
                return akcija



class Nakljucni:
    """
    Igralec, ki se vede naključno. Uporaben za namene testiranja in treniranja.
    """

    def __init__(self, ime):
        self.ime = ime


    def izberi_akcijo(self, pozicije):
        """
        Enostavno pridobi seznam vseh legalnih pozicij in izbere naključno.
        """
        indeks =  np.random.choice(len(pozicije))
        akcija = pozicije[indeks]
        return akcija



#class Minimax():
#    pass



def main(p1=AgentLin('p1', epsilon=0.05, alfa=0.2), 
         p2=AgentLin('p2', epsilon=0.05, alfa=0.2), 
         m=3,
         n=3,
         k=3,
         gravitacija=False,
         trening=True,
         epizode=50000,
         nalozi=False,
         nalozi_iz='333', 
         shrani=True, 
         shrani_v='333lin',
         nasprotnik=Nakljucni('p2'), 
         strategija='333lin',
         zacne=True):
    """
    p1 = Agent
    p2 = nasprotnik za namene treninga
    m, n, k = specifikacije igre
    gravitacija = pomožno dodamo pogoje iz connect-4
    trening = treniramo ali samo igramo
    epizode = število iger, ki se odigrajo med treningom
    nalozi, nalozi_iz = pomožno predhodno naložimo strategijo
    shrani, shrani_v = ali želimo shraniti stratecijo
    nasprotnik = tip igralca za testiranje
    strategija = katero strategijo uporabi
    zacne = True, če začne agent in False sicer
    """

    # definiramo naše hiperparametre
    hiperparametri['VRSTICE'] = m
    hiperparametri['STOLPCI'] = n
    hiperparametri['V_VRSTO'] = k
    hiperparametri['GRAVITACIJA'] = gravitacija

    if trening:
        if nalozi:
            p1.nalozi_strategijo(nalozi_iz)
            p2.nalozi_strategijo(nalozi_iz + '-2')

        igra = Okolje(p1, p2)
        tik = time.perf_counter()
        igra.treniraj(epizode, decay=False)
        tok = time.perf_counter()

        # izmerimo čas treniranja
        print(f'\nTrening je trajal: {tok - tik} sekund')

        if shrani:
            p1.shrani_strategijo(shrani_v)
            p2.shrani_strategijo(shrani_v + '-2')

    #pripravimo p1 na igro
    p1.epsilon = 0

    # naložimo ustrezno strategijo
    if zacne:
        p1.nalozi_strategijo(strategija)
    else:
        p1.nalozi_strategijo(strategija + '-2')

    ##igranje
    p2 = nasprotnik
    igra = Okolje(p1, p2)

    # pripravimo igro glede na tip nasprotnika
    if isinstance(p2, Agent):
        if zacne:
            p2.nalozi_strategijo(strategija + '-2') 
        else:
            p2.nalozi_strategijo(strategija) 

        p2.epsilon = 0
        a = igra.testiraj_sebi(st_iger=10)
        return a

    elif isinstance(p2, Clovek):
        a = igra.igraj_clovek(zacne)
        return a

    elif isinstance(p2, Nakljucni):
        a = igra.testiraj_nakljucni(st_iger=1000, zacne=zacne)
        return a



if __name__ == '__main__':
    main()





# TODO: vse dobro dokumentiraj
# TODO: implementiraj nevronske mreže
# TODO: refaktorizacija
# TODO: treniraj proti drugim vrstam nasprotnika
# TODO: online trening ne dela!!