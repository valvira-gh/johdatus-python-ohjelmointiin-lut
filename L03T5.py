# Johdatus Python-ohjelmointiin, LUT, viikko 3, tehtävä 5
#########################################################
# Valintarakenteen sovellusesimerkki painoindeksin laskennassa
# Kaava: painoindeksi x = massa (kg) / pituus (m)^2

# Osa 1: Painoindeksi
#####################

# Syötteet
syote = input("Anna pituus (cm): ")
pituus_cm = int(syote)
syote = input("Anna paino (kg): ")
massa = int(syote)

pituus_m = float(pituus_cm / 100)


# Painoindeksin laskenta
painoindeksi =  float(massa / pituus_m ** 2)
painoindeksi = round(painoindeksi, 1)


# Vertailurakenne
if (painoindeksi <= 17):
    indeksiluokka = "Vaarallinen aliravitsemus"
elif (17 < painoindeksi and painoindeksi < 18.5):
    indeksiluokka = "Liiallinen laihuus"
elif (18.5 <= painoindeksi and painoindeksi < 25):
    indeksiluokka = "Normaali paino"
elif (25 <= painoindeksi and painoindeksi < 30):
    indeksiluokka = "Ylipaino eli lievä lihavuus"
elif (30 <= painoindeksi and painoindeksi < 35):
    indeksiluokka = "Merkittävä lihavuus"
elif (35 <= painoindeksi and painoindeksi < 40):
    indeksiluokka = "Vaikea lihavuus"
elif (40 <= painoindeksi):
    indeksiluokka = "Sairaalloinen lihavuus"
else:
    print("Virheellinen luku, odottamaton virhe.")


# Tulostus
print(f"Painoindeksi on {painoindeksi} ({indeksiluokka})")


# Osa 2: Tavoiteindeksi
#######################
# Kaava: Massa x = Painoindeksi * Pituus(m^2)

# Käyttäjäsyöte
syote = input("Anna tavoiteindeksi: ")
tavoiteindeksi = float(syote)

# Laskenta
tavoitemassa = float(tavoiteindeksi * pituus_m ** 2)

# Vertailurakenne ja tulostus
if (tavoiteindeksi < painoindeksi):
    massan_erotus = massa - tavoitemassa
    massan_erotus = round(massan_erotus, 1)
    print(f"Tavoiteindeksi vastaa {massan_erotus} kg alhaisempaa painoa.")
elif (tavoiteindeksi > painoindeksi):
    massan_erotus = tavoitemassa - massa
    massan_erotus = round(massan_erotus, 1)
    print(f"Tavoiteindeksi vastaa {massan_erotus} kg suurempaa painoa.")
else:
    print("Tavoiteindeksi on sama kuin jo annettu painoindeksi.")


# Ohjelman lopetus
print("Kiitos ohjelman käytöstä.")


