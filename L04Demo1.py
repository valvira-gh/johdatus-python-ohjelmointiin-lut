# LUT, viikko 4, Demo 1
#######################
# TOISTORAKENTEET: for ja while
#######################


# Alkuehtoinen toistorakenne
##i = 1
##while (i <= 10):
##    print(i)
##    i = i + 1


#####################################
# Askeltava toisto

##for i in [1,2,3,4,5,6,7,8,9,10]:
##    print(i)

##Alku = 1
##Loppu = 10
##Askel = 1
# range()-funktio ottaa parametrit start, stop ja step.
##for i in range(Alku, Loppu, Askel):
##    print(i)

# Käytännössä pelkkä stop riittää
##for i in range(Loppu):
##    print(i)


#####################################
# continue

# Toistetaan luvut 1:stä 101:een, muttei 101.
##for i in range(1, 101):
##    # Jos luku on kymmenellä jaollinen, hypätään yli käyttämällä 'continue'
##    if ((i % 10) == 0):
##        continue
##    # Else, eli printataan luvut paitsi kymmenellä jaolliset 1:stä 101:een-
##
##print(i)


######################################
# break

# Toistetaan luvut 1:sta 101:een, kunnes tulee ensimmäinen kymmenellä jaollinen
# luku, jolloin 'break':in avulla hypätään toistorakenteesta pois ennenaikaisesti
##for i in range(1,101):
##    if ((i % 10) == 0):
##        break
##    print(i)


#####################################
# Monta ehtoa

##Lkm = 1
##Jatka = True
##
### Ohjelma jatkuu, jos käyttäjä haluaa jatkaa sen ajoa.
### 'Lkm' kasvaa joka kierroksella yhdellä ja lopulta ohjelma loppuu
### kun Lkm ei enää ole pienempi kuin 10
##while ((Lkm < 10) and (Jatka == True)):
##    print("Luku on", Lkm)
##    Syote = input("Haluatko jatkaa (k/e): ")
##    if ((Syote == 'e') or (Syote == 'E')):
##        Jatka = False
##    Lkm = Lkm + 1
##print("Ohjelma loppui.")
##


#####################################
# Loppuehtoinen toisto

Summa = 0
Lkm = 0
while (True):
    Syote = input("Anna luku (0 lopettaa): ")
    Luku = int(Syote)
    Summa = Summa + Luku
    Lkm = Lkm + 1
    if (Luku == 0):
        Lkm = Lkm - 1
        break

print("Keskiarvo on " + str(round((Summa/Lkm), 1)) + ".")

##

#####################################
#

##for i in range(10):
##    print(i)
##
##
##while (i < 10):
##    print(i)
##    i = i + 1
##

#####################################
######################
# eof

