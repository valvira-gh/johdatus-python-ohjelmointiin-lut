print("******************************\n" +
    " *Palkanlaskentaohjelma 3000*\n" +
      "******************************"
    )

Nimi = input("Anna nimesi: ") 
Syote = input("Anna tuntipalkkasi: ") # e/h

Tuntipalkka = float(Syote)
Syote = input("Anna työaika viikossa: ") # h

TuntejaViikko = float(Syote)
TuntejaKuukausi = float(TuntejaViikko * 4.1)
Paiva = int(Tunteja_Viikko / 7 * Tuntipalkka)

Paivapalkka = int(Paiva)
Viikkopalkka = int(Tuntipalkka * TuntejaViikko)
Kuukausipalkka = int(Tuntipalkka * 4.1)

Jatkuvuus_Syote = input(
    "Anna tarkkuus:\n\t(1) Päivä\n\t(2) Viikko\n\t(3) Kuukausi\n\t(0)Päätä ohjelma\nVastaus:\t"
    )
ViikkoViesti = "\nHenkilön", Nimi, "viikkopalkka on", Viikkopalkka, "euroa / viikko"



Jatkuvuus = int(Jatkuvuus_Syote)
print("Käytttäjän", Nimi, "valinta:", Jatkuvuus) 


def Laske_Lopputulos():
    if(Jatkuvuus == 1):
        print("Henkilön", Nimi, "päiväpalkka oli keskimäärin:", Paivapalkka)
    elif(Jatkuvuus == 2):
         print("Valinta on 2")
    elif(Jatkuvuus == 3):
        print("Valinta on 3")

    else:
        print("Tee valinta lukujen 1, 2, 3 ja 0 joukosta!", end='\n')
        



