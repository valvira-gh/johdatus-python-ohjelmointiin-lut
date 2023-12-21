######################################################
# VIIKKO 6, DEMO 2, LUT, Johdatus Python-ohjelmointiin
######################################################
# Tiedosto tyhjennys

tiedosto = open("tiedosto.txt", "w")
tiedosto.close()

######################################################
# Merkkijonon käsittely kirjaimittain

# merkkijono = "Tämä on merkkijono"
# for i in range(len(merkkijono)):
#     print(merkkijono[i], end=" ")
#     print(merkkijono[i], merkkijono[i].isalpha())

# s2 = "Tämä 55 on 545toinefe534576n merkkijono."
# s3 = ""

# for i in range(len(s2)):
#     if (s2[i].isdigit()):
#         print(s2[i], end=" ")
#         s3 += s2[i]
# print()# 
#print(s3)
######################################################
# Sopivimman arvon löytäminen, nimilista.txt

# Alustetaan muuttujat
# lyhinPituus = None
# lyhinNimi = None

# # Avataan tiedosto
# tiedosto = open("nimilista.txt", "r", encoding="utf-8")

# # Luetaan ensimmäinen rivi
# rivi = tiedosto.readline()

# while (len(rivi) > 0):
#     pituus = len(rivi) - 1 # -1, koska rivinvaihtomerkki, sama funktiolla 'rstrip()'

#     # Ohjelma tarkista rivi kerrallaan rivien pituuden ja vertailee niitä
#     if lyhinPituus == None or lyhinPituus > pituus:  # lyhinPituus == None ottaa huomioon muuttujan alustuksen
#         # Kohdatessaan lyhyemmän pituuden kuin aiemmin lyhyimmän, ohjelma korvaa sen uudella arvolla
#         lyhinPituus = pituus

#         # Tallennetaan myös lyhin nimi, joka on tallennettuna muuttujaan 'rivi'
#         lyhinNimi = rivi

    
#     # Luetaan seuraava rivi
#     rivi = tiedosto.readline() 

# # suljetaan tiedosto
# tiedosto.close()
# print("Lyhin rivi oli", lyhinPituus, "merkkiä pitkä.")
# print("Se oli", lyhinNimi, end="")

######################################################
# Datan ryhmittely ja operointi osajoukon kanssa

# MALLIDATA:
# Ti;4

# Avataan tiedosto
tiedosto = open("paivadata.txt", "r", encoding="utf-8")
# Edetään rivi kerrallaan
rivi = tiedosto.readline()

# Alustetaan muuttujat
summa = 0
ryhmaEdellinen = rivi[0:2]

while len(rivi) > 0:
    rivi = rivi.rstrip()

    # Määritellään ryhmä, jonka arvo on päivämäärän lyhenne, esim. 'Ti' tai 'Ke'
    ryhma = rivi[0:2]
    # Määritellään data, jonka arvo on päivämäärän kokonaisluku
    data = int(rivi[3:])

    # Jos ryhmä on sama kuin edellinen, lisätään data eli kokonaisluku edelliseen summaan ja jatketaan
    if ryhma == ryhmaEdellinen:
        summa = summa + data
    # Kun päivämäärän lyhenne muuttuu, tulostetaan edellisen ryhmän summa ja nollataan arvot uutta ryhmää varten
    else:
        print(ryhma, summa)
        summa = data
        ryhmaEdellinen = ryhma

    # Siirrytään seuraavaan ryhmään 
    rivi = tiedosto.readline()

tiedosto.close()
# print(ryhmaEdellinen, summa)
print("Ryhmä {0:>5s} : {1:>5d}".format(ryhmaEdellinen, summa))

        


