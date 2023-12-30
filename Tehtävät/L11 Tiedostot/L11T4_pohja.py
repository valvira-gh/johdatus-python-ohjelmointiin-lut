# (c) LUT 2020 L11T4.py un
# Tämä esimerkki on tarkoitettu omatoimisen oppimisen tueksi ohjelmoinnin 
# opiskeluun. Muu käyttö kielletty.
######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: 
# Opiskelijanumero: 
# Päivämäärä:
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat 
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
# 
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse 
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Ohjelma, joka etsii sopivia numeroita

import time
import sys

def Hakufunktio():
    Luvut = ["",""]
    Luvut[0] = 0  #Pienempi luku tallennetaan tähän
    Luvut[1] = 0  #Suurempi luku tallennetaan tähän

# Lisättävä koodi alkaa alta.

# Lisättävä koodi loppuu ylle.  

def paaohjelma():
    Kello1 = time.perf_counter()
    Tulosluvut = Hakufunktio()
    Kello2 = time.perf_counter()
    Aika = Kello2 - Kello1
    if ((Tulosluvut[0] == 0) and (Tulosluvut[1] == 0)):
        print("Hakualgoritmi ei löytänyt sopivaa lukuparia.")
    elif (Aika > 2):
        print("Hakualgoritmi ei ollut tarpeeksi nopea.")
    else:
        print("Hakualgoritmi oli riittävän nopea!")
        print("Se löysi sopivan parin:", Tulosluvut[0], "ja", Tulosluvut[1])
    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()

###########################################################################
# eof
