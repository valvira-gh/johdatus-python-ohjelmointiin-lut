# OHJELMOINTIA PYTHONILLA, LUT, VIIKKO 2, TEHTÄVÄ 5

# OHJELMAN ALKU
print("Tämä ohjelma laskee antamiesi 3 luvun keskiarvon.")

# Syötteet
syote = input("Anna luku 0 ja 10 väliltä: ")
luku1 = int(syote)

syote = input("Anna toinen luku 0 ja 10 väliltä: ")
luku2 = int(syote)

syote = input("Anna kolmas luku 0 ja 10 väliltä: ")
luku3 = int(syote)


# Laskenta
summa = luku1 + luku2 + luku3
keskiarvo_des = float((luku1 + luku2 + luku3) / 3)
keskiarvo_int = int(keskiarvo_des)
keskiarvo_3 = round(keskiarvo_des, 3)


# Tulostus
print("\n" + "Antamiesi lukujen summa on", summa, end=".\n")
print("Antamiesi lukujen keskiarvo on", keskiarvo_des, end=".\n")
print("Keskiarvo on kokonaislukuna", keskiarvo_int, end=".\n")
print("Keskiarvo pyöristettynä 3 desimaalin tarkkuuteen on", keskiarvo_3, end=".\n")


# OHJELMAN LOPETUS
print("Kiitos ohjelman käytöstä.")
