# luku = 12223.234452342
# tarkkuus = 3

# print("{0:.{1}f}".format(float(luku), tarkkuus))

# merkkijono = "scooby doo"
# merkki, jono = merkkijono.split(" ")
# print(merkki)
# print(jono)

# merkki = merkki.capitalize()
# jono = jono.capitalize()
# print(merkki)
# print(jono)

# merkkijono = merkki, jono
# print(type(merkkijono))

# merkkijono = " ".join(merkkijono)
# print(merkkijono)

# merkkijono = merkkijono.replace(" ", "")
# print(merkkijono)

# merkkijono = merkkijono.replace("o", "0")
# print(merkkijono)

###############################################3

def valikko():
    print("1) Tallenna tiedosto")
    print("2) Lue tiedosto")
    print("0) Lopeta")
    valinta = int(input("Valinta: "))
    return valinta

def tallenna(tiedosto):
    # tiedosto = open(tiedosto, 'w', encoding='utf-8')
    # while True:
    #     rivi = tiedosto.readline()
    #     if len(rivi) == 0:
    #         break
    with open(tiedosto, 'w', encoding='utf-8') as tiedosto:
        tiedosto.write("scooby doo\n")
        rivi = rivi.rstrip()
        sarake = rivi.split(';')
        print("Tiedostossa oli '"+sarake[0]+"' ja '"+sarake[1]+"'.")
    return None


def lue(tiedosto):
    tiedosto = open(tiedosto, 'r', encoding='utf-8')
    while True:
        rivi = tiedosto.readline()
        if len(rivi) == 0:
            break
        rivi = rivi.rstrip()
        sarake = rivi.split(';')
        print("Tiedostossa oli '" + sarake[0] + "' ja '" + sarake[1] + "'.")
    tiedosto.close()
    return None


2
def paaohjelma():
    tiedosto = "L06Demo.txt"
    while True:
        toiminto = valikko()
        if toiminto == 1:
            tallenna(tiedosto)
        elif toiminto == 2:
            lue(tiedosto)
        elif toiminto == 0:
            print("Kiitos ohjelman käytöstä!")
            break
        else:
            print("Virheellinen valinta!")


    
    return None

paaohjelma()