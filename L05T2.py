# VIIKKO 5, TEHTÄVÄ 2
################################
#  Laskenta

def vertaa_luvut(a, b):
    if (a < b):
        return suurempi = a
    elif (a > b):
        return suurempi = b
    elif (a == b):
        return suurempi = a

    print(f"Suurempi: {suurempi}")

################################



################################
# 


################################


################################
#  pääohjelma

def paaohjelma():
    while True:
        syote = input("Anna ensimmäinen luku: ")
        luku_A = int(syote)
        syote = input("Anna toinen luku: ")
        luku_B= int(syote)
        suurempi_luku= vertaa_luvut(luku_A, luku_B)
        if (a == suurempi_luku):
            return print(f"Testatuista luvuista {suurempi_luku} on suurempi kuin {b}.")
        print(suurempi_luku)
        
        print("Kiitos ohjelman käytöstä.")



################################
paaohjelma()
