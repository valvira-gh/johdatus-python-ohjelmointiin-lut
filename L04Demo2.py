# Toistorakenteet ja laajennokset
# LUT, Johdatus Python-ohjelmointiin, viikko 4, Demo 2

##########################################################
# for

##syote = input("Anna ensimmäinen luku: ")
##alku = int(syote)
##syote = input("Anna yläraja luku: ")
##loppu = int(syote)
##
##for i in range(alku, loppu+1):
##    if ((i % 2) == 0):
##        print(i)
##    

##########################################################
# while

##aanennopeus = 340
##syote = input("Anna kulunut aika (s, 0 lopettaa): ")
##aika = int(syote)
##
##while (aika > 0):
##    etaisyys = aika * aanennopeus / 1000
##    print("Salama löi", etaisyys, "km:n päässä")
##    syote = input("Anna kulunut aika (s, 0 lopettaa): ")
##    aika = int(syote)
##
##print("Ohjelman lopetus.")


##########################################################
# KESKIARVON LASKENTA
### TAPA 1 - lukumäärä tiedossa
##summa = 0
##for kurssi in [1,2,3,4,5,6,7,8]:
##    kehote = "Anna " + str(kurssi) + ". arvosana: "
##    syote = input(kehote)
##    arvosana = int(syote)
##    summa = summa + arvosana
##    
##keskiarvo = summa / 8
##print("Keskiarvo on", keskiarvo)
##print("Ohjelman lopetus")
##


# TAPA 2 - lukumäärä tiedossa - range-funktio
##summa = 0
##syote = input("Monenko arvosanan keskiarvo lasketaan: ")
##lkm = int(syote)
##
##for kurssi in range(1, lkm+1):
##    kehote = "Anna " + str(kurssi) + ". arvosana: "
##    syote = input(kehote)
##    arvosana = int(syote)
##    summa = summa + arvosana
##    
##keskiarvo = summa / lkm
##print("Keskiarvo on", keskiarvo)
##print("Ohjelman lopetus")
##


### TAPA 3 - while - muuten sama
##
##summa = 0
##kurssi = 1
##syote = input("Monenko arvosanan keskiarvo lasketaan: ")
##kursseja = int(syote)
##
##while (kurssi < kursseja + 1):
##    kehote = "Anna " + str(kurssi) + ". arvosana: "
##    syote = input(kehote)
##    arvosana = int(syote)
##    summa = summa + arvosana
##    kurssi = kurssi + 1
##    
##keskiarvo = summa / (kurssi - 1)
##print("Keskiarvo on", keskiarvo)
##print("Ohjelman lopetus")


# TAPA 4 - while - käyttäjä antaa lopetusmerkin

summa = 0
lkm = 1
syote = input("Anna arvosana (-1 lopettaa): ")
arvosana = int(syote)

while (arvosana > -1):
    summa = summa + arvosana
    lkm = lkm + 1
    syote = input("Anna arvosana (-1 lopettaa): ")
    arvosana = int(syote)

if (lkm > 0):
    keskiarvo = summa / lkm
    print("Keskiarvo on", keskiarvo)
else:
    print("Ei voi laskea nollalla")
    
print("Ohjelman lopetus")

##########################################################


##########################################################


##########################################################


##########################################################
