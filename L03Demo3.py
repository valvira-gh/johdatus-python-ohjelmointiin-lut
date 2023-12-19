# LUT, Ohjelmointia Pythonilla, viikko 3, luento 3
#######################################
# VALINTARAKENNEDEMOJA
# Valintarakenne ohjelmassa
# Henkilötunnuksen tietojen tulkinta
#######################################
# Äänennopeus

##aanennopeus = 340   # m/s
##lahella = 1.5       # km
##
##syote = input("Anna kulunut aika: ")
##aika = int(syote)
##etaisyys = aika * aanennopeus / 1000
##
##if (aika < 0):
##    print("Anna positiivinen luku.")
##elif (aika == 0):
##    print("Osui kohdalle.")
##elif (etaisyys < lahella):
##    print("Osui lähelle.")
##else:
##    print("Osui kauas.")
##
##print("\nOhjelman lopetus.")


#######################################
# Henkilötunnus

htunnus = input("Anna henkilötunnus: ")

pp = htunnus[0:2]
kk = htunnus[2:4]
vv = htunnus[4:6]
vuosisata = htunnus[6:7]
jarjestysnumero = htunnus[7:10]
sukupuoli = int(htunnus[9:10])
tarkistusmerkki = htunnus[10:11]

if (vuosisata == '+'):
    vuosisata = "1800-luku"
    vuosi = "18" + vv
elif (vuosisata == '-'):
    vuosisata = "1900-luku"
    vuosi = "19" + vv
elif (vuosisata == 'A'):
    vuosisata = "2000-luku"
    vuosi = "20" + vv
else:
    print("Ongelma haarautumisessa, odottamaton virhe.")


nainen = bool
# Sukupuolen käsittely
if (sukupuoli % 2 == 0):
    nainen = True

print("Päivämäärä on", pp)
print("Kuukausi on",  kk)
print("Vuosi on", vuosi)
print("Vuosisata on", vuosisata)
print("Järjestysnumero on", jarjestysnumero)

print("Sukupuoli on", end=' ')
if (nainen == True):
    print("nainen")
else:
    print("mies")

print("Tarkistusmerkki on", tarkistusmerkki)
#######################################


#######################################


#######################################


#######################################


#######################################


#######################################
# eof
