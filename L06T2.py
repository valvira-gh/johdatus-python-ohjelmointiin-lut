
def kysyTiedosto():
    tiedosto = input("Anna luettavan tiedoston nimi: ")
    return tiedosto


def laskeNimet(tiedostoNimi):
    # Alustetaan paluumuuttujat
    nimetSumma = 0
    merkitSumma = 0
    # Avataan tiedosto
    tiedosto = open(tiedostoNimi, 'r', encoding='utf-8')
    # Erotetaan yksittäinen rivi muuttujaan 'rivi'
    rivi = tiedosto.readline()
    # Luodaan silmukka tiedoston sisällön läpikäymiseksi rivi kerrallaan
    while len(rivi) > 0:
        # Joka rivilla on yksi nimi, joten nimet voidaan laskea laskemalla rivit. Lisätään siis
        # 'nimetSumma' muuttujaan aina yksi luku lisää joka kierroksella.
        nimetSumma += 1
        # Merkkimäärän laskentaan tallennetaan yksittäisen rivin merkkimäärä, erotuksena rivinvaihtomerkki,
        # käyttämällä len()-funktiota. Lisätään yksittäisen rivin merkkimäärä 'merkitSumma'-muuttujan arvoon.
        rivinMerkit = len(rivi)
        merkitSumma += rivinMerkit
        # Alustetaan 'rivi'-muuttuja uuteen riviin
        rivi = tiedosto.readline()
    # Suljetaan tiedosto heti kun sitä ei enää tarvita
    tiedosto.close()

    # Lasketaan nimien keskimääräinen pituus, pyöristetään muuttamalla kokonaisluvuksi.
    keskiarvo = merkitSumma / nimetSumma
    keskiarvo = int(keskiarvo)

    # Tulostetaan tulokset
    print(f"Tiedostossa oli {nimetSumma} nimeä ja {merkitSumma} merkkiä.")
    print(f"Keskimääräinen nimen pituus oli {keskiarvo} merkkiä.")
    return None

def paaohjelma():
    tiedostoNimi = kysyTiedosto()
    summa = laskeNimet(tiedostoNimi)
    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()
