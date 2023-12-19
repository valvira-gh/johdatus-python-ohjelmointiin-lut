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

def paaohjelma():
    valinta = 1

    while valinta != 0:
        valinta = valikko()

        if valinta == 1:
            operandi1 = kysyLuku("Anna ensimmäinen luku: ")
            operandi2 = kysyLuku("Anna toinen luku: ")
        elif valinta == 2:
            operaattori = "+"
            tulos = operandi1 + operandi2
            print(f"{operandi1} {operaattori} {operandi2} = {tulos}")
        elif valinta == 3:
            operaattori = "-"
            tulos = operandi1 - operandi2
            print(f"{operandi1} {operaattori} {operandi2} = {tulos}")
        elif valinta == 0:
            print("\n" +" Kiitos ohjelman käytöstä.")
        else:
            print("Virheellinen valinta.")
        print()

    print("Ohjelma loppuu.")
    return None

paaohjelma()


