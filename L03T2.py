# Johdatus Python-ohjelmointiin, LUT, viikko 3, tehtävä 2
#########################################################

# Ohjelman aloitus
syote = input("Haluatko lopettaa ohjelman suorittamisen (k/K): ")


# Ohjelma
if (syote == 'k' or syote == 'K'):
    print("Kiitos ohjelman käytöstä.")
else:
    kayttajanimi = input("Anna nimi: ")
    salasana = input("Anna salasana: ")

    # Laskenta
    kayttaja_pituus = len(kayttajanimi)

    # Vertailu
    if (kayttajanimi == 'Matti' and salasana == 'salasana'):
        print("Käyttäjä tunnistettu.")
    else:
        print("Antamasi nimi oli", kayttaja_pituus, "merkkiä pitkä, mutta se tai salasana ei ollut oikein.")

# Ohjelman lopetus
