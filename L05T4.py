# TEHTÄVÄ: Tee pääohjelma, joka saa aliohjelmalta merkkijonon. Välitä arvo toiseen aliohjelmaan, joka tarkistaa
# merkkijonon pituuden KÄYTTÄMÄTTÄ len()-funktiota. Ohjelma pyörii kunnes käyttäjä on antanut sopivan merkkijonon,
# jonka pituus saadaan globaaleista kiintoarvoista
###################################################################################################################
# KIINTOARVOT
MIN_MERKKIMAARA = 5
MAX_MERKKIMAARA = 15


# Aliohjelmat
def kysyMerkkijono():
    syote = input(f"Anna merkkijono, {MIN_MERKKIMAARA}-{MAX_MERKKIMAARA} merkkiä: ")
    merkkijono = str(syote)
    return merkkijono


def tarkistaMerkkimäärä(sana):
    pituus = 0
    for kirjain in sana:
        pituus += 1
    if pituus < MIN_MERKKIMAARA:
        print("Liian lyhyt,", pituus, "merkkiä, anna uusi.")
    elif pituus > MAX_MERKKIMAARA:
        print("Liian pitkä,", pituus, "merkkiä, anna uusi.")
    else:
        print("Annoit sopivan merkkijonon,", pituus, "merkkiä.") 
        merkitOk = True
        return merkitOk


# Pääohjelma
def paaohjelma():
    # Ohjelmaa pyörittävä silmukka
    while True:
        # Syötteet aliohjelmasta
        merkkijono = kysyMerkkijono()

        # Tarkistava aliohjelma
        merkitOk = tarkistaMerkkimäärä(merkkijono)

        #print("Onko merkit ok?", merkitOk)
        if merkitOk:
            break

    print("Kiitos ohjelman käytöstä.")
    return None


paaohjelma()