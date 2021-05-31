import pickle
import os
import numpy as np
import random
import torch

from torch import nn, FloatTensor, save, load, optim
from collections import namedtuple, deque
from okolje import hiperparametri, Okolje


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
    def __init__(self, ime, epsilon=0.01, alfa=0.2, gama=1, lamb=0.9):
        Agent.__init__(self, ime, epsilon=0.3, alfa=0.2)

        self.gama = gama
        self.lamb = lamb

    
    def nagradi_naprej(self, nagrada):
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
        ti. forward-view TD(lambda), ki omogoča tudi online učenje, v tej funkciji pa je implementiran 
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
        # alt: np.random.uniform(-1, 1)
        self.utezi = [0] * (hiperparametri['VRSTICE'] * hiperparametri['STOLPCI'] * 3 + 9)


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

    
    def nagradi(self, nagrada):
        
        for stanje in reversed(self.stanja):
            
            # stanje pretvorimo začasno stran iz stringa
            num_stanje = [float(s) for s in stanje[1:-1].split(' ') if s != '']

            delta = [self.alfa * (nagrada - self.vrednost_stanja(stanje)) * x for x in num_stanje]
            self.utezi = [a + b for a, b in zip(self.utezi, delta)]

            nagrada = self.vrednost_stanja(stanje)
        
        return nagrada


    def nagradi_tdl(self, nagrada):

        # inicializacija sledi upravičenosti
        vmes = [float(s) for s in self.stanja[0][1:-1].split(' ') if s != '']
        sledi = np.zeros((len(vmes),))

        for stanje in reversed(self.stanja):
            vmes = [float(s) for s in stanje[1:-1].split(' ') if s != '']
            vmes = np.array(vmes)

            sledi = self.gama * self.lamb * (sledi + vmes)

            delta = self.alfa * (nagrada - self.vrednost_stanja(stanje)) * sledi
            self.utezi = [a + b for a, b in zip(self.utezi, delta.tolist())]

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
    

  
class AgentNN(Agent):
    """
    Verzija agenta, ki za reprezentacijo vrednostne funkcije uporabi funkcijski 
    aprosksimator - nevronsko mrežo.
    """

    def __init__(self, ime, epsilon=0.3, alfa=0.05, hidden_dim=64):
        Agent.__init__(self, ime, epsilon=epsilon, alfa=alfa)

        self.input_dim = hiperparametri['STOLPCI'] * hiperparametri['VRSTICE'] * 3 + 1
        #self.hidden_dim = hidden_dim
        self.hidden_dim = 2 * self.input_dim

        self.mreza = nn.Sequential(nn.Linear(self.input_dim, self.hidden_dim),
                                   nn.ReLU(),
                                   nn.Linear(self.hidden_dim, self.hidden_dim),
                                   nn.ReLU(),
                                   # zadnji sloj ni relu, saj imamo lahko negativne vrednosti
                                   nn.Linear(self.hidden_dim, 1))
                                   #nn.Tanh())

        # kritejiska funkcija - srednja kvd. napaka
        self.kriterij = nn.MSELoss()

        # dejanski algoritem - stohastični gradientni spust
        self.optimizer = optim.SGD(self.mreza.parameters(), lr=self.alfa)


    def pridobi_stanje(self, plosca):
        """
        Stanje predstavimo kot binarni vektor.
        """
        plosca = list(plosca.reshape(hiperparametri['VRSTICE'] * hiperparametri['STOLPCI']))
        prvi = [1 if el == 1 else 0 for el in plosca]
        drugi = [1 if el == -1 else 0 for el in plosca]
        tretji = [1 if el == 0 else 0 for el in plosca]

        vektor = prvi + drugi + tretji

        # dodamo 1 na zadnje mesto kot "bias" nevron
        return str(np.array(vektor + [1]))


    def vrednost_stanja(self, stanje):
        """
        Vrednost stanja nam da naša nevronska mreža.
        """
        # pretvorimo stanje v ustrzen vektor
        stanje = [float(s) for s in stanje[1:-1].split(' ') if s != '']
        stanje = FloatTensor(stanje)

        return self.mreza(stanje)


    def nagradi(self, nagrada):
        
        for stanje in reversed(self.stanja):
            
            # stanje pretvorimo stran iz stringa v tenzor
            num_stanje = [float(s) for s in stanje[1:-1].split(' ') if s != '']
            tenzor = FloatTensor(num_stanje)
            
            # pripravimo za backward pass
            self.optimizer.zero_grad()

            output = self.mreza(tenzor)
            napaka = self.kriterij(output, FloatTensor([nagrada]))
            #print(napaka.item())
            napaka.backward()
            self.optimizer.step()

            # TODO: TDlambda
            nagrada = self.vrednost_stanja(stanje)
        
        return napaka.item()


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
        save(self.mreza.state_dict(), 'koda/strategije/' + datoteka)
    

    def nalozi_strategijo(self, datoteka):
        """
        Naloži slovar naučenih vrednosti.
        """
        self.mreza.load_state_dict(load('koda/strategije/' + datoteka))



class NNER(AgentNN):
    """
    Nadgradnja agenta, ki uporablja nevronsko mrežo s "spominom".
    """

    def __init__(self, ime, epsilon=0.3, alfa=0.01, hidden_dim=512, velikost=10000):
        super().__init__(ime, epsilon=epsilon, alfa=alfa, hidden_dim=hidden_dim)

        # hranimo spomin - replay memory
        self.spomin = deque([], maxlen=velikost)


    def __len__(self):
        return len(self.spomin)


    def zapomni(self, *args):
        """
        Shranimo tranzicijo v spomin.
        """
        Tranzicija = namedtuple('Tranzicija',('stanje', 'naslednje_stanje', 'nagrada'))
        self.spomin.append(Tranzicija(*args))


    def vzorec(self, batch_size=200):
        return random.sample(self.spomin, batch_size)