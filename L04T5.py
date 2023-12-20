# Johdatus Python-ohjelmointiin, LUT, viikko 4, tehtävä 5
# Valikkopohjainen taskulaskin


# Valikkorakenne while-loopilla
while True:
    print("Tämä laskin osaa seuraavat toiminnot:")

    print("1) Anna luvut")
    print("2) Summa")
    print("3) Erotus")
    print("4) Tulo")
    print("5) Osamäärä")
    print("6) Potenssi")
    print("0) Lopeta")

    syote = input("Valitse toiminto (0-6): ")
    valinta = int(syote)

    if valinta == 0:
        break
    elif valinta == 1:
        syote = input("Anna ensimmäinen luku: ")
        luku1 = int(syote)
        syote = input("Anna toinen luku: ")
        luku2 = int(syote)

        print(f"Annoit luvut {luku1} ja {luku2}")
        continue
    elif valinta == 2:
        tulos = luku1 + luku2
        print(f"Summa {luku1} + {luku2} = {tulos}")
    elif valinta == 3:
        tulos = luku1 - luku2
        print(f"Erotus {luku1} - {luku2} = {tulos}")
    elif valinta == 4:
        tulos = round(luku1 * luku2, 2)
        print(f"Tulo {luku1} * {luku2} = {tulos}")
    elif valinta == 5:
        if luku2 == 0:
            print("Nollalla ei voi jakaa.")
        else:
            tulos = round(float(luku1 / luku2), 2)
            print(f"Osamäärä {luku1} / {luku2} = {tulos}")
    elif valinta == 6:
        tulos = luku1 ** luku2
        print(f"Potenssi {luku1} ** {luku2} = {tulos}")
    elif valinta == 0:
        break
    else:
        print("Tuntematon valinta, yritä uudestaan.")

print("Lopetetaan")
print("Kiitos ohjelman käytöstä.")
        