######################################
# VIIKKO 6, DEMO 3

def valikko():
        print("Analysoi tiedoston tiedot")
        print("1) Anna tiedostonimet")
        print("2) Analysoi")
        print("3) Tallenna tulokset")
        print("0) Lopeta")
        syote = input("Valintasi: ")
        valinta = int(syote)
        return valinta


def kysyNimi(kehote):
    nimi = input(kehote)
    return nimi


def laskeDatanSumma(nimi):
    summa = 0
    tiedosto = open(nimi, 'r', encoding='utf-8')
    rivi = tiedosto.readline()
    while len(rivi) > 0:
        data = int(rivi[10:])
        summa = summa + data
        rivi = tiedosto.readline()
    tiedosto.close()
    return summa


def haeEkaPvm(nimi):
    tiedosto = open(nimi, 'r', encoding='utf-8')
    rivi = tiedosto.readline()
    pvm = rivi[0:9]
    return pvm


def haeVikaPvm(nimi):
    tiedosto = open(nimi, 'r', encoding='utf-8')
    rivi = tiedosto.readline()
    vikaRivi = rivi
    while len(rivi) > 0:
        vikaRivi = rivi
        rivi = tiedosto.readline()
    tiedosto.close()
    pvm = vikaRivi[0:9]
    return pvm


def tallennaTulokset(nimi, summa, pvmEka, pvmVika):
    tiedosto = open(nimi, 'w', encoding='utf-8')
    rivi = "Tiedostossa oli dataa " + str(pvmEka) + " - " + str(pvmVika) + ", jonka summa on " + str(summa) + ".\n"
    tiedosto.write(rivi)
    tiedosto.close()
    return None



def paaohjelma():
    valinta = 1

    while valinta != 0:
        valinta = valikko()

        if valinta == 1:
            tiedostoLue = kysyNimi("Anna luettavan tiedoston nimi: ")
            tiedostoKirjoita = kysyNimi("Anna kirjoitettavan tiedoston nimi: ")
        elif valinta == 2:
            summa = laskeDatanSumma(tiedostoLue)
            print("Tiedostossa oli dataa, jonka summa on", summa)
            pvmEka = haeEkaPvm(tiedostoLue)
            print("Tiedostossa oli dataa", pvmEka, "- alkaen.")
            pvmVika = haeVikaPvm(tiedostoLue)
            print("Tiedostossa oli dataa", pvmVika, "- asti.")
        elif valinta == 3:
            tallennaTulokset(tiedostoKirjoita, summa, pvmEka, pvmVika)
        elif valinta == 0:
            print("\n" +" Kiitos ohjelman käytöstä.")
        else:
            print("Virheellinen valinta.")
        print()

    print("Ohjelma loppuu.")
    return None

paaohjelma()


