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