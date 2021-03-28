import random as r
import math as m
from copy import deepcopy as dc


def calculeaza_lungime(precizie, a, b):
    return m.floor(abs(m.log((b - a) * 10 ** precizie, 2)) + 1)


def populatie_initiala(dimensiune_populatie, lungime_cromozom):
    return [[r.randint(0, 1) for i in range(lungime_cromozom)] for j in range(dimensiune_populatie)]


def binary_to_decimal(x):
    copie_x = dc(x)
    copie_x = int(''.join(str(e) for e in copie_x))
    baza10, i, n = 0, 0, 0
    while copie_x != 0:
        baza10 = baza10 + (copie_x % 10) * pow(2, i)
        copie_x = copie_x // 10
        i += 1
    return baza10


def codificare_cromozom(cromozom, a, b):
    cromozom_baza_10 = binary_to_decimal(cromozom)
    lungime = len(cromozom)
    return round(((b - a) * cromozom_baza_10) / (pow(2, lungime) - 1) + a, 6)


def interval_din_coeficienti(a, b, c):
    delta = pow(b, 2) - 4 * a * c
    return (-b + m.sqrt(delta)) / 2 * a, (-b - m.sqrt(delta)) / 2 * a


def fitness(x, a, b, c):
    return a * pow(x, 2) + b * x + c


def binary_search(lista, elem):
    i = 0
    j = len(lista) - 1
    while i < j:
        mijloc = (i + j) // 2
        if lista[mijloc] <= elem < lista[mijloc + 1]:
            return mijloc
        elif elem >= lista[mijloc]:
            i = mijloc + 1
        else:
            j = mijloc
    return -1


def incruciseaza_2_cromozomi(a, b, u):
    return a[:u] + b[u:], b[:u] + a[u:]


def incruciseaza_3_cromozomi(a, b, c, u):
    return a[:u] + b[u:], b[:u] + c[u:], c[:u] + a[u:]


