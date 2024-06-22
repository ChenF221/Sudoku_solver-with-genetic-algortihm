import random as rndm
import time

def generar_gen(initial=None):
    if initial is None:
        initial = [0] * 9
    mapp = {}
    gen = list(range(1, 10))
    rndm.shuffle(gen)
    for i in range(9):
        mapp[gen[i]] = i
    for i in range(9):
        if initial[i] != 0 and gen[i] != initial[i]:
            temp = gen[i], gen[mapp[initial[i]]]
            gen[mapp[initial[i]]], gen[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gen

def generar_cromosoma(initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    cromosoma = []
    for i in range(9):
        cromosoma.append(generar_gen(initial[i]))
    return cromosoma

def generar_poblacion(count, initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    poblacion = []
    for _ in range(count):
        poblacion.append(generar_cromosoma(initial))
    return poblacion

def obtener_fitness(cromosoma):
    """Calcula la aptitud de un cromosoma (rompecabezas)."""
    fitness = 0
    for i in range(9): # Para cada columna
        seen = {}
        for j in range(9): # Verifica cada celda en la columna
            if cromosoma[j][i] in seen:
                seen[cromosoma[j][i]] += 1
            else:
                seen[cromosoma[j][i]] = 1
        for key in seen: # Resta aptitud por números repetidos
            fitness -= (seen[key] - 1)
    for m in range(3): # Para cada cuadrado 3x3
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):  # Verifica celdas en cuadrado 3x3
                for j in range(3 * m, 3 * (m + 1)):
                    if cromosoma[j][i] in seen:
                        seen[cromosoma[j][i]] += 1
                    else:
                        seen[cromosoma[j][i]] = 1
            for key in seen: # Resta aptitud por números repetidos
                fitness -= (seen[key] - 1)
    return fitness

ch = generar_cromosoma()
print(obtener_fitness(ch))

def imprimir_cromosoma(ch):
    for i in range(9):
        for j in range(9):
            print(ch[i][j], end=" ")
        print("")

def cruzar(ch1, ch2):
    nuevo_hijo_1 = []
    nuevo_hijo_2 = []
    for i in range(9):
        x = rndm.randint(0, 1)
        if x == 1:
            nuevo_hijo_1.append(ch1[i])
            nuevo_hijo_2.append(ch2[i])
        elif x == 0:
            nuevo_hijo_2.append(ch1[i])
            nuevo_hijo_1.append(ch2[i])
    return nuevo_hijo_1, nuevo_hijo_2

def mutacion(ch, pm, initial):
    for i in range(9):
        x = rndm.randint(0, 100)
        if x < pm * 100:
            ch[i] = generar_gen(initial[i])
    return ch

def leer_rompecabezas(direccion):
    rompecabezas = []
    f = open(direccion, 'r')
    for fila in f:
        temp = fila.split()
        rompecabezas.append([int(c) for c in temp])
    return rompecabezas

def r_obtener_piscina_mating(populacion):
    lista_aptitudes = []
    piscina = []
    for cromosoma in populacion:
        aptitud = obtener_fitness(cromosoma)
        lista_aptitudes.append((aptitud, cromosoma))
    lista_aptitudes.sort()
    peso = list(range(1, len(lista_aptitudes) + 1))
    for _ in range(len(populacion)):
        ch = rndm.choices(lista_aptitudes, peso)[0]
        piscina.append(ch[1])
    return piscina

def w_obtener_piscina_mating(populacion):
    lista_aptitudes = []
    piscina = []
    for cromosoma in populacion:
        aptitud = obtener_fitness(cromosoma)
        lista_aptitudes.append((aptitud, cromosoma))
    peso = [fit[0] - lista_aptitudes[0][0] for fit in lista_aptitudes]
    for _ in range(len(populacion)):
        ch = rndm.choices(lista_aptitudes, weights=peso)[0]
        piscina.append(ch[1])
    return piscina

def obtener_descendencia(populacion, initial, pm, pc):
    nueva_piscina = []
    i = 0
    while i < len(populacion):
        ch1 = populacion[i]
        ch2 = populacion[(i + 1) % len(populacion)]
        x = rndm.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = cruzar(ch1, ch2)
        nueva_piscina.append(mutacion(ch1, pm, initial))
        nueva_piscina.append(mutacion(ch2, pm, initial))
        i += 2
    return nueva_piscina


def imprimir_sudoku(solucion):
    for fila in solucion:
        print(" ".join(map(str, fila)))

# Función principal del algoritmo genético
def algoritmo_genetico(initial, POBLACION, REPETICION, PM, PC, callback=None):
    poblacion = generar_poblacion(POBLACION, initial)
    mejor_solucion = None
    mejor_aptitud = float('-inf')
    solucion_encontrada = False

    for iteracion in range(REPETICION):
        piscina_mating = r_obtener_piscina_mating(poblacion)
        rndm.shuffle(piscina_mating)
        poblacion = obtener_descendencia(piscina_mating, initial, PM, PC)
        aptitudes = [obtener_fitness(c) for c in poblacion]
        m = max(aptitudes)

        # Call the callback function with the current iteration and solution
        if callback is not None:
            callback(iteracion + 1, poblacion[aptitudes.index(m)])

        # Actualizar la mejor solución si se encuentra una mejor
        if m > mejor_aptitud:
            mejor_aptitud = m
            mejor_solucion = [list(fila) for fila in poblacion[aptitudes.index(m)]]

        if m == 0:
            # Si se encuentra una solución con aptitud 0, romper el bucle
            print("Solución encontrada en la iteración {}".format(iteracion + 1))
            solucion_encontrada = True
            break

    if solucion_encontrada:
        print("Mejor Solución (Aptitud: {}):".format(mejor_aptitud))
        imprimir_sudoku(mejor_solucion)
    else:
        print("No se encontró una solución.")

    return solucion_encontrada, mejor_solucion


