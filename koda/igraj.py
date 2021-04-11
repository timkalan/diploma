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



def main(p1=Agent('p1', epsilon=0.05, alfa=0.05), 
         p2=Agent('p2', epsilon=0.05), 
         m=6,
         n=7,
         k=4,
         gravitacija=True,
         trening=True,
         epizode=10000,
         nalozi=False,
         nalozi_iz='333', 
         shrani=True, 
         shrani_v='674g',
         nasprotnik=Nakljucni('p2'), 
         strategija='674g',
         zacne=False):
    """
    p1 = Agent
    p2 = nasprotnik za namene treninga
    trening = treniramo ali samo igramo
    epizode = število iger, ki se odigrajo med treningom
    nasprotnik = tip igralca za igrati proti
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
        igra.treniraj(epizode, decay=True)
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

    #igranje
    p2 = nasprotnik
    igra = Okolje(p1, p2)

    if isinstance(p2, Agent):
        if zacne:
            p2.nalozi_strategijo(strategija + '-2') 
        else:
            p2.nalozi_strategijo(strategija) 

        p2.epsilon = 0
        a = igra.testiraj_sebi(st_iger=200)
        return a

    elif isinstance(p2, Clovek):
        a = igra.igraj_clovek(zacne)
        return a

    elif isinstance(p2, Nakljucni):
        a = igra.testiraj_nakljucni(st_iger=200, zacne=zacne)
        return a



if __name__ == '__main__':
    main()





# TODO: vse dobro dokumentiraj
# TODO: implementiraj nevronske mreže
# TODO: refaktorizacija
# TODO: treniraj proti drugim vrstam nasprotnika
# TODO: decaying epsilon 
# TODO: online trening ne dela!!
# TODO: pogled nazaj