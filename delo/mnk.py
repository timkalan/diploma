"""
V tej skripti bo implementirana igra in agent, ki se bo v njej naučil 
igrati "križce in krožce" oz. posplošeno m,n,k-igro. (m * n plošča, 
želimo k simbolov v vrsto).
"""

# za hitrejše matrike
import numpy as np
# import numba as nb

VRSTICE = 3
STOLPCI = 3
V_VRSTO = 3
GRAVITACIJA = False

KRIZCI = 1
KROZCI = -1

NAGRADA_ZMAGA = 1
NAGRADA_REMI = 0
NAGRADA_PORAZ = -1


class Okolje:
    """
    Okolje predstavlja igralno ploščo. Vsebuje vsa pravila igre. To je:
    nastavi igralce, izrisuje, dobiva stanja, gleda legalne pozicije, 
    igra, sodi, daje nagrade.
    """
    def __init__(self, p1, p2):
        """
        Naredimo igralno ploščo kot "array" ustrezne velikosti in dimenzij, 
        shranimo igralca, 
        povemo, da igre ni konec, 
        nastavimo trenutno stanje na None in 
        povemo, kdo bo prvi igral. 

        p1 = član razreda Agent ali Clovek (p2 podobno)
        """
        self.plosca = np.zeros((VRSTICE, STOLPCI), dtype='int64')
        self.p1 = p1
        self.p2 = p2
        self.konec = False
        self.stanje = None
        self.simbol = KRIZCI


    def __str__(self):
        """
        Funkcija za izris plošče na terminal.
        """
        natis = ''
        for i in range(VRSTICE):
            for j in range(STOLPCI):
                if self.plosca[i, j] == -1:
                    natis += '|' + str(self.plosca[i, j])
                # za lepši izris dodamo presledek
                else:
                    natis += '| ' + str(self.plosca[i, j])
            natis += '|' + '\n'
        return natis


    def pridobi_stanje(self):
        """
        Pridobi trenutno stanje igralne plošče in ga shrani kot 
        enodimenzionalni seznam.
        """
        self.stanje = str(self.plosca.reshape(VRSTICE * STOLPCI))
        return self.stanje


    # morda prepiši to z numpy
    def legalne_pozicije(self):
        """
        Poišče vse legalne pozicije - torej prazna polja, 
        znotraj meja igralne plošče.
        """
        pozicije = []
        for i in range(VRSTICE):
            for j in range(STOLPCI):
                if self.plosca[i, j] == 0:
                    # pozicijo shranimo kot nabor
                    pozicije.append((i, j))
        return  pozicije


    # mogoče prepiši v naravne indekse?
    def igraj(self, pozicija):
        """
        Preveri, če je pozicija na seznamu legalnih, in če je, nanjo vpiše 
        simbol trenutnega aktivnega igralca, po uspešni vložitvi pa 
        simbol zamenja.

        pozicija = nabor oblike (x koordinata, y koordinata)
        (POZOR: prvi indeks je 0 (in ne 1))
        """
        if pozicija in self.legalne_pozicije():
            self.plosca[pozicija] = self.simbol
            # zamenjamo igralca po vsaki potezi
            self.simbol = 1 if self.simbol == -1 else -1
        else:
            print('To ni legalna pozicija!')


    def zmagovalec(self):
        """
        Preveri, če imamo zmagovalca in vrne njegovo številko. 
        V primeru remija vrne 0. Prav tako pove okolju, da je
        igre (epizode) konec.
        """
        # vrstice
        for i in range(VRSTICE):
            if sum(self.plosca[i, :]) == V_VRSTO:
                self.konec == True
                return 1
            if sum(self.plosca[i, :]) == - V_VRSTO:
                self.konec == True
                return -1

        # stolpci
        for i in range(STOLPCI):
            if sum(self.plosca[:, i]) == V_VRSTO:
                self.konec == True
                return 1
            if sum(self.plosca[:, i]) == - V_VRSTO:
                self.konec == True
                return -1

        # diagonale
        # preveri obe diagonalni vsoti
        vsota1 = sum([self.board[i, i] for i in range(STOLPCI)])
        vsota2 = sum([self.board[i, STOLPCI - i - 1] for i in range(STOLPCI)])
        if vsota1 == V_VRSTO or vsota2 == V_VRSTO:
            self.konec = True
            return 1
        elif vsota1 == - V_VRSTO or vsota2 == - V_VRSTO:
            self.konec = True
            return -1
            
        # izenačenje
        if len(self.legalne_pozicije()) == 0:
            self.konec = True
            return 0

        # ni konec
        self.konec = False
        return None


    def daj_nagrado(self):
        """
        Da nagrade obema igralcema glede na izid igre, 
        s številkami se lahko še malo igramo.
        """
        # nagrade pridejo samo ob koncu igre
        rezultat = self.zmagovalec()
        if rezultat == 1:
            self.p1.nagradi(NAGRADA_ZMAGA)
            self.p2.nagradi(NAGRADA_PORAZ)
        elif rezultat == -1:
            self.p1.nagradi(NAGRADA_PORAZ)
            self.p2.nagradi(NAGRADA_ZMAGA)
        else:
            self.p1.nagradi(NAGRADA_REMI)
            self.p2.nagradi(NAGRADA_REMI)






igra = Okolje('x', 'y')
print(igra)
print(igra.legalne_pozicije())
igra.igraj((1, 1))
print(igra)
print(igra.legalne_pozicije())
igra.igraj((0, 0))
print(igra)
print(igra.legalne_pozicije())