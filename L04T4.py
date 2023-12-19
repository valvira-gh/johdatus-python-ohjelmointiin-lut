# Johdatus Python-ohjelmointiin, LUT, viikko 4, tehtävä 4
# Toistorakenteiden laajennokset


# Syötteet
alaraja = int(input("Anna alueen alaraja: "))
ylaraja = int(input("Anna alueen yläraja: "))

# Apumuuttujan alustus
loytyi = False

# Lukualueen iterointi
for luku in range(alaraja, ylaraja + 1):
    # Tarkitetaan jaollisuus 5:llä
    if luku % 5 != 0:
        print(f"{luku} ei ole jaollinen viidellä, hylätään.")
        continue

    # Tarkistetaan jaollisuus 7:llä
    if luku % 7 != 0:
        print(f"{luku} ei ole jaollinen seitsemällä, hylätään.")
        continue

    # Jos luku on jaollinen sekä 5:llä että 7:llä
    print(f"Luku {luku} on jaollinen 5:llä ja 7:llä.")
    print("Lopetetaan etsintä.")
    loytyi = True
    break

# Tarkistetaan, löytyikö sopiva luku
if not loytyi:
    print("Alueelta ei löytynyt sopivaa arvoa.")

print("Kiitos ohjelman käytöstä.")

