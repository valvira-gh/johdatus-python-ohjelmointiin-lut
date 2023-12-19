# Johdatus Python-ohjelmointiiin, LUT, viikko 4, tehtävä 1
# Erilaiset toistorakenteet

# Syötteet
syote = input("Anna aloitusarvo: ")
aloitus = int(syote)
syote = input("Anna lopetusarvo: ")
lopetus = int(syote)


# Toteutus for-lauseella:
print("Toteutus for-lauseella:")

for i in range(aloitus, lopetus+1):
    print(i, end=' ')


print("\n")
# Toteutus while-lauseella
print("Toteutus while-lauseella:")

i = aloitus
while (i >= aloitus and i <= lopetus):
    print(i, end=' ')
    i = i + 1

print("\n")

print("Kiitos ohjelman käytöstä.")
