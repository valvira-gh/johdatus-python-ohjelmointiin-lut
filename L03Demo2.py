# Ohjelmointia Pythonilla, LUT, viikko 3, luento 2

### Valintarakenne, ehdollinen koodi, koodin haarautuminen,
### yleinen valintarakenne ja logiikka

##########################################################

# Valintarakenne, ehdollinen suorittaminen
x = 1
if (x):
    print(x)
    print(x)

##########################################################
# Ehdollinen koodi

##syote = input("Anna jaettava: ")
##jaettava = int(syote)
##syote = input("Anna jakaja: ")
##jakaja = int(syote)
##
##if (jakaja != 0):
##    tulos = jaettava / jakaja
##    print(tulos)
##
##print("Loppu.")

##########################################################
# Haarautuva koodi

##syote = input("Anna jaettava: ")
##jaettava = int(syote)
##syote = input("Anna jakaja: ")
##jakaja = int(syote)
##
##if (jakaja != 0):
##    tulos = jaettava / jakaja
##    print(tulos)
##else:
##    print("Jakaja ei voi olla nolla.")
##
##
##
##print("Loppu.")


##########################################################

# Yleinen valintarakenne

##syote = input("Luku 1: ")
##x = int(syote)
##syote = input("Luku 2: ")
##y = int(syote)
##
##if (x == y):
##    # Koodilohkon kommentti - selitys
##    print("Ehdollinen koodi.")
##    print("Luvut ovat yhtä suuria.")
##elif (x > y):
##    print("elif-haara")
##    print("Luku 1 suurempi kuin luku 2.")
##elif (x < y):
##    print("toinen elif-haara")
##    print("Luku 2 suurempi kuin luku 1.")
##else:
##    print("muutoin - odottamaton lopputulos")
##


##########################################################
# Syntaksi tärkeää tulkin (interptereter) kannalta
# Logiikka tärkeää - vaikuttaa tulokseen

luku = int(input("Anna luku: "))
print("if-elif-else")
if (luku < 10):
    print("Pienempi kuin kymmenen")
elif (luku < 100):
    print("Pienempi kuin sata")
elif (luku < 1000):
    print("Pienempi kuin tuhat")
else:
    print("Suurempi tai yhtä suuri kuin tuhat")


print("if-elif-else")
if (luku < 10):
    print("Pienempi kuin kymmenen")
if (luku < 100):
    print("Pienempi kuin sata")
if (luku < 1000):
    print("Pienempi kuin tuhat")
if (luku >= 1000):
    print("Suurempi tai yhtä suuri kuin tuhat")


print("if-elif-else")
if (luku < 1000):
    print("Pienempi kuin tuhat")
elif (luku < 100):
    print("Pienempi kuin sata")
elif (luku < 10):
    print("Pienempi kuin kymmenen")
else:
    print("Suurempi tai yhtä suuri kuin tuhat")



##########################################################
# eof
