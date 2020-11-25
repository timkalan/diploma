"""
Sem bom odlagal staro kodo, ki je ne uporabljam več, a se mi vseeno zdi, da bo
kdaj morda koristila.
"""

VRSTICE = 6
STOLPCI = 6
V_VRSTO = 3

def zmagovalec2(self):
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
    vsota1 = sum([self.plosca[i, i] for i in range(STOLPCI)])
    vsota2 = sum([self.plosca[i, STOLPCI - i - 1] for i in range(STOLPCI)])
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


def zmagovalec2(self):
    """
    Preveri, če imamo zmagovalca in vrne njegovo številko. 
    V primeru remija vrne 0. Prav tako pove okolju, da je
    igre (epizode) konec. Z uporabo funkcije pomagača deluje 
    za poljubno velike plošče, kjer je m == n.
    """
    # vrstice
    for i in range(VRSTICE):
        if ponovitve(list(self.plosca[i, :]), 1):
            self.konec = True
            return 1
        if ponovitve(list(self.plosca[i, :]), -1):
            self.konec = True
            return -1
                
    # stolpci
    for i in range(STOLPCI):
        if ponovitve(list(self.plosca[:, i]), 1):
            self.konec = True
            return 1
        if ponovitve(list(self.plosca[:, i]), -1):
            self.konec = True
            return -1

    # diagonale
    if (V_VRSTO <= VRSTICE) or (V_VRSTO <= STOLPCI):
        diag1 = [self.plosca[j, j] for j in range(min(VRSTICE, STOLPCI))]
        diag2 = [np.flip(self.plosca, axis=1)[j, j] for 
                j in range(min(VRSTICE, STOLPCI))]

        for i in range(max(VRSTICE, STOLPCI)):
            # to ni prilagojeno za m != n
            # razdelimo na naddiagonale, poddiagonale in diagonale
            poddiag1 = [self.plosca[min(VRSTICE, STOLPCI) - i + j, j] for 
                        j in range(min(i, min(VRSTICE, STOLPCI)))]
            naddiag1 = [self.plosca[j, min(VRSTICE, STOLPCI) - i + j] for 
                        j in range(min(i, min(VRSTICE, STOLPCI)))]

            # zrcalimo ploščo čez x os in ponovimo
            poddiag2 = [np.flip(self.plosca, axis=1)[min(VRSTICE, STOLPCI) - i + j, j] for 
                        j in range(min(i, min(VRSTICE, STOLPCI)))]
            naddiag2 = [np.flip(self.plosca, axis=1)[j, min(VRSTICE, STOLPCI) - i + j] for 
                        j in range(min(i, min(VRSTICE, STOLPCI)))]

            if (ponovitve(list(diag1), 1) or ponovitve(list(naddiag1), 1) 
                or ponovitve(list(poddiag1), 1) or ponovitve(list(diag2), 1) 
                or ponovitve(list(naddiag2), 1) or ponovitve(list(poddiag2), 1)):
                self.konec = True
                return 1

            if (ponovitve(list(diag1), -1) or ponovitve(list(naddiag1), -1) 
                or ponovitve(list(poddiag1), -1) or ponovitve(list(diag2), -1) 
                or ponovitve(list(naddiag2), -1) or ponovitve(list(poddiag2), -1)):
                self.konec = True
                return -1
        
    # izenačenje
    if len(self.legalne_pozicije()) == 0:
        self.konec = True
        return 0

    # ni konec
    self.konec = False
    return None


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




    def poteza_agent(self):
        pozicije = self.legalne_pozicije()
        p1_akcija = self.p1.izberi_akcijo(pozicije, self.plosca, self.simbol)
        self.igraj(p1_akcija)
        stanje = self.pridobi_stanje()
        self.p1.dodaj_stanje(stanje)


    def poteza_clovek(self, naravno=True):
        pozicije = self.legalne_pozicije()
        p2_akcija = self.p2.izberi_akcijo(pozicije, naravno=naravno)
        self.igraj(p2_akcija)
    

    def igraj_clovek2(self, naravno=True, zacne=True):
        """
        Metoda za igranje agent - človek.
        """
        if zacne:
            poteza1 = self.poteza_agent()
            poteza2 = self.poteza_clovek()
        else:
            poteza2 = self.poteza_agent()
            poteza1 = self.poteza_clovek()

        while not self.konec:
            poteza1
            print(self)

            zmaga = self.zmagovalec()
            if zmaga is not None:
                if zmaga == 1:
                    print(f'Zmagal je {self.p1.ime}!')

                else:
                    print('Izenačeno!')
                self.ponastavi()
                break

            else:
                poteza2
                print(self)

                zmaga = self.zmagovalec()
                if zmaga is not None:
                    if zmaga == -1:
                        print(f'Zmagal je {self.p2.ime}!')
                    
                    else:
                        print('Izenačeno!')
                    self.ponastavi()
                    break



    # prepiši s try except
#    def igraj2(self, pozicija):
#        """
#        Preveri, če je pozicija na seznamu legalnih, in če je, nanjo vpiše 
#        simbol trenutnega aktivnega igralca, po uspešni vložitvi pa 
#        simbol zamenja.
#
#        pozicija = nabor oblike (x koordinata, y koordinata)
#        (POZOR: prvi indeks je 0 (in ne 1))
#        """
#        if pozicija in self.legalne_pozicije():
#            self.plosca[pozicija] = self.simbol
#            
#            # zamenjamo igralca po vsaki potezi
#            self.simbol = hiperparametri['KRIZCI'] if self.simbol == hiperparametri['KROZCI'] else hiperparametri['KROZCI']
#        else:
#            print('To ni legalna pozicija!')

def shrani_strategijo(self, datoteka):
        """
        Shrani slovar vrednosti stanj za kasnejšo uporabo.
        """
        f = open('koda/strategije/' + datoteka, 'wb')
        pickle.dump(self.vrednosti_stanj, f)
        f.close()