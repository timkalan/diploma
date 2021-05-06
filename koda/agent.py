import pickle
import os
import ast
import numpy as np

#from keras.models import Sequential
#from keras.layers import Dense
#import keras.backend as K
#import keras

from okolje import hiperparametri, Okolje
from math import comb
#from mreza import Mreza


def ponovitve(seznam):
    """
    Funkcija v seznamu poišče, če se simbol kje ponovi st_ponovitev-krat.
    Uporabljeno pri metodi zmagovalec, da je bila posplošena na nxn plošče.
    """
    st_ponovitev=hiperparametri['V_VRSTO']-1
    i = 0
    while i < len(seznam):
        if seznam[i] in [-1, 1]:
            if [seznam[i]] * st_ponovitev == seznam[i:i+st_ponovitev]:
                return 1
                break
        i += 1
    return 0


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
                    vrednost = 0 
                    #vrednost = np.random.uniform(-1, 1)
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
    
    def __init__(self, ime, epsilon=0.3, alfa=0.2, gama=1):
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



class TDn(Agent):
    """
    Agent, ki uporablja n-step return.
    """
    def __init__(self, ime, epsilon=0.3, alfa=0.2, gama=1, n=3):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama
        self.n = n

    
    def nagradi(self, nagrada):

        zacetna_nagrada = nagrada

        for stanje in reversed(self.stanja):
            # poskrbimo za primer, ko stanja še nismo videli
            if self.vrednosti_stanj.get(stanje) is None:
                self.vrednosti_stanj[stanje] = 0
                #self.vrednosti_stanj[stanje] = np.random.uniform(-1, 1)

            self.vrednosti_stanj[stanje] += self.alfa * (
                nagrada - self.vrednosti_stanj[stanje])

            cas = self.stanja.index(stanje)
            if len(self.stanja[cas:]) <= self.n:
                nagrada *= self.gama

            else:
                nagrada = (self.gama ** len(self.stanja[cas:])) * (
                            self.vrednosti_stanj.get(self.stanja[cas+self.n]))


class TD(Agent):
    """
    Agent, ki za učenje uporablja tabelarični TD(lambda).
    """
    def __init__(self, ime, epsilon=0.3, alfa=0.2, gama=1, lamb=0.9):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama
        self.lamb = lamb

    
    def nagradi_nazaj(self, nagrada):
        """
        ti. backward-view TD(lambda), ki omogoča samo offline učenje.
        """
        for stanje in reversed(self.stanja):
            if self.vrednosti_stanj.get(stanje) is None:
                self.vrednosti_stanj[stanje] = 0

            nagrada = self.lamb * self.gama * nagrada + self.vrednosti_stanj[stanje]

            self.vrednosti_stanj[stanje] += self.alfa * (
                (1 - self.lamb) * nagrada - self.vrednosti_stanj[stanje])


    
    def nagradi(self, nagrada):
        """
        ti. firward-view TD(lambda), ki omogoča tudi online učenje, v tej funkciji pa je implementiran 
        kot offline algoritem.
        """
        # nastavimo sledi upravičenosti na 0
        sledi = {stanje: 0 for stanje in self.stanja}
        multiplikator = 1

        for stanje in reversed(self.stanja):
            # poskrbimo za primer, ko stanja še nismo videli
            if self.vrednosti_stanj.get(stanje) is None:
                self.vrednosti_stanj[stanje] = 0
                #self.vrednosti_stanj[stanje] = np.random.uniform(-1, 1)

            sledi[stanje] = multiplikator
            multiplikator = self.gama * self.lamb

            self.vrednosti_stanj[stanje] += self.alfa * (
                nagrada - self.vrednosti_stanj[stanje]) * sledi[stanje]

            nagrada = self.gama * self.vrednosti_stanj[stanje]



