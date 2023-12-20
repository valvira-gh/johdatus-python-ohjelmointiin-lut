# Johdatus Python-ohjelmointiin, LUT, viikko 4, tehtävä 5
# Valikkopohjainen taskulaskin

def valikko():
    print("Tämä laskin osaa seuraavat toiminnot:")

    print("1) Anna luvut")
    print("2) Summa")
    print("3) Osamäärä")
    print("0) Lopeta")

    syote = input("Valitse toiminto (0-3): ")
    valinta = int(syote)
    return valinta


def annaLuku(kehote):
    syote = input(kehote)
    return syote


def summa(num1, num2):
    tulos = int(num1) + int(num2)
    tuloste = f"Summa {num1} + {num2} = {tulos}"
    return tuloste


def osamaara(num1, num2):
    tulos = float()
    num1 = int(num1)
    num2 = int(num2)
    if num2 != 0:
        tulos = num1 / num2
        tulos = round(tulos, 2)
        tuloste = f"Osamäärä {num1} / {num2} = {tulos}"
        return tuloste
    else:
        tuloste = "Nollalla ei voi jakaa."
        return tuloste
        

# Valikkorakenne while-loopilla
def paaohjelma():
    while True:
        valinta = valikko()

        if valinta == 1:
            luku1 = annaLuku("Anna ensimmäinen luku: ")
            luku2 = annaLuku("Anna toinen luku: ")
            print(f"Annoit luvut {luku1} ja {luku2}")
        elif valinta == 2:
            tulos = summa(luku1, luku2)
            print(tulos)
        elif valinta == 3:
            tulos = osamaara(luku1, luku2)
            print(tulos)
        elif valinta == 0:
            print("Lopetetaan")
            break

    print("Kiitos ohjelman käytöstä.")


paaohjelma()