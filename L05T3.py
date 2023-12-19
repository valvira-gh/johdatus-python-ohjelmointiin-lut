
def tulostaTeksti(teksti, luku):
    for i in range(luku):
        print(teksti)
    return None


def paaohjelma():
    while True:
        # 1. vaihe
        # Syötteet käyttäjältä
        syote = input("Anna teksti: ")
        teksti = syote

        if syote != "lopeta":
            syote = input("Anna luku: ")
            
        if syote != "lopeta":
            luku = int(syote)
            tulostaTeksti(teksti, luku)
            print()
        
        else:
            print("Lopetetaan.")
            break

    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()