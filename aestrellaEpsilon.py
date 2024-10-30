from casilla import Casilla
from mapa import Mapa
from typing import List, Tuple
import math
import heapq

# Funciones heurísticas (se mantienen igual)
def heuristicaTrivial(nodoActual, destino):
    return 0

def heuristicaEuclidea(nodoActual, destino):
    return math.sqrt((destino.fila - nodoActual.fila) ** 2 + (destino.col - nodoActual.col) ** 2)

def heuristicaManhattanNoAdmisible(nodoActual, destino):
    return abs(destino.fila - nodoActual.fila) + abs(destino.col - nodoActual.col)

def heuristicaManhattanAdmisible(nodoActual, destino):
    dx = abs(destino.col - nodoActual.col)
    dy = abs(destino.fila - nodoActual.fila)
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

def heuristicaOctile(nodoActual, destino):
    delta_f = abs(destino.fila - nodoActual.fila)
    delta_c = abs(destino.col - nodoActual.col)
    return delta_f + (math.sqrt(2) - 1) * min(delta_f, delta_c)

def heuristicaChebyshev(nodoActual, destino):
    return max(abs(destino.fila - nodoActual.fila), abs(destino.col - nodoActual.col))

def heuristicaDiagonal(nodoActual, destino):
    dx = abs(destino.col - nodoActual.col)
    dy = abs(destino.fila - nodoActual.fila)
    return max(dx, dy) + (1.5 - 1) * min(dx, dy)

# El coste del movimiento
def mirarMov(movI, movJ, nodoActual):
    if abs(movI - nodoActual.fila) == 1 and abs(movJ - nodoActual.col) == 1:
        return 1.5  # movimiento diagonal
    else:
        return 1  # movimiento horizontal o vertical

# Función para seleccionar la heurística
def seleccionarHeuristica(tipoHeuristica, nodoActual, destino):
    if tipoHeuristica == 1:
        return heuristicaEuclidea(nodoActual, destino)
    elif tipoHeuristica == 2:
        return heuristicaManhattanNoAdmisible(nodoActual, destino)
    elif tipoHeuristica == 3:
        return heuristicaManhattanAdmisible(nodoActual, destino)
    elif tipoHeuristica == 4:
        return heuristicaOctile(nodoActual, destino)
    elif tipoHeuristica == 5:
        return heuristicaChebyshev(nodoActual, destino)
    elif tipoHeuristica == 6:
        return heuristicaDiagonal(nodoActual, destino)
    elif tipoHeuristica == 0:
        return heuristicaTrivial(nodoActual, destino)
    else:
        raise ValueError("Tipo de heurística no válido. Seleccione una opción válida.")

# Función que determina el coste en calorías según el tipo de celda
def caloriasPorCelda(celda):
    if celda == 0:  # Hierba
        return 2
    elif celda == 4:  # Agua
        return 4
    elif celda == 5:  # Roca
        return 6
    else:
        return 0  # Otras celdas o muro
    