if __name__ == '__main__':
    f_out = open("fisier.out", "w")
    # f_test = open("test.txt", "r")
    f_in = open("date.in", "r")

    # date citite din fisier -----------------------------------------------------------

    precizie = int(f_in.readline())
    print("Precizie: ", precizie)

    x = int(f_in.readline())
    y = int(f_in.readline())
    z = int(f_in.readline())

    dimensiune_populatie = int(f_in.readline())
    probabilitate_incrucisare = float(f_in.readline())
    probabilitate_mutatie = float(f_in.readline())
    nr_generatii = int(f_in.readline())

    # date citite din fisier -----------------------------------------------------------

    a, b = interval_din_coeficienti(x, y, z)
    lungime = calculeaza_lungime(precizie, a, b)

    print("Lungimea cromozomilor: ", lungime)
    print("Intervalul functiei de fitness: ", a, b)
    print("Dimensiunea populatiei: ", dimensiune_populatie)
    print("Probabilitate de incrucisare: ", probabilitate_incrucisare)
    print("Probabilitate de mutatie: ", probabilitate_mutatie)

    populatie = populatie_initiala(dimensiune_populatie, lungime)
    # iau un semafor pentru a afisa doar o data in fisier
    afiseaza = True

    # aici incepe for-ul pentru generatii ----------------------------------------------

    for k in range(nr_generatii):
        # valorile pe axa Ox ale cromozomilor
        cromozomi_codificati = []
        for i in range(dimensiune_populatie):
            cromozomi_codificati.append(codificare_cromozom(populatie[i], a, b))
        print("x: ", cromozomi_codificati)

        # valorile de fitness pentru fiecare cromozom
        fitness_cromozomi = []
        for i in range(dimensiune_populatie):
            fitness_cromozomi.append(fitness(cromozomi_codificati[i], x, y, z))
        print("Fitness: ", fitness_cromozomi)

        if afiseaza:
            f_out.write("Populatia initiala\n")
            for i in range(dimensiune_populatie):
                f_out.write(f"""{i+1}: {''.join(str(x) for x in populatie[i])} x= {cromozomi_codificati[i]} f= {fitness_cromozomi[i]}\n""")

        # selectez elementul elitist, il elimin din lista de cromozomi si din lista de fitness
        indice_elitist = fitness_cromozomi.index(max(fitness_cromozomi))
        cromozom_elitist = dc(populatie[indice_elitist])
        fitness_cromozomi.remove(fitness_cromozomi[indice_elitist])
        populatie.remove(populatie[indice_elitist])
        cromozomi_codificati.remove(cromozomi_codificati[indice_elitist])
        dimensiune_populatie -= 1

        # suma tuturor valorilor de fitness ale cromozomilor
        suma_fitness = 0
        for i in range(dimensiune_populatie):
            suma_fitness += fitness_cromozomi[i]
        print("Suma fitness: ", suma_fitness)

        # probabilitatea de selectare pentru fiecare cromozom in parte
        probabilitati_selectare = []
        for i in range(dimensiune_populatie):
            probabilitati_selectare.append(fitness_cromozomi[i] / suma_fitness)
        print("prob selectare: ", probabilitati_selectare)

        # calculez o lista de intervale cu ajutorul unei sumae partiale calculata din probabilitatile de selectare
        intervale_selectie = []
        suma_partiala = 0
        for i in range(dimensiune_populatie):
            intervale_selectie.append(suma_partiala)
            suma_partiala += probabilitati_selectare[i]
        intervale_selectie.append(1)
        print("intervale: ", intervale_selectie)

        if afiseaza:
            f_out.write("\nProbabilitati de selectie \n")
            for i in range(dimensiune_populatie):
                f_out.write(f"""cromozom {i+1} probabilitate {probabilitati_selectare[i]}\n""")
            f_out.write("\nIntervalele de selectie\n")
            for i in range(dimensiune_populatie+1):
                f_out.write(f"""{intervale_selectie[i]}\n""")
            f_out.write("\nCromozomi selectati\n")

        # iau indicii cromozomilor care vor merge mai departe in mod aleator si la fel si pt cei ce merg la incrucisare
        indici_cromozomi_selectati = []
        cromozomi_selectati = []
        indici_incrucisare = []
        indici_mutatie = []
        for i in range(dimensiune_populatie):
            # iau o variablia u random pentru a vedea in ce interval se incadreaza si ce cromozom selectez pt a merge
            # mai departe
            u = r.random()
            indice = binary_search(intervale_selectie, u)
            indici_cromozomi_selectati.append(indice)
            cromozomi_selectati.append(populatie[indice])

            if afiseaza:
                f_out.write(f"""u= {u} selectam cromozomul {indice+1}\n""")

        if afiseaza:
            f_out.write("\nProbabilitati de incrucisare\n")

        for i in range(dimensiune_populatie):
            # generez apoi o alta variabila random pentru a vedea daca acel cromozom se incadreaza la incrucisare
            u = r.random()
            if u < probabilitate_incrucisare:
                indici_incrucisare.append(i)
                if afiseaza:
                    f_out.write(f"""{i+1}: {''.join(str(x) for x in cromozomi_selectati[i])} u={u} < 0.25 participa\n""")
            else:
                if afiseaza:
                    f_out.write(f"""{i+1}: {''.join(str(x) for x in cromozomi_selectati[i])} u={u}\n""")

        for i in range(dimensiune_populatie):
            # generez iar o variabila random pentru a selecta cromozomul la mutatie
            u = r.random()
            if u < probabilitate_mutatie:
                indici_mutatie.append(i)

        print("Indicii celor ce merg mai departe: ", indici_cromozomi_selectati)
        print("Cromozomi selectati: ", cromozomi_selectati)
        print("Indicii celor selectati pentru incrucisare: ", indici_incrucisare)

        # daca am mai mult de un cromozom de incrucisat
        # iterez prin lista de indici de incrucisare si iau cate doua elemente random din lista de cromozomi selectati
        # in functie de punctul de rupere u generat random
        if len(indici_incrucisare) > 1:
            if len(indici_incrucisare) % 2 == 1:
                # daca lungimea listei de indici e impara, trebuie sa incrucisez 3 cromozomi o data
                indice_1 = dc(r.choice(indici_incrucisare))
                indici_incrucisare.remove(indice_1)
                print("Indice 1: ", indice_1)
                indice_2 = dc(r.choice(indici_incrucisare))
                indici_incrucisare.remove(indice_2)
                print("Indice 2: ", indice_2)
                indice_3 = dc(r.choice(indici_incrucisare))
                indici_incrucisare.remove(indice_3)
                print("Indice 3: ", indice_3)

                # iau u punct de rupere in cromozomi
                u = r.randrange(0, lungime)
                print("Punct de rupere: ", u)

                if afiseaza:
                    f_out.write(f"\nRecombinare cromozomii {indice_1+1} cu {indice_2+1} si {indice_3+1}:\n")
                    f_out.write(f"""{''.join(str(x) for x in cromozomi_selectati[indice_1])} {''.join(str(x) for x in cromozomi_selectati[indice_2])} {''.join(str(x) for x in cromozomi_selectati[indice_3])} punct {u}\n""")

                # incrucisez cei 3 cromozomi
                cromozomi_selectati[indice_1], cromozomi_selectati[indice_2], cromozomi_selectati[indice_3] = \
                    incruciseaza_3_cromozomi(cromozomi_selectati[indice_1], cromozomi_selectati[indice_2],
                                             cromozomi_selectati[indice_3], u)

                if afiseaza:
                    f_out.write(f"""Rezultat: {''.join(str(x) for x in cromozomi_selectati[indice_1])} {''.join(str(x) for x in cromozomi_selectati[indice_2])} {''.join(str(x) for x in cromozomi_selectati[indice_3])}\n""")
                print("------------------")

            while len(indici_incrucisare) >= 2:
                # iau 2 indici random din lista de indici de incrucisare
                indice_1 = dc(r.choice(indici_incrucisare))
                indici_incrucisare.remove(indice_1)
                print("Indice 1: ", indice_1)
                indice_2 = dc(r.choice(indici_incrucisare))
                indici_incrucisare.remove(indice_2)
                print("indice 2: ", indice_2)

                # iau u punct de rupere in cromozomi
                u = r.randrange(0, lungime)
                print("Punct de rupere: ", u)

                if afiseaza:
                    f_out.write(f"\nRecombinare cromozomii {indice_1+1} cu {indice_2+1}:\n")
                    f_out.write(f"""{''.join(str(x) for x in cromozomi_selectati[indice_1])} {''.join(str(x) for x in cromozomi_selectati[indice_2])} punct {u}\n""")

                # incrucisez cei doi cromozomi
                cromozomi_selectati[indice_1], cromozomi_selectati[indice_2] = \
                    incruciseaza_2_cromozomi(cromozomi_selectati[indice_1], cromozomi_selectati[indice_2], u)

                if afiseaza:
                    f_out.write(f"""Rezultat {"".join(str(x) for x in cromozomi_selectati[indice_1])} {''.join(str(x) for x in cromozomi_selectati[indice_2])}\n""")

                print("------------------")

        print("Indicii celor selectati pentru mutatie: ", indici_mutatie)

        if afiseaza:
            f_out.write("\nProbabilitate de mutatie pentru fiecare cromozom 0.01\n")
            if len(indici_mutatie) > 0:
                f_out.write("Au fost selectati cromozomii:\n")
                for i in range(len(indici_mutatie)):
                    f_out.write(f"""{indici_mutatie[i]+1}\n""")
            else:
                f_out.write("Nu a fost selectat niciun cromozom pentru mutatie! :(\n")

            f_out.write("\nDupa incrucisari si mutatii:\n")
            for i in range(dimensiune_populatie):
                f_out.write(f"""{i+1}: {''.join(str(x) for x in cromozomi_selectati[i])} x= {codificare_cromozom(cromozomi_selectati[i], a, b)} f= {fitness(codificare_cromozom(cromozomi_selectati[i], a, b), x, y, z)}\n""")
            f_out.write("\nEvolutia maximului si a average-ului:\n")

        f_out.write(f"{fitness(codificare_cromozom(cromozom_elitist, a, b), x, y, z)} -- {(suma_fitness+fitness(codificare_cromozom(cromozom_elitist, a, b), x, y, z))/20}\n")

        # iau cromozomii din lista si modific cate o gena selectata random
        for i in range(len(indici_mutatie)):
            u = r.randrange(0, lungime)
            print("Am modificat gena nr ", u + 1, " a cromozomului ", indici_mutatie[i])
            print("Cromozomul nemodificat: ", cromozomi_selectati[indici_mutatie[i]])
            cromozomi_selectati[indici_mutatie[i]][u] = 0 if cromozomi_selectati[indici_mutatie[i]][u] == 1 else 1
            print("Cromozomul modificat:   ", cromozomi_selectati[indici_mutatie[i]])

        print(cromozomi_selectati)
        populatie = dc(cromozomi_selectati)
        populatie.append(cromozom_elitist)
        dimensiune_populatie +=1
        print("Valoarea maxima: ", fitness(codificare_cromozom(cromozom_elitist, a, b), x, y, z))
        print("==================================================================================================")
        if afiseaza:
            afiseaza = False
