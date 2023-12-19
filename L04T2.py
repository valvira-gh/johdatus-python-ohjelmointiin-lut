# Johdatus Python-ohjelmointiin, LUT, viikko 4, tehtävä 2
# Loppuehtoinen toistorakenne


summa = 0
lkm = 0

while (True):
    syote = input("Anna kurssiarvosana väliltä 1-5 (-1 lopettaa): ")
    arvosana = int(syote)
    
    if (arvosana == -1):
        break
    elif (1 <= arvosana <= 5):
        summa = summa + arvosana
        lkm = lkm + 1
    else:
        print("Väärä syöte. Vain arvosanat 1-5 kelpaavat (-1 lopettaa).")
        

if (lkm > 0):
    keskiarvo = str(round(summa / lkm, 2))
    print("Arvosanojen keskiarvo on", keskiarvo + ".")
else:
    print("Ei annettuja arvosanoja.")

print("Kiitos ohjelman käytöstä.")
