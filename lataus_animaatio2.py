def lataus_animaatio():
    lataus_prosentti = 0
    
    for i in range(101):
        viivakerroin = 25
        viivat = "-" * viivakerroin
        edistyslista = list(viivat)
        
        baari = str(i) + "%" + "\t" + "|" + ''.join(edistyslista) + "|"
        print(baari)
        
##        i += 1
        prosentit = int(i)

        for j in range(4):
            viivat[0:edistyslista(len):1] = '#'
        
        
        
                       
        



lataus_animaatio()
