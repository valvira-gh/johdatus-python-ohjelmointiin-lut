# Johdatus Python-ohjelmointiin, LUT, viikko 3, tehtävä 3
#########################################################


# Käyttäjäsyötteet
syote = input("Anna sana 1: ")
sana1 = str(syote)
syote = input("Anna sana 2: ")
sana2 = str(syote)


# 1. osio: Sanavertailu
#######################
if (sana1 == sana2):
    print("Sanat ovat samoja.")
elif (sana1 < sana2):
    print(f"'{sana1}' on aakkosissa aiemmin kuin '{sana2}'.")
elif (sana1 > sana2):
    print(f"'{sana2}' on aakkosissa aiemmin kuin '{sana1}'.")


# 2. osio: Onko sanassa kirjainta 'z'
#####################################
if ('z' in sana1):
    print("Kirjain 'z' löytyy sanasta 1.")
if ('z' in sana2):
    print("Kirjain 'z' löytyy sanasta 2.")
else:
    print("Kummastakaan sanasta ei löytynyt kirjainta 'z'.")


# 3. osio: Onko sana palindromi
###############################
syote = input("Anna testattava sana: ")
sana_oikeinpain = str(syote)
sana_vaarinpain = sana_oikeinpain[::-1]

if (sana_oikeinpain == sana_vaarinpain):
    print("Antamasi sana", "'" + sana_oikeinpain + "'", "on palindromi.")
else:
    print("Antamasi sana ei ole palindromi.")
    print(f"Se on väärinpäin '{sana_vaarinpain}' ja oikein päin '{sana_oikeinpain}'.")


# Ohjelman lopetus
print("Kiitos ohjelman käytöstä.")
    


