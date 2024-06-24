'''
Authors: Chen Yangfeng, Diaz Jimenez Jorge Arif, 5BM1, Escom IPN
26/jun/24  Algoritmos Bioinpirados, Proyecto Final
Sudoku_solver-with-genetic-algortihm
'''

import random
import numpy as np

def generar_gen(initial=None):
    """Genera un gen aleatorio o ajustado inicialmente."""
    if initial is None:
        initial = [0] * 9
    mapp = {}
    gen = list(range(1, 10))
    random.shuffle(gen)
    for i in range(9):
        mapp[gen[i]] = i
    for i in range(9):
        if initial[i] != 0 and gen[i] != initial[i]:
            temp = gen[i], gen[mapp[initial[i]]]
            gen[mapp[initial[i]]], gen[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gen

def generar_cromosoma(initial=None):
    """Genera un cromosoma Sudoku aleatorio o ajustado inicialmente."""
    if initial is None:
        initial = [[0] * 9] * 9
    cromosoma = []
    for i in range(9):
        cromosoma.append(generar_gen(initial[i]))
    return cromosoma

def generar_poblacion(count, initial=None):
    """Genera una población de cromosomas Sudoku."""
    if initial is None:
        initial = [[0] * 9] * 9
    poblacion = []
    for _ in range(count):
        poblacion.append(generar_cromosoma(initial))
    return poblacion

def obtener_fitness(cromosoma):
    """Calcula la aptitud de un cromosoma (Sudoku)."""
    fitness = 0

    # Evaluar filas y columnas
    for i in range(9):
        seen_row = {}
        seen_col = {}
        for j in range(9):
            # Verifica filas
            if cromosoma[i][j] in seen_row:
                seen_row[cromosoma[i][j]] += 1
            else:
                seen_row[cromosoma[i][j]] = 1

            # Verifica columnas
            if cromosoma[j][i] in seen_col:
                seen_col[cromosoma[j][i]] += 1
            else:
                seen_col[cromosoma[j][i]] = 1

        for key in seen_row:
            fitness -= (seen_row[key] - 1)
        for key in seen_col:
            fitness -= (seen_col[key] - 1)

    # Evaluar bloques 3x3
    for m in range(3):
        for n in range(3):
            seen_block = {}
            for i in range(3 * m, 3 * (m + 1)):
                for j in range(3 * n, 3 * (n + 1)):
                    if cromosoma[i][j] in seen_block:
                        seen_block[cromosoma[i][j]] += 1
                    else:
                        seen_block[cromosoma[i][j]] = 1
            for key in seen_block:
                fitness -= (seen_block[key] - 1)

    return fitness


def cruzar(ch1, ch2):
    """Realiza el cruce entre dos cromosomas."""
    nuevo_hijo_1 = []
    nuevo_hijo_2 = []
    for i in range(9):
        x = random.randint(0, 1)
        if x == 1:
            nuevo_hijo_1.append(ch1[i])
            nuevo_hijo_2.append(ch2[i])
        elif x == 0:
            nuevo_hijo_2.append(ch1[i])
            nuevo_hijo_1.append(ch2[i])
    return nuevo_hijo_1, nuevo_hijo_2

def mutacion(ch, pm, initial):
    """Realiza la mutación en un cromosoma con cierta probabilidad."""
    for i in range(9):
        x = random.randint(0, 100)
        if x < pm * 100:
            ch[i] = generar_gen(initial[i])
    return ch

# Función para realizar la selección por ruleta
def roulette_wheel_selection(probabilities):
    cumulative_sum = np.cumsum(probabilities)
    random_number = np.random.rand()
    for i, cumulative_prob in enumerate(cumulative_sum):
        if random_number < cumulative_prob:
            return i
        
def obtener_piscina_mating(populacion):
    """Selecciona la piscina de apareamiento usando ruleta."""
    lista_aptitudes = []
    for cromosoma in populacion:
        aptitud = obtener_fitness(cromosoma)
        lista_aptitudes.append(aptitud)
    
    # Normalizar las aptitudes para convertirlas en probabilidades
    min_aptitud = min(lista_aptitudes)
    adjusted_fitness = [aptitud - min_aptitud + 1 for aptitud in lista_aptitudes]  # Ajustar para evitar valores negativos
    total_fitness = sum(adjusted_fitness)
    probabilities = [fit / total_fitness for fit in adjusted_fitness]
    
    piscina = []
    for _ in range(len(populacion)):
        idx = roulette_wheel_selection(probabilities)
        piscina.append(populacion[idx])
    return piscina

def obtener_descendencia(populacion, initial, pm, pc):
    """Obtiene la descendencia a partir de la población actual."""
    nueva_piscina = []
    i = 0
    while i < len(populacion):
        ch1 = populacion[i]
        ch2 = populacion[(i + 1) % len(populacion)]
        x = random.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = cruzar(ch1, ch2)
        nueva_piscina.append(mutacion(ch1, pm, initial))
        nueva_piscina.append(mutacion(ch2, pm, initial))
        i += 2
    return nueva_piscina

def imprimir_sudoku(solucion):
    """Imprime el Sudoku en un formato legible."""
    for fila in solucion:
        print(" ".join(map(str, fila)))

# Función principal del algoritmo genético para resolver Sudoku
def algoritmo_genetico(initial, POBLACION, REPETICION, PM, PC, callback=None):
    """Implementación del algoritmo genético para resolver Sudoku."""
    poblacion = generar_poblacion(POBLACION, initial)
    mejor_solucion = None
    mejor_aptitud = float('-inf')
    solucion_encontrada = False

    for iteracion in range(REPETICION):
        piscina_mating = obtener_piscina_mating(poblacion)
        random.shuffle(piscina_mating)
        poblacion = obtener_descendencia(piscina_mating, initial, PM, PC)
        aptitudes = [obtener_fitness(c) for c in poblacion]
        m = max(aptitudes)

        # Llamar a la función de callback con la iteración actual y la mejor solución encontrada
        if callback is not None:
            callback(iteracion + 1, poblacion[aptitudes.index(m)])

        # Actualizar la mejor solución si encontramos una con mejor aptitud
        if m > mejor_aptitud:
            mejor_aptitud = m
            mejor_solucion = [list(fila) for fila in poblacion[aptitudes.index(m)]]

        if m == 0:
            # Si encontramos una solución con aptitud 0, salir del bucle
            print("Solución encontrada en la iteración {}".format(iteracion + 1))
            solucion_encontrada = True
            break

    if solucion_encontrada:
        print("Mejor Solución (Aptitud: {}):".format(mejor_aptitud))
        imprimir_sudoku(mejor_solucion)
    else:
        print("No se encontró una solución.")

    return solucion_encontrada, mejor_solucion

