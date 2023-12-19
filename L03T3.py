# Johdatus Python-ohjelmointiin, LUT, viikko 3, tehtävä 3
#########################################################
# Yksinkertainen taskulaskin


# Käyttäjäsyötteet

syote = input("Anna ensimmäinen luku: ")
luku1 = int(syote)
syote = input("Anna toinen luku: ")
luku2 = int(syote)


# Toimintojen tulostus

print("Laskin osaa seuraavat toiminnot:")
print("1) Summa\n2) Erotus\n3) Tulo\n4) Osamäärä\n5) Potenssi")
print(f"Antamasi luvut ovat {luku1} ja {luku2}")
valinta = input("Valitse toiminto (1-5): ")


# Valintarakenne

if (valinta == '1'):
    summa = luku1 + luku2
    print(f"Summa {luku1} + {luku2} = {summa}")
elif (valinta == '2'):
    erotus = luku1 - luku2
    print(f"Erotus {luku1} - {luku2} = {erotus}")
elif (valinta == '3'):
    tulo = luku1 * luku2
    print(f"Tulo {luku1} * {luku2} = {tulo}")
elif (valinta == '4'):
    if (luku2 == 0):
        print("Nollalla ei voi jakaa.")
    else:
        osamaara = luku1 / luku2
        osamaara = round(osamaara, 2)
        print(f"Osamäärä {luku1} / {luku2} = {osamaara}")
elif (valinta == '5'):
    potenssi = luku1 ** luku2
    print(f"Potenssi {luku1} ** {luku2} = {potenssi}")
else:
    print("Toimintoa ei tunnistettu.")

          
    
    

# Ohjelman lopetus
print("Kiitos ohjelman käytöstä.")
