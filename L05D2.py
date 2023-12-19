# VIIKKO 5, DEMO 2
##################################


##################################
# Aliohjelmarakenne tyhjästä


##def tulostaOhjeet():
#    print("Ohje rivi 1.")
#    print("Ohje rivi 1.")
#    return None
#
#
#def kysyPaino(kehote):
#    syote = input(kehote)
#    paino = int(syote)
#    return paino
#
#
#def tulostaTulokset(painoEka, painoToka):
#    print("Paino on", painoEka, "kg.")
#    print("Paino on", painoToka, "kg.")
#    return None
#
#
#def paaohjelma():
#    tulostaOhjeet()
#
#    paino1 = kysyPaino("Anna eka paino: ")
#    paino2 = kysyPaino("Anna toka paino: ")
#    tulostaTulokset(paino1, paino2)
#
#    
#    print("Kiitos ohjelman käytöstä.")
#    return None
#
#

#paaohjelma()


##################################
# ARVOPARAMETRI
# Arvoparametrin arvo on kopio, eikä se muuta alkuperäistä arvoa

# def tulosta(numero):
#     print("Aliohjelma alkaa.")
#     print(numero)
#     numero = numero + 1
#     print(numero)
#     print("Aliohjelma päättyy.")
    
#     return None


# def paaohjelma():
#     luku = 1
#     print(luku)
#     tulosta(luku)
#     print(luku)
    
#     print("Kiitos.")
#     return None


# paaohjelma()
##################################
# NIMIAVARUUS
# Kolme toisistaan erillistä nimiavaruutta.

# def aliohjelma1():
#     muuttuja = 1
#     print("aliohjelma1:", muuttuja)
#     return None


# def aliohjelma2():
#     muuttuja = 2
#     print("aliohjelma2:", muuttuja)
#     return None



# def paaohjelma():
#     muuttuja = "Hei."
#     print(muuttuja)
#     aliohjelma1()
#     aliohjelma2()

#     print(muuttuja)
#     aliohjelma1()

#     print("Kiitos.")
#     return None

# paaohjelma()

##################################
# PARAMETRIEN JÄRJESTYS JA NIMEÄMINEN

# def tulosta(eka, toka, kolmas):
#     print(eka, toka, kolmas, end="\n" * 2)
#     return None

# a = "eka"
# b = 1
# c = 2.34

# tulosta(a, b, c)
# tulosta(b, c, a)
# tulosta(c, a, b)

# tulosta(kolmas = c, eka = a, toka = b)

##################################
# Dokumentti-merkkijono, docstring

# def tulostaLuku(Luku):
#     '''Tulostaa parametrina saadun luvun.'''
#     print(Luku)
#     return None

# tulostaLuku(1)

##################################
# Globaalit kiintoarvot ok, globaalit muuttujat ei

MERKKEJA_MAX = 30

def kysyNimi():
    nimi = input("Anna nimi, max " + str(MERKKEJA_MAX) + " merkkiä: ")
    print(nimi)

    return nimi

def paaohjelma():
    nimi = kysyNimi()
    for i in range(MERKKEJA_MAX):
        print(i, end=" ")
    print()

    # tarkista nimen pituus
    if len(nimi) > MERKKEJA_MAX:
        print("Nimi on liian pitkä!")
    else:
        print("Nimi on sopivan pituinen.")

    return None

paaohjelma()

##################################



