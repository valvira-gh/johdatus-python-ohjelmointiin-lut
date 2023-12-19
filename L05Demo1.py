# Johdanto Python-ohjelmointiin, LUT, viikko 5, Demo 1
# ALIOHJELMARAKENNE PÄÄTASON KOODISTA: pää- ja aliohjelmien perusasiat ja käyttö
################################################################################

#####################################
# Pääohjelmarakenne

##def paaohjelma():
##    print("Tämä on palindromi-sovellus.")
##    print("Anna sana ja sovellus kertoo onko kyseessä palindromi-sana.")
##    syote = input("Anna sana: ")
##    sana_oikeinpain = str(syote)
##    sana_vaarinpain = sana_oikeinpain[::-1]
##    print(f"Antamasi sana '{sana_oikeinpain}' on väärinpäin '{sana_vaarinpain}'.")
##    if sana_oikeinpain == sana_vaarinpain:
##        print("Sana", sana_oikeinpain, "on siis palindromi! :D")
##    else:
##        print("Kyseessä ei näin ollen ole palindromi :(")
##    print("Kiitos ohjelman käytöstä.")
##    return None
##
##paaohjelma()
    

#####################################
# Aliohjelmat
# aliohjelmat ja pääohjelma

def tulostaOhjeet():
    print("Tämä on palindromi-sovellus.")
    print("Anna sana ja sovellus kertoo onko kyseessä palindromi-sana.")
    return None

def kysySana():
    syote = input("Anna sana: ")
    sana = str(syote)
    sana = sana.lower()
    return sana

def kasitteleSana(sana):
    sana_vaarinpain = sana[::-1]
    print(f"Antamasi sana '{sana}' on väärinpäin '{sana_vaarinpain}'.")
    return sana_vaarinpain

def tarkistaPalindromi(sana_oikein, sana_vaarinpain):
    if sana_oikein == sana_vaarinpain:
        print("Sana", "'" + sana_oikein + "'", "on siis palindromi! :D")
    else:
        print("Kyseessä ei näin ollen ole palindromi :(")
    return None

def paaohjelma():
    tulostaOhjeet()
    sana_oikein = kysySana()
    sana_vaarin = kasitteleSana(sana_oikein)
    tarkistaPalindromi(sana_oikein, sana_vaarin)

    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()


#####################################
# eof


#####################################


#####################################


#####################################


#####################################


#####################################
