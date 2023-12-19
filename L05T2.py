
def vertaileLukuja(num1, num2):
    # Aliohjelma saa PARAMETREINA kaksi lukuarvoa, jotka se vertailee
    # PALUUARVONA se palauttaa suuremman luvun
    if num1 > num2:
        print(f"Testatuista luvuista {num1} on suurempi kuin {num2}")
        return num1
    elif num2 > num1:
        print(f"Testatuista luvuista {num2} on suurempi kuin {num1}")
        return num2
    else:
        print("Luvut ovat samansuuruiset.")
        return num1

def paaohjelma():
    # Syötteet käyttäjältä ensimmäisenä.
    syote = input("Anna ensimmäinen luku: ")
    luku1 = int(syote)
    syote = input("Anna toinen luku: ")
    luku2 = int(syote)

    # Seuraavaksi vertaillaan lukuja aliohjelmassa, jolle 
    # annetaan ARGUMENTTEINA luku1 ja luku2. Paluuarvo tallennetaan
    # muuttujaan 'suurempi_luku'.
    suurempi_luku = vertaileLukuja(luku1, luku2)

    # Varmennetaan ensin, että luvut ovat erisuuruiset. Tämä varmistaa
    # sen, että ohjelma päättyy tasalukutilanteessa aliohjelman logiikan
    # mukaisesti.
    if luku1 != luku2:
        syote = input("Paljonko vähennetään suuremmasta luvusta: ")
        vahennys = int(syote)
        # Tallennetaan erotustulos muuttujaan 'erotus', jotta sitä voidaan
        # käyttää uutena argumenttina uudessa vertailussa.
        erotus = suurempi_luku - vahennys

        # Tarkistetaan päätasolla kumpi luvuista oli suurempi, jotta
        # tiedetään pienempi luku, jotta tiedetään kumpaa lukua
        # käytetään uudessa vertailussa.
        if suurempi_luku == luku1:
            pienempi_luku = luku2
        else:
            pienempi_luku = luku1
        
        # Kutsutaan aliohjelmaa uudelleen, jotta voidaan vertailla
        # suuremman luvun uutta erotuksen jälkeistä arvoa ja aiemmin
        # selvitettyä pienempää lukua.
        vertaileLukuja(erotus, pienempi_luku)

    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()
