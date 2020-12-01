from okolje import hiperparametri, Okolje
from agent import Agent, MonteCarlo, TD, SelfPlay


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



def main(p1=SelfPlay('p1', epsilon=0.01), 
         p2=Agent('p2', epsilon=0.1), 
         m=3,
         n=3,
         k=3,
         gravitacija=False,
         trening=True,
         epizode=1,
         nalozi=False,
         nalozi_iz='454g', 
         shrani=True, 
         shrani_v='333',
         nasprotnik=Clovek('p2'), 
         strategija='333',
         zacne=True):
    """
    p1 = Agent
    p2 = nasprotnik za namene treninga
    trening = treniramo ali samo igramo
    epizode = število iger, ki se odigrajo med treningom
    nasprotnik = tip igralca za igrati proti
    zacne = True, če začne agent in False sicer
    """
    p2 = p1
    # definiramo naše hiperparametre
    hiperparametri['VRSTICE'] = m
    hiperparametri['STOLPCI'] = n
    hiperparametri['V_VRSTO'] = k
    hiperparametri['GRAVITACIJA'] = gravitacija

    if trening:
        igra = Okolje(p1, p2)
        print('Treniram...')

        if nalozi:
            p1.nalozi_strategijo(nalozi_iz)

        igra.treniraj_self(epizode)
        #test = {k: -v for k, v in p2.vrednosti_stanj.items()}
        #p1.vrednosti_stanj.update(test)

        if shrani:
            p1.shrani_strategijo(shrani_v)

    #igraj
    p1.epsilon = 0
    p1.nalozi_strategijo(strategija)
    p2 = nasprotnik
    #p2.nalozi_strategijo('333-mc')

    igra = Okolje(p1, p2)
    igra.igraj_clovek(zacne)


if __name__ == '__main__':
    main()


# TODO: a je res dobra ideja da majo imena igralci
# TODO: implementiraj nek timer (mogoče je lahko dekorator)
# TODO: vse dobro dokumentiraj
# TODO: implementiraj boljše algoritme
# TODO: implementiraj nevronske mreže
# TODO: refaktorizacija
# TODO: online vs offline učenje
# TODO: treniraj proti drugim vrstam nasprotnika
# TODO: prepiši vse z numpy, da bo hitreje
# TODO: da en in isti agent igra oba igralca -> true self play; za P1 max, za P2 min
# TODO: decaying epsilon 