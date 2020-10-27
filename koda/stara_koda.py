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