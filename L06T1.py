### VIIKKO 6, TIEDOSTOKÄSITTELYN PERUSTEET, LUT, Johdatus Python-ohjelmointiin ###

# Kirjoita tiedosto
def tiedostoKirjoita(tiedostoNimi):
    # Avataan tiedosto aluksi ja talletetaan se tiedostokahvaan 'tiedosto'.
    tiedosto = open(tiedostoNimi, 'w', encoding='utf-8')

    # Kysytään käyttäjältä tallennettava nimi toistorakenteessa
    while True:
        syote = input("Anna tiedostoon tallennettava nimi (0 lopettaa): ")
        nimi = syote

        if nimi != '0':
            tiedosto.write(nimi + '\n')
        else:
            break
    
    tiedosto.close() # Suljetaan tiedosto aina, kun manipulointi päättyy.
    return None


# Lue tiedosto
def tiedostoLue(tiedostoNimi):
    # Avataan tiedosto ja tallennetaan se tiedostokahvaan 'tiedosto'
    tiedosto = open(tiedostoNimi, 'r', encoding='utf-8')

    print(f"Tiedostoon '{tiedostoNimi}' on tallennettu seuraavat nimet:")
    # Toistorakenteen avulla käydään tiedosto läpi rivi kerrallaan
    while True:
        rivi = tiedosto.readline()  # Kunkin rivin arvo tallennetaan muuttujaan 'rivi'
        if len(rivi) == 0:
            break
        print(rivi, end='')
    tiedosto.close()
    return None


# Pääohjelmataso
def paaohjelma():
    # Kysytään tiedoston nimi
    syote = input("Anna tallennettavan tiedoston nimi: ")
    tiedostoNimi = syote

    # Kirjoitetaan tiedosto aliohjelman avulla
    tiedostoKirjoita(tiedostoNimi)

    # Luetaan tiedosto aliohjelman avulla
    tiedostoLue(tiedostoNimi)

    print("Kiitos ohjelman käytöstä.")
    return None


paaohjelma()
