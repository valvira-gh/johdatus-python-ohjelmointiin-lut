# VIIKKO 5, TEHTÄVÄ 1


def tulosta():
    print("Ensimmäinen vaihe:")
    print("Nyt olemme tulosta-aliohjelmassa")
    print("Tämä aliohjelma tulostaa vain tekstiä.")
    print("Tämä sopii hyvin valikon tulostamiseen.")
    print()
    return None


def tulostaLuku(luku):
    print("Aliohjelmassa parametrin arvo on", luku)

    # Korota neliöön
    luku = luku * luku
    print("Aliohjelmassa parametrin arvo on neliöön korottamisen jälkeen", luku)

    return None


def yhdistaNimet(etunimi, sukunimi):
    kokonimi = etunimi + " " + sukunimi

    return kokonimi



def main():
    # 1. vaihe
    tulosta()

    # 2. vaihe
    print("Toinen vaihe:")
    syote = input("Anna luku: ")
    luku = int(syote)
    print("Päätasolla ennen aliohjelmaa luku on", luku)
    tulostaLuku(luku)
    print("Päätasolla aliohjelman jälkeen luku on", luku)
    print()

    # 3. vaihe
    print("Kolmas vaihe:")
    syote = input("Anna etunimi: ")
    etunimi = syote
    syote = input("Anna sukunimi: ")
    sukunimi = syote
    kokonimi = yhdistaNimet(etunimi, sukunimi)
    print("Etunimi '" + etunimi + "' ja sukunimi '" + sukunimi + "' muodostavat nimen '" + kokonimi + "'.")

    print("Kiitos ohjelman käytöstä.")
    return None

main()