def a_aestrella_epsilon(mapa, origen, destino, tipoHeuristica, epsilon):
    listaFrontera: List[Tuple[float, float, Casilla]] = []
    heapq.heapify(listaFrontera)
    
    # Inicializar listas bidimensionales con valores por defecto
    costeAcumulado = [[math.inf for _ in range(mapa.ancho)] for _ in range(mapa.alto)]
    costeAcumulado[origen.fila][origen.col] = 0

    caloriasAcumuladas = [[math.inf for _ in range(mapa.ancho)] for _ in range(mapa.alto)]
    caloriasAcumuladas[origen.fila][origen.col] = 0

    nodoPadre = [[None for _ in range(mapa.ancho)] for _ in range(mapa.alto)]

    # Insertar el nodo de origen en la frontera correctamente
    h_origen = seleccionarHeuristica(tipoHeuristica, origen, destino)
    f_origen = 0 + h_origen  # f(n) = g(n) + h(n)
    heapq.heappush(listaFrontera, (f_origen, 0, origen))  # (f, calorias, nodo)
    print(f"Nodo de origen insertado: ({origen.fila}, {origen.col}) con f={f_origen}")

    nodosExplorados = 0
    traza = [f"- Mapa: {mapa.nombre if hasattr(mapa, 'nombre') else 'No especificado'}; origen en ({origen.fila},{origen.col}); destino en ({destino.fila},{destino.col}); heurística: {['Trivial', 'Euclídea', 'Manhattan nA', 'Manhattan A', 'Octile', 'Chebyshev', 'Diagonal'][tipoHeuristica]}"]
    traza.append("- Lista interior: []")
    traza.append(f"- Lista frontera: [({origen.fila},{origen.col})]")

    while listaFrontera:
        # Obtener el f_min actual
        f_min = listaFrontera[0][0]
        print(f"f_min actual: {f_min}")

        # Crear lista focal
        listaFocal = [nodo for nodo in listaFrontera if nodo[0] <= f_min * (1 + epsilon)]
        print(f"Tamaño de lista focal: {len(listaFocal)}")

        if not listaFocal:
            print("Lista focal vacía, terminando búsqueda")
            break

        # Seleccionar el nodo con el menor valor de calorías dentro de la lista focal
        nodoSeleccionado = min(listaFocal, key=lambda nodo: nodo[1])  # (f, calorias, nodo)
        print(f"Nodo seleccionado de la lista focal: {nodoSeleccionado}")

        # Remover el nodo seleccionado de la frontera
        listaFrontera.remove(nodoSeleccionado)
        heapq.heapify(listaFrontera)  # Re-heapify después de la eliminación
        f, calorias, nodoActual = nodoSeleccionado
        nodosExplorados += 1

        # Verificar si es el destino
        if nodoActual.fila == destino.fila and nodoActual.col == destino.col:
            print("Destino alcanzado, reconstruyendo camino")
            camino = []
            sumaCalorias = caloriasAcumuladas[nodoActual.fila][nodoActual.col]
            fila, col = nodoActual.fila, nodoActual.col
            while fila is not None and col is not None:
                camino.append((fila, col))
                padre = nodoPadre[fila][col]
                if padre is not None:
                    fila, col = padre
                else:
                    print(f"({fila}, {col}) no tiene padre, terminando reconstrucción")
                    fila, col = None, None
            camino.reverse()
            print(f"Camino encontrado: {camino}")
            return costeAcumulado[destino.fila][destino.col], camino, sumaCalorias, traza, nodosExplorados

        # Explorar vecinos
        for movI, movJ in movimientosPosibles(mapa, nodoActual):
            costeMov = mirarMov(movI, movJ, nodoActual)
            tipoCelda = mapa.getCelda(movI, movJ)
            caloriasMov = caloriasPorCelda(tipoCelda)
            h = seleccionarHeuristica(tipoHeuristica, Casilla(movI, movJ), destino)
            nuevoCoste = costeAcumulado[nodoActual.fila][nodoActual.col] + costeMov
            nuevasCalorias = caloriasAcumuladas[nodoActual.fila][nodoActual.col] + caloriasMov
            print(f"  Nuevas calorias: {nuevasCalorias}")
            # Definir f(n) como la suma de coste acumulado y la heurística
            f = nuevoCoste + h

            # Condición de actualización mejorada
            if (nuevoCoste < costeAcumulado[movI][movJ]) or \
               (nuevoCoste == costeAcumulado[movI][movJ] and nuevasCalorias < caloriasAcumuladas[movI][movJ]):
                costeAcumulado[movI][movJ] = nuevoCoste
                caloriasAcumuladas[movI][movJ] = nuevasCalorias
                nuevaCasilla = Casilla(movI, movJ)
                heapq.heappush(listaFrontera, (f, nuevasCalorias, nuevaCasilla))
                nodoPadre[movI][movJ] = (nodoActual.fila, nodoActual.col)

    print("No se encontró un camino válido")
    traza.append("- No se ha cambiado camino al destino.")
    return -1, [], 0, traza, nodosExplorados

def movimientosPosibles(mapa, posActual):
    # Los 8 movimientos posibles
    movimientos = [(0, 1),
                   (1, 1),
                   (1, 0),
                   (1, -1),
                   (0, -1),
                   (-1, -1),
                   (-1, 0),
                   (-1, 1)]                   
    # Tamaño mapa
    filas = mapa.alto
    columnas = mapa.ancho
    #vector que almacena las celdas a las que se puede acceder
    celdasValidas = []
    #La posicion del conejo
    i = posActual.fila
    j = posActual.col
    
    #Comprobamos los 8 movimientos
    for movimiento in movimientos:
        movI = i + movimiento[0]
        movJ = j + movimiento[1]
        
        # Comprobamos que no nos hemos salido del mapa
        if movI >= 0 and movI < filas and movJ >= 0 and movJ < columnas:
            # Obtenemos el valor de la celda
            celdaVisitada = mapa.getCelda(movI, movJ)
            
            # Verificamos si la celda es transitable
            if celdaVisitada != 1:
                celdasValidas.append((movI, movJ))
    
    return celdasValidas
