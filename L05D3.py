######################################
# VIIKKO 5, DEMO 3

def valikko():
        print("LASKIN")
        print("1) Anna 2 lukua")
        print("2) Laske summa")
        print("3) Laske erotus")
        print("0) Lopeta")
        syote = input("Valintasi: ")
        valinta = int(syote)
        return valinta

def kysyLuku(kehote):
    syote = input(kehote)
    luku = int(syote)
    return luku

def laskeSumma(luku1, luku2):
    print(f"{luku1} + {luku2} = {luku1 + luku2}")
    return None

def laskeErotus(luku1, luku2):
    print(f"{luku1} - {luku2} = {luku1 - luku2}")
    return None


def paaohjelma():
    valinta = 1

    while valinta != 0:
        valinta = valikko()

        if valinta == 1:
            operandi1 = kysyLuku("Anna ensimmäinen luku: ")
            operandi2 = kysyLuku("Anna toinen luku: ")
        elif valinta == 2:
            laskeSumma(operandi1, operandi2)
        elif valinta == 3:
            laskeErotus(operandi1, operandi2)
        elif valinta == 0:
            print("\n" +" Kiitos ohjelman käytöstä.")
        else:
            print("Virheellinen valinta.")
        print()

    print("Ohjelma loppuu.")
    return None

paaohjelma()



