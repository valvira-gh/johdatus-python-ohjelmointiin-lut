# OHJELMOINTI PYTHONILLA LUT VIIKKO 2, TEHTÄVÄ 4


# KIINTOARVOT
PII = 3.14


######
# I: Positiivinen kokonaisluku kerrottuna itsellään

# Syöte ja muuttujien määrittely
syote = input("Anna positiivinen kokonaisluku: ")
kokonaisluku = int(syote)

# Laskenta
kerrottuna = kokonaisluku * kokonaisluku

# Tulostus
print("Luku", kokonaisluku, "kerrottuna itsellään on", kerrottuna)


######
# II: Ympyrän säde, kehä ja pinta-ala
# Kaavat: Ympyrän kehä: C = 2πr || Ympyrän pinta-ala: A = πr^2

# Syöte ja muuttujien määrittely
syote = input("Anna ympyrän säteen pituus kokonaislukuna: ")
r = int(syote)

# Laskenta
C = 2 * PII * r
A = PII * r ** 2

# Tulostus
print(f"Ympyrän säde on {r}, kehä on {C} ja pinta-ala on {A}.")


######
# III: Suorakulmion sivut, kehä ja pinta-ala
# Kaavat:
# Suorakulmion sivut:       a ja b
# Suorakulmion kehä:        P = 2a + 2b
# Suorakulmion pinta-ala:   A = a * b

# Syöte ja muuttujien määrittely
syote = input("Anna suorakulmion yhden sivun pituus kokonaislukuna: ")
a = int(syote)
syote = input("Anna suorakulmion toisen sivun pituus kokonaislukuna: ")
b = int(syote)

# Laskenta
P = (2 * a) + (2 * b)
A = a * b


# Tulostus
print(f"Suorakulmion sivut ovat {a} ja {b}; kehä on {P}; ja pinta-ala on {A}.")

######
# OHJELMAN LOPETUS
print("Kiitos ohjelman käytöstä.")
