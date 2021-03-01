import numpy as np

hiperparametri = {
                  'VRSTICE': 3,
                  'STOLPCI': 3,
                  'V_VRSTO': 3,
                  'GRAVITACIJA': False,
                  'NAGRADA_ZMAGA': 1,
                  'NAGRADA_REMI': 0.1,
                  'NAGRADA_PORAZ': -1,
                  'NAGRADA_KORAK': -0.1,
                  'KRIZCI': 1,
                  'KROZCI': -1
                  }

# Funkcije pomagači
def ponovitve(seznam, simbol):
    """
    Funkcija v seznamu poišče, če se simbol kje ponovi st_ponovitev-krat.
    Uporabljeno pri metodi zmagovalec, da je bila posplošena na nxn plošče.
    """
    st_ponovitev=hiperparametri['V_VRSTO']
    i = 0
    while i < len(seznam):
        if seznam[i] == simbol:
            if [seznam[i]] * st_ponovitev == seznam[i:i+st_ponovitev]:
                return simbol
                break
        i += 1



# naredi, da se tu definira velikost igre
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

        p1 = eden od igralcev (p2 podobno)
        """
        self.plosca = np.zeros((hiperparametri['VRSTICE'], hiperparametri['STOLPCI']), dtype='int64')
        self.p1 = p1
        self.p2 = p2
        self.konec = False      # ni konec
        self.stanje = None      # nismo še začeli
        self.simbol = hiperparametri['KRIZCI']    # arbitrarna odločitev


    def __str__(self):
        """
        Funkcija za izris plošče na terminal.
        """
        natis = '\n' + f"{'-' * (hiperparametri['STOLPCI'] * 4 + 1)}" + '\n'
        for i in range(hiperparametri['VRSTICE']):
            for j in range(hiperparametri['STOLPCI']):
                if self.plosca[i, j] == hiperparametri['KROZCI']:
                    natis += '| ' + 'O' + ' '
                # za lepši izris dodamo presledek
                elif self.plosca[i, j] == hiperparametri['KRIZCI']:
                    natis += '| ' + 'X' + ' '
                else:
                    natis += '| ' + ' ' + ' '
            natis += '|' + '\n' + f"{'-' * (hiperparametri['STOLPCI'] * 4 + 1)}" + '\n'
        return natis


    def ponastavi(self):
        """
        Funkcija, ki ponastavi igralno okolje na začetno vrednost.
        """
        self.plosca = np.zeros((hiperparametri['VRSTICE'], hiperparametri['STOLPCI']), dtype='int64')
        self.konec = False
        self.stanje = None
        self.simbol = hiperparametri['KRIZCI']


    def pridobi_stanje(self):
        """
        Pridobi trenutno stanje igralne plošče in ga shrani kot 
        enodimenzionalni seznam.
        """
        stanje = str(self.plosca.reshape(hiperparametri['VRSTICE'] * hiperparametri['STOLPCI']))
        return stanje


    def legalne_pozicije(self):
        """
        Poišče vse legalne pozicije - torej prazna polja, 
        znotraj meja igralne plošče.
        """
        pozicije = []
        if hiperparametri['GRAVITACIJA']:
            for j in range(hiperparametri['STOLPCI']):
                najnizja = -1
                for i in range(hiperparametri['VRSTICE']):
                    if (self.plosca[i, j] == 0) and i > najnizja:
                        najnizja = i

                if najnizja >= 0:
                    pozicije.append((najnizja, j))

        else:
            for i in range(hiperparametri['VRSTICE']):
                for j in range(hiperparametri['STOLPCI']):
                    if self.plosca[i, j] == 0:

                        # pozicijo shranimo kot nabor
                        pozicije.append((i, j))

        return pozicije



    def igraj(self, pozicija):
        """
        Preveri, če je pozicija na seznamu legalnih, in če je, nanjo vpiše 
        simbol trenutnega aktivnega igralca, po uspešni vložitvi pa 
        simbol zamenja.

        pozicija = nabor oblike (x koordinata, y koordinata)
        (POZOR: prvi indeks je 0 (in ne 1))
        """
        legalne = self.legalne_pozicije()
        if pozicija in legalne:
            self.plosca[pozicija] = self.simbol
            
            # zamenjamo igralca po vsaki potezi
            self.simbol = (hiperparametri['KRIZCI'] if 
                          self.simbol == hiperparametri['KROZCI'] else 
                          hiperparametri['KROZCI'])

        else:
            print('To ni legalna pozicija!')


    def zmagovalec(self):
        """
        Preveri, če dana plošča vsebuje zmagovalca za poljubno velikost igre in 
        zahtevanega števila simbolov v vrsti.
        """
        pregled = min(hiperparametri['VRSTICE'], hiperparametri['STOLPCI'])
        razlika = abs(hiperparametri['VRSTICE'] - hiperparametri['STOLPCI'])
        plosca = (self.plosca if 
                  hiperparametri['VRSTICE'] >= hiperparametri['STOLPCI'] else 
                  np.transpose(self.plosca))

        if hiperparametri['V_VRSTO'] > max(hiperparametri['VRSTICE'], hiperparametri['STOLPCI']):
            print("Ne bo zmage!")
            raise Exception 

        for k in range(razlika+1):
            for i in range(pregled):
                # hiperparametri['VRSTICE']
                if ponovitve(list(plosca[i+k, :]), 1):
                    self.konec = True
                    return 1
                if ponovitve(list(plosca[i+k, :]), -1):
                    self.konec = True
                    return -1

                # hiperparametri['STOLPCI']
                if ponovitve(list(plosca[:, i]), 1):
                    self.konec = True
                    return 1
                if ponovitve(list(plosca[:, i]), -1):
                    self.konec = True
                    return -1

            
            diag1 = [plosca[j+k, j] for j in range(pregled)]
            diag2 = [np.flip(plosca, axis=1)[j+k, j] for 
                    j in range(pregled)]

            for i in range(pregled):
                # to ni prilagojeno za m != n
                # razdelimo na naddiagonale, poddiagonale in diagonale
                poddiag1 = [plosca[pregled - i + j+k, j] for 
                            j in range(i)]
                naddiag1 = [plosca[j+k, pregled - i + j] for 
                            j in range(i)]

                # zrcalimo ploščo čez x os in ponovimo
                poddiag2 = [np.flip(plosca, axis=1)[pregled - i + j+k, j] for 
                            j in range(i)]
                naddiag2 = [np.flip(plosca, axis=1)[j+k, pregled - i + j] for 
                            j in range(i)]

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
        

    def daj_nagrado(self):
        """
        Da nagrade obema igralcema glede na izid igre.
        """
        # nagrade pridejo samo ob koncu igre
        rezultat = self.zmagovalec()
        if rezultat == 1:
            self.p1.nagradi(hiperparametri['NAGRADA_ZMAGA'])
            self.p2.nagradi(hiperparametri['NAGRADA_PORAZ'])
        elif rezultat == -1:
            self.p1.nagradi(hiperparametri['NAGRADA_PORAZ'])
            self.p2.nagradi(hiperparametri['NAGRADA_ZMAGA'])
        else:
            self.p1.nagradi(hiperparametri['NAGRADA_REMI'])
            self.p2.nagradi(hiperparametri['NAGRADA_REMI'])


    def daj_nagrado_online(self):
        """
        Za posodabljanje nagrad "online" oz. med igro. 
        """
        rezultat = self.zmagovalec()
        if rezultat == 1:
            self.p1.nagradi_koncna(hiperparametri['NAGRADA_ZMAGA'])
            self.p2.nagradi_koncna(hiperparametri['NAGRADA_PORAZ'])
        elif rezultat == -1:
            self.p1.nagradi_koncna(hiperparametri['NAGRADA_PORAZ'])
            self.p2.nagradi_koncna(hiperparametri['NAGRADA_ZMAGA'])
        else:
            self.p1.nagradi_koncna(hiperparametri['NAGRADA_REMI'])
            self.p2.nagradi_koncna(hiperparametri['NAGRADA_REMI'])



    def poteza_agent(self, igralec):
        """
        Tako zgleda agentova poteza med treniranjem, igranjem in testiranjem, 
        zato je smiselno, da je v svoji funkciji.

        igralec = kater igralec igre je (npr. self.p1)
        """
        pozicije = self.legalne_pozicije()
        agent_akcija = igralec.izberi_akcijo(pozicije, self.plosca, self.simbol)
        self.igraj(agent_akcija)
        stanje = self.pridobi_stanje()
        igralec.dodaj_stanje(stanje)

    
    def poteza_clovek(self, igralec, naravno):
        """
        To je tipična poteza človeka, skrajšamo tako, damo v svojo funkcijo.

        igralec = kater igralec igre je (npr. self.p1)
        naravno = naravno = indeksiranje za pozicije človeka
        """
        pozicije = self.legalne_pozicije()
        clovek_akcija = igralec.izberi_akcijo(pozicije, naravno)
        self.igraj(clovek_akcija)


    def poglej_zmago_igra(self):
        zmaga = self.zmagovalec()
        if zmaga is not None:
            if zmaga == 1:
                print(f'Zmagal je {self.p1.ime}!')
            
            elif zmaga == -1:
                print(f'Zmagal je {self.p2.ime}!')

            else:
                print('Izenačeno!')
            self.ponastavi()
            return True


    def treniraj(self, epizode):
        """
        Vsak igralec:
        poišče možne pozicije, 
        izbere akcijo, 
        posodobi ploščo in zabeleži stanje, 
        počaka razsodbo o koncu
        """
        for i in range(epizode):
            if i % 100 == 0:
                print(f'Epizoda {i+1}')
            
            while not self.konec:
                # 1. igralec
                self.poteza_agent(self.p1)

                zmaga = self.zmagovalec()
                if zmaga is not None:
                    # zmagal je prvi ali remi
                    self.daj_nagrado()
                    self.p1.ponastavi()
                    self.p2.ponastavi()
                    self.ponastavi()
                    break

                else:
                    # 2. igralec
                    self.poteza_agent(self.p2)

                    zmaga = self.zmagovalec()
                    if zmaga is not None:
                        # zmagal je drugi ali remi
                        self.daj_nagrado()
                        self.p1.ponastavi()
                        self.p2.ponastavi()
                        self.ponastavi()
                        break


    def treniraj_online(self, epizode):
        """
        Vsak igralec:
        poišče možne pozicije, 
        izbere akcijo, 
        posodobi ploščo in zabeleži stanje, 
        počaka razsodbo o koncu
        """
        for i in range(epizode):
            if i % 100 == 0:
                print(f'Epizoda {i+1}')
            
            while not self.konec:
                # 1. igralec
                self.poteza_agent(self.p1)
                self.p2.nagradi_online()

                zmaga = self.zmagovalec()
                if zmaga is not None:
                    # zmagal je prvi ali remi
                    self.daj_nagrado_online()
                    self.p1.ponastavi()
                    self.p2.ponastavi()
                    self.ponastavi()
                    break

                else:
                    # 2. igralec
                    self.poteza_agent(self.p2)
                    self.p1.nagradi_online()

                    zmaga = self.zmagovalec()
                    if zmaga is not None:
                        # zmagal je drugi ali remi
                        self.daj_nagrado_online()
                        self.p1.ponastavi()
                        self.p2.ponastavi()
                        self.ponastavi()
                        break

    
    def igraj_clovek(self, zacne=True, naravno=True):
        """
        Metoda za igranje agent - človek.

        zacne = bool; ali začne agent
        naravno = indeksiranje za pozicije človeka
        """
        while not self.konec:
            # poteza prvega igralca
            if zacne:
                self.poteza_agent(self.p1)
            else:
                self.poteza_clovek(self.p2, naravno)

            print(self)
            if self.poglej_zmago_igra():
                break

            # poteza drugega igralca
            if zacne:
                self.poteza_clovek(self.p2, naravno)
            else:
                self.poteza_agent(self.p1)
            print(self)
            if self.poglej_zmago_igra():
                break



    def testiraj_nakljucni(self, st_iger=1000):
        """
        Metoda za igranje agent - naključni igralec.
        """
        rezultati = {
            'zmage': 0,
            'izenačenja': 0,
            'porazi': 0
            }

        for i in range(st_iger):
            if i % 100 == 0:
                print(f'Igra {i+1}')

            while not self.konec:
                # 1. igralec
                self.poteza_agent(self.p1)

                zmaga = self.zmagovalec()
                if zmaga is not None:
                    # zmagal je prvi ali remi
                    if zmaga == 1:
                        rezultati['zmage'] += 1

                    else: 
                        rezultati['izenačenja'] += 1

                    self.ponastavi()
                    break

                else:
                    # 2. igralec
                    pozicije = self.legalne_pozicije()
                    p2_akcija = self.p2.izberi_akcijo(pozicije)
                    self.igraj(p2_akcija)

                    zmaga = self.zmagovalec()
                    if zmaga is not None:
                        # zmagal je drugi ali remi
                        if zmaga == -1:
                            rezultati['porazi'] += 1

                        else: 
                            rezultati['izenačenja'] += 1

                        self.ponastavi()
                        break
        print(rezultati)


    def testiraj_sebi(self, st_iger=1000):
        """
        Metoda za igranje agent - agent.
        """
        rezultati = {
            'zmage': 0,
            'izenačenja': 0,
            'porazi': 0
            }

        for i in range(st_iger):
            if i % 100 == 0:
                print(f'Igra {i+1}')
            
            while not self.konec:
                # 1. igralec
                pozicije = self.legalne_pozicije()
                p1_akcija = self.p1.izberi_akcijo(pozicije, self.plosca, self.simbol)
                self.igraj(p1_akcija)
                stanje = self.pridobi_stanje()
                self.p1.dodaj_stanje(stanje)

                zmaga = self.zmagovalec()
                if zmaga is not None:
                    # zmagal je prvi ali remi
                    if zmaga == 1:
                        rezultati['zmage'] += 1

                    else: 
                        rezultati['izenačenja'] += 1

                    self.ponastavi()
                    break

                else:
                    # 2. igralec
                    pozicije = self.legalne_pozicije()
                    p2_akcija = self.p2.izberi_akcijo(pozicije, self.plosca, self.simbol)
                    self.igraj(p2_akcija)
                    stanje = self.pridobi_stanje()
                    self.p2.dodaj_stanje(stanje)

                    zmaga = self.zmagovalec()
                    if zmaga is not None:
                        # zmagal je drugi ali remi
                        if zmaga == -1:
                            rezultati['porazi'] += 1

                        else: 
                            rezultati['izenačenja'] += 1

                        self.ponastavi()
                        break
        print(rezultati)



    def igraj_splosni(self, p1, p2):
        pass