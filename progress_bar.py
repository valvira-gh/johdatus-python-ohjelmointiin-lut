def lataus_animaatio():
    lataus = 0
    edistysbaari = list('------------------------------')
    
    for i in range(12):  # Toistetaan 12 kertaa (0-11)
        tuloste = str(lataus) + "%" + "\t" "|" + ''.join(edistysbaari) + "|"
        print(tuloste)
        
        # Päivitetään edistysbaari tämän iteraation osalta
        for j in range(3*i, 3*(i+1)):
            if j < len(edistysbaari):
                edistysbaari[j] = '#'
        
        lataus += 10  # Kasvatetaan latausta 10% jokaisella iteraatiolla

lataus_animaatio()


       
lataus_animaatio()


##    for i in range(1, 10):
##        tuloste = str(lataus) + "%" + "\t" "|" + ''.join(edistysbaari) + "|"
##        print(tuloste)
##        # Muuta kolme viivaa kerrallaan
##        for j in range(3):
##            edistysbaari[3*(i-1)+j] = '#'
##        lataus += 10
