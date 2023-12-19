# Johdatus Python-ohjelmointiin, LUT, viikko 4, tehtävä 3
# Toistorakenne useila lopetusehdoilla

# Syötteet
syote = input("Anna a:n arvo: ")
a = int(syote)
syote = input("Anna b:n arvo: ")
b = int(syote)

while True:
    print("a:", a, "b:", b)
    if (a >= 10000):
        break
    elif (b >= 10000):
        break
    elif (a > b):
        break
    else:
        a = a * 2
        b = b + 100

    
print("Kiitos ohjelman käytöstä.")
