import pickle
import os
import numpy as np
from okolje import hiperparametri 

from mreza import Mreza


class Agent:
    """
    To je računalniški igralec; mora si shranjevati stanja, 
    jih ocenjevati in posodabljati ob koncu igre. Mora tudi
    shraniti strategijo.
    """

    def __init__(self, ime, epsilon=0.3, alfa=0.2):
        """
        Agent mora beležiti vsa raziskana stanja v epizodi in 
        posodabljati vrednosti teh stanj. 

        epsilon = verjetnost da naredi naključno potezo (raziskuje)
        gama = diskontni faktor
        alfa = hitrost učenja (learning rate)
        """
        self.ime = ime
        self.stanja = []            # beleži vsa stanja
        self.epsilon = epsilon
        self.alfa = alfa

        # začnemo s prazno - izogib prevelikim tabelam
        self.vrednosti_stanj = {}   # stanje -> vrednost

    
    def izberi_akcijo(self, pozicije, stanje, simbol):
        """
        epsilon-požrešno izbere akcijo in jo vrne.

        pozicije = možne pozicije, ki jih lahko igramo
        """
        # izberemo naključno
        if np.random.uniform(0, 1) <= self.epsilon:
            indeks =  np.random.choice(len(pozicije))
            akcija = pozicije[indeks]

        else:
            najvecja_vrednost = -10
            for pozicija in pozicije:
                naslednje_stanje = stanje.copy()
                naslednje_stanje[pozicija] = simbol
                naslednji = self.pridobi_stanje(naslednje_stanje)

                if self.vrednosti_stanj.get(naslednji) is None:
                    #vrednost = 0 
                    vrednost = np.random.uniform(-1, 1)
                    #vrednost = 0.5
                else:
                    vrednost = self.vrednosti_stanj.get(naslednji)

                if vrednost >= najvecja_vrednost:
                    najvecja_vrednost = vrednost
                    akcija = pozicija
        
        return akcija


    def pridobi_stanje(self, plosca):
        """
        Agent mora dobiti stanje od plošče in ga spremeniti v
        njemu razumljivo obliko.
        """
        plosca = str(plosca.reshape(hiperparametri['VRSTICE'] * hiperparametri['STOLPCI']))
        return plosca


    def dodaj_stanje(self, stanje):
        self.stanja.append(stanje)


    def nagradi(self, nagrada):
        """
        Po koncu igre se posodobijo vrednosti stanj od zadaj naprej
        po pravilu spodaj. Za vrednost zadnjega stanja (ki ni dejansko 
        stanje) je vrednost kar nagrada.

        vrednost = vrednost + alfa * (gama * vrednost(naslednji) - vrednost)
        """
        for stanje in reversed(self.stanja):
            # poskrbimo za primer, ko stanja še nismo videli
            if self.vrednosti_stanj.get(stanje) is None:
                self.vrednosti_stanj[stanje] = 0
                #self.vrednosti_stanj[stanje] = np.random.uniform(-1, 1)

            self.vrednosti_stanj[stanje] += self.alfa * (
                nagrada - self.vrednosti_stanj[stanje])

            nagrada = self.vrednosti_stanj[stanje]


    def nagradi_online(self):
        """
        Agent lahko posodobi svoje vrednosti stanj kar med igro.
        """
        if len(self.stanja) > 1:
            zadnje, predzadnje = self.stanja[-1], self.stanja[-2]

            # poskrbimo za primer, ko stanja še nismo videli
            if (self.vrednosti_stanj.get(predzadnje) is None) or (
                self.vrednosti_stanj.get(zadnje) is None):
                self.vrednosti_stanj[predzadnje] = 0
                self.vrednosti_stanj[zadnje] = 0
                #self.vrednosti_stanj[predzadnje] = np.random.uniform(-1, 1)
                #self.vrednosti_stanj[zadnje] = np.random.uniform(-1, 1)

            self.vrednosti_stanj[predzadnje] += self.alfa * (
                self.vrednosti_stanj[zadnje] - self.vrednosti_stanj[predzadnje])


    def nagradi_koncna(self, nagrada):
        """
        Tudi online po koncu igre dobi nagrado.
        """
        zadnje = self.stanja[-1]

        # poskrbimo za primer, ko stanja še nismo videli
        if self.vrednosti_stanj.get(zadnje) is None:
                self.vrednosti_stanj[zadnje] = 0

        self.vrednosti_stanj[zadnje] += self.alfa * (
            nagrada - self.vrednosti_stanj[zadnje])


    def ponastavi(self):
        """
        Izbriše zgodovino agentovih stanj.
        """
        self.stanja = []

    
    def shrani_strategijo(self, datoteka):
        """
        Shrani slovar vrednosti stanj za kasnejšo uporabo.
        """
        with open('koda/strategije/' + datoteka, 'wb') as f:
            pickle.dump(self.vrednosti_stanj, f)
    

    def nalozi_strategijo(self, datoteka):
        """
        Naloži slovar naučenih vrednosti.
        """
        with open('koda/strategije/' + datoteka, 'rb') as f:
            self.vrednosti_stanj = pickle.load(f)



class MonteCarlo(Agent):
    """
    Modificiramo agenta tako, da uporablja Monte Carlo 
    algoritem namesto TD(0) - učenja s časovno razliko, 
    ki gleda en korak.
    """
    
    def __init__(self, ime, epsilon=0.3, alfa=0.2, gama=0.9):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama


    def nagradi(self, nagrada):
        """
        Po koncu igre se posodobijo vrednosti stanj od zadaj naprej
        po pravilu spodaj. Za vrednost zadnjega stanja (ki ni dejansko 
        stanje) je vrednost kar nagrada.

        vrednost = vrednost + alfa * (gama * vrednost(naslednji) - vrednost)
        """
        for stanje in reversed(self.stanja):
            if self.vrednosti_stanj.get(stanje) is None:
                self.vrednosti_stanj[stanje] = 0

            self.vrednosti_stanj[stanje] += self.alfa * (
                self.gama * nagrada - self.vrednosti_stanj[stanje])

            nagrada *= self.gama



class TD(Agent):
    def __init__(self, ime, epsilon=0.3, alfa=0.2, gama=0.9, lamb=0.9):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama
        self.lamb = lamb

    
    def nagradi_nazaj(self, nagrada):
        pass

    
    def nagradi_naprej(self, nagrada):
        pass



class DeepAgent(Agent):
    def __init__(self, ime, epsilon=0.3, alfa=0.2):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.vrednosti_stanj = Mreza()
