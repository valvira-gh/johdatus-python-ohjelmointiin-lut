# Kirjan esimerkki tiedoston avaamisesta, kirjoittamisesta ja lukemisesta.

# Määritellään useita merkkijonoja
rivi1 = "Merkkijono"
rivi2 = "Toinen merkkijono"
rivi3 = "Kokonaislukuja: 1, 2, 3, 4, 5"
rivi4 = "Liukulukuja: 1.1, 2.2, 3.3, 4.4, 5.5"

### AVAUS ###
# Avataan tiedosto kirjoittamista varten
tiedostoKahva = open("testitiedosto.txt", "w", encoding="utf-8")


### KIRJOITTAMINEN ###
# Kirjoitetaan tiedostoon
tiedostoKahva.write(rivi1 + "\n") # Kirjoittaa rivin 1 ja rivinvaihdon
tiedostoKahva.write(rivi2 + "\n") # Kirjoittaa rivin 2 ja rivinvaihdon
tiedostoKahva.write(rivi3 + "\n") # Kirjoittaa rivin 3 ja rivinvaihdon
tiedostoKahva.write(rivi4 + "\n") # Kirjoittaa rivin 4 ja rivinvaihdon

# Suljetaan tiedosto
tiedostoKahva.close()


### LUKEMINEN ###
# Avataan tiedosto lukemista varten
tiedostoKahva = open("testitiedosto.txt", "r", encoding="utf-8")

# Käytetään toistorakennetta tiedoston lukemiseen
while True:
    rivi = tiedostoKahva.readline() # Luetaan tiedosto rivi kerrallaan
    if len(rivi) == 0: # Jos rivi on tyhjä, tiedosto on luettu
        break
    print(rivi, end="") # Tulostetaan rivi, ei lisätä rivinvaihtoa
tiedostoKahva.close() # Suljetaan tiedosto

# open()-funtion parametrit: (tiedostonimi, tila, merkistö)
# Tila: 'r' = read, 'w' = write, 'a' = append, 'x' = exclusive
# Merkistö: 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'iso-8859-15'

# Tiedoston avaaminen ja sulkeminen
# Tiedosto avataan open()-funktiolla ja suljetaan close()-funktiolla
# Tiedosto avataan muuttujaan, joka on tiedoston kahva
# Tiedoston kahva on tiedoston käsittelyyn tarkoitettu muuttuja
# Tiedosto suljetaan, kun sitä ei enää tarvita, jotta tietokoneen muisti ei täyty

# 1. Tiedostokahva ei päästä meitä käsiksi itse tiedostoon, vaan se toimii
# välittäjänä tiedoston ja ohjelman välillä. Tiedostoa itsessään manipuloidaan
# kahvan kautta, ja siksi funktiot kuten 'write' ja 'close' merkataan pistenotaatioin.

# 2. On hyvä muistaa, että olemme nyt avanneet tiedoston kirjoitustilassa.
# Täten voimme nyt kirjoittaa mitä hauamme, mutta jos tila olisi valittu
# toisin, kuten 'r' eli read, kirjoitusyritys aiheuttaisi virheilmoituksen.

# 3. Tekstitiedostoon voi kirjoittaa vain mrekijonoja, joten luvut on muutettava
# merkkijonoiksi, jotta ne voidaan kirjoittaa tiedostoon. Tämä tehdään
# str()-funktiolla. Myös round()-funktio palauttaa merkkijonon.

# 4. 'write'-käsky poikkeaa 'print'-käskystä kahdella tavalla eli se ottaa
# parametriksen vain yhden merkkijonon, eli ei siis pilkulla erotettuja parametreja.
# Lisäksi 'write'-käsky ei lisää mitään merkkijonoon, ei myöskään rivinvaihtoa.


# ON TÄRKEÄÄ jakaa ohjelma niin, että yhdessä paikassa kirjoitetaan tiedostoon
# ja toisaalla luetaan, jottei tiedostorakenne mene sekaisin.

# Tiedostoa luetaan 'kirjainmerkin' avulla, johon palataan myöhemmin.
# readline()-funktio siirtää kirjanmerkkiä yhden rivin eteenpäin seuraavan
# fyysisen rivin alkuun.

# open()-funktion 3. parametri 'encoding' määrittää merkistön. Sitä ei usein
# tarvita, mutta esim. 'ä' ja 'ö' aiheuttavat ongelmia ilman, että encoding
# määritellään 'utf-8' -merkistöksi.
