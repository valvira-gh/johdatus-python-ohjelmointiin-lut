Alkuperainen_sana = input("Anna pitkä Sana: ")

Viisi_ekaa = Alkuperainen_sana[0:5]
Viisi_vikaa = Alkuperainen_sana[-5:]
Kaksi_viisi = Alkuperainen_sana[1:5]

print("Antamasi sanan viisi ensimmäistä kirjainta ovat", Viisi_ekaa)
print("Viisi viimeistä kirjainta ovat", Viisi_vikaa)
print("Kirjaimet 2,3,4 ja 5 ovat", Kaksi_viisi, end="\n\n")

Joka_toinen = Alkuperainen_sana[1::2]
print(f"Sanan joka toinen kirjain alkaen toisesta kirjaimesta: {Joka_toinen}", end="\n\n")

Takaperin = Alkuperainen_sana[::-1]
print("Annoit sanan", "'" + Alkuperainen_sana + "',", "joka on takaperin", "'" + Takaperin + "'.", end="\n\n")

############################################################

Syote = input("Anna aloituspaikka: ")
Aloituspaikka = int(Syote)

Syote = input("Anna lopetuspaikka: ")
Lopetuspaikka = int(Syote)

Syote = input("Anna siirtymä: ")
Siirtyma = int(Syote)

Lopullinen_sana = Alkuperainen_sana[Aloituspaikka:Lopetuspaikka:Siirtyma]

print("Antamillasi asetuksilla sana", Alkuperainen_sana, "tulostuu näin:", Lopullinen_sana, end="\n\n")

Sanan_pituus = len(Alkuperainen_sana)
print(f"Sana oli {Sanan_pituus} merkkiä pitkä.")

Lopputeksti = "Kiitos ohjelman käytöstä."
print(Lopputeksti)

