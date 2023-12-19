####################
# TIEDONKÄSITTELY

##def tiedosto_kirjoita(nimi):
##    tiedosto = open(nimi, 'w')
##    for i in range(10):
##        tiedosto.write(str(i)+'\n')
##    tiedosto.close()
##    return None
##def tiedosto_lue(nimi):
##    tiedosto = open(nimi, 'r')
##    rivi = tiedosto.readline()
##    while (len(rivi) > 0):
##        print(rivi, end='')
##        rivi = tiedosto.readline()
##    tiedosto.close()
##    return None
##
##def paaohjelma():
##    tiedosto_nimi =  "L06D1T1.txt"
##    tiedosto_kirjoita(tiedosto_nimi)
##    tiedosto_lue(tiedosto_nimi)
##    return None
##    
##paaohjelma()


#######################
# JÄSENFUNKTIOT

##Merkkijono = "Tämä on lause"
##print(Merkkijono)
##print(Merkkijono.upper()) # kaikki isoksi
##print(Merkkijono.lower()) # kaikki pieneksi
##print(Merkkijono.capitalize()) # eka isoksi
##print(Merkkijono.isdigit()) # onko numero
##print(Merkkijono.isalpha()) # onko kirjaimia (välilyönnit ja pisteet antaa false)
##
##numero = '123'
##print(numero.isdigit())

#############################3
# MERKKIJONOJEN MUOTOILU

Luku = 4.1234
print("Tähän tulee luku", Luku, ".")
print("Tähän tulee luku" + str(Luku) + ".")
print("Tähän tulee luku" + str(round(Luku, 2)) + ".")
print("Tähän tulee luku" , str(round(Luku, 0)) + ".")
print("Tähän tulee luku" , str(round(Luku, 0))[:-2] + ".")

# .format()
print("Tähän tulee luku {0:1d}, kahdella desimaalilla: {0:3.2f}.".format(5))











#########
# eof
