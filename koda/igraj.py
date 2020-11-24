from okolje import hiperparametri, Okolje
from agent import Agent, MonteCarlo, TD


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
            if naravno:
                vrstica = int(input('Izberi vrstico: ')) - 1
                stolpec = int(input('Izberi stolpec: ')) - 1

            else:
                vrstica = int(input('Izberi vrstico: '))
                stolpec = int(input('Izberi stolpec: '))

            akcija = (vrstica, stolpec)
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



def main(p1=Agent('p1', epsilon=0.01), 
         p2=Agent('p2', epsilon=0.1), 
         trening=False,
         epizode=5000,
         nalozi=False,
         nalozi_iz='454g', 
         shrani=True, 
         shrani_v='333g',
         nasprotnik=Clovek('Tim'), 
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
    if trening:
        igra = Okolje(p1, p2)
        print('Treniram...')

        if nalozi:
            p1.nalozi_strategijo(nalozi_iz)

        igra.treniraj(epizode)

        if shrani:
            p1.shrani_strategijo(shrani_v)

    #igraj
    p1.epsilon = 0
    p1.nalozi_strategijo(strategija)
    p2 = nasprotnik
    #p2.nalozi_strategijo('333-mc')

    igra = Okolje(p1, p2)
    igra.igraj_clovek()


if __name__ == '__main__':
    main()