class AgentLin(Agent):
    def __init__(self, ime, epsilon=0.1, alfa=0.2, gama=1, lamb=0.9):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama
        self.lamb = lamb
        self.utezi = [np.random.uniform(-1, 1)] * (hiperparametri['VRSTICE'] * hiperparametri['STOLPCI'] * 3 + 8)


    def pridobi_stanje(self, plosca):
        """
        Agent mora dobiti stanje od plošče in ga spremeniti v
        njemu razumljivo obliko. Pri agentu z linearno aproksimacijo 
        to pomeni narediti čim daljši vektor.
        """
        dodatki = []
        for vrstica in plosca:
            dodatki.append(ponovitve(list(vrstica)))

        for stolpec in np.transpose(plosca):
            dodatki.append(ponovitve(list(stolpec)))

        diag1 = list(plosca.diagonal())
        diag2 = list(np.fliplr(plosca).diagonal())

        dodatki += [ponovitve(diag1), ponovitve(diag2)]

        plosca = list(plosca.reshape(hiperparametri['VRSTICE'] * hiperparametri['STOLPCI']))
        prvi = [1 if el == 1 else 0 for el in plosca]
        drugi = [1 if el == -1 else 0 for el in plosca]
        tretji = [1 if el == 0 else 0 for el in plosca]

        vektor = prvi + drugi + tretji

        #dodatki = []
        #for el1 in vektor:
        #    for el2 in vektor:
        #        dodatki.append(el1 * el2)

        # dodamo 1 na konec vektorja kot nek "bias neuron"
        return str(np.array(vektor + dodatki + [1]))
        


    def vrednost_stanja(self, stanje):
        """
        Vrednost izračunamo kot skalarni produkt med vektorjem stanja in 
        vektorjem uteži.
        """
        stanje = [float(s) for s in stanje[1:-1].split(' ') if s != '']
        return (1 / len(self.utezi)) * sum([i*j for (i, j) in zip(self.utezi, stanje)])

    
    def nagradi2(self, nagrada):
        
        for stanje in reversed(self.stanja):
            
            # stanje pretvorimo začasno stran iz stringa
            vmes = [float(s) for s in stanje[1:-1].split(' ') if s != '']

            drugi = [x * self.alfa * (nagrada - self.vrednost_stanja(stanje)) for x in vmes]
            self.utezi = [a + b for a, b in zip(self.utezi, drugi)]

            nagrada = self.vrednost_stanja(stanje)




    def nagradi(self, nagrada):

        sledi = {stanje: 0 for stanje in self.stanja}
        multiplikator = 1

        for stanje in reversed(self.stanja):
            vmes = [float(s) for s in stanje[1:-1].split(' ') if s != '']

            sledi[stanje] = multiplikator
            multiplikator = self.gama * self.lamb

            drugi = [x * self.alfa * (nagrada - self.vrednost_stanja(stanje)) * sledi[stanje] for x in vmes]
            self.utezi = [a + b for a, b in zip(self.utezi, drugi)]

            nagrada = self.gama * self.vrednost_stanja(stanje)









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
            akcija = pozicije[0]
            for pozicija in pozicije:
                naslednje_stanje = stanje.copy()
                naslednje_stanje[pozicija] = simbol
                naslednji = self.pridobi_stanje(naslednje_stanje)

                vrednost = self.vrednost_stanja(naslednji)

                if vrednost >= najvecja_vrednost:
                    najvecja_vrednost = vrednost
                    akcija = pozicija
        
        return akcija


    def shrani_strategijo(self, datoteka):
        """
        Shrani slovar vrednosti stanj za kasnejšo uporabo.
        """
        with open('koda/strategije/' + datoteka, 'wb') as f:
            pickle.dump(self.utezi, f)
    

    def nalozi_strategijo(self, datoteka):
        """
        Naloži slovar naučenih vrednosti.
        """
        with open('koda/strategije/' + datoteka, 'rb') as f:
            self.utezi = pickle.load(f)
    



    
#class AgentNN(Agent):
#    """
#    Verzija agenta, ki za reprezentacijo vrednostne funkcije uporabi funkcijski 
#    aprosksimator - nevronsko mrežo.
#    """
#
#    def __init__(self, ime, epsilon=0.3, alfa=0.2, na_koliko=10):
#        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)
#
#        self.na_koliko
#
#        # začetne vrednosti uteži
#        li = keras.initializers.RandomUniform(minval=-1, maxval=1, seed=None)
#        dim = hiperparametri['VRSTICE'] * hiperparametri['STOLPCI']
#
#        # naredimo našo mrežo
#        self.cm = Sequential()
#        self.cm.add(Dense(dim, input_dim=dim, activation='sigmoid', kernel_initializer=li, use_bias=True))
#        self.cm.add(Dense(36, activation='relu', kernel_initializer=li, use_bias=True))
#        self.cm.add(Dense(1, activation='sigmoid', kernel_initializer=li, use_bias=False))
#
#        # optimizacije in kreacija modela
#        self.opt_cm = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, amsgrad=False)
#        self.cm.compile(loss='mean_squared_error', optimizer=self.opt_cm)
#
#
#    def nagradi(self, nagrada):
#        pass

