# Ohjelmointia Pythonilla, LUT, viikko 3, tehtävä 1
#######################

# Syöte käyttäjältä
syote = input("Anna kokonaisluku: ")
luku = int(syote)


# Laskenta ja vertailurakenne
if (luku < 10):
    print("Luku on pienempi kuin 10.")
else:
    print("Luku on suurempi tai yhtä suuri kuin 10.")
    
if (luku % 2 == 0):
    print("Antamasi luku on parillinen.")
else:
    print("Antamasi luku on pariton.")


# Ohjelman lopetus
print("Kiitos ohjelman käytöstä.")

