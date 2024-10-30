from casilla import Casilla
from mapa import Mapa
from heapq import heappush, heappop
from typing import List, Tuple, Dict
import math

# Funciones heurísticas
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

#El coste del movimiento
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


def a_aestrella(mapa, origen, destino, tipoHeuristica):
    #-----Definicion de las variables-----
    listaFrontera: List[Tuple[float, float, Casilla]] = []  # Anotación de tipo
    #                     f(n), costeAcumulado, nodo
    heappush(listaFrontera, (0, 0, origen))
    #Diccionario para almacenar el coste acumulado
    #inicialmente 0
    costeAcumulado: Dict[Tuple[int, int], float] = { (origen.fila, origen.col): 0 }
    #Diccionario para almacenar el nodo padre de cada nodo
    nodoPadre = { (origen.fila, origen.col): None }
    #Diccionario para almacenar las calorías acumuladas
    caloriasAcumuladas = {(origen.fila, origen.col): 0}
    #contador de nodos
    nodosExplorados = 0
    traza = [f"- Mapa: {mapa.nombre if hasattr(mapa, 'nombre') else 'No especificado'}; origen en ({origen.fila},{origen.col}); destino en ({destino.fila},{destino.col}); distancia {['Trivial', 'Euclídea', 'Manhattan nA', 'Manhattan A', 'Octile', 'Chebyshev', 'Diagonal'][tipoHeuristica]}"]
    traza.append("- Lista interior: []")
    traza.append(f"- Lista frontera: [({origen.fila},{origen.col})]")
    #-------------------------------------
    
    #El pseudocódigo
    while listaFrontera:
        # Obtener nodo de la listaFrontera con menor coste g
        # costeActual = menor coste g acumulado, nodoActual = pos del nodo con el menor coste g acumulado 
        f, costeActual, nodoActual = heappop(listaFrontera)
        nodosExplorados +=1
        traza.append(f"- Cogemos nodo frontera con menor f: n=({nodoActual.fila},{nodoActual.col}), g={costeActual:.2f}, h={f-costeActual:.2f}.")
        
        
        
        #si n es meta -> reconstruir el camino
        if nodoActual.fila == destino.fila and nodoActual.col == destino.col:
            traza.append("- Hemos llegado al destino. Reconstruyendo camino...")
            camino = []
            sumaCalorias = caloriasAcumuladas[(nodoActual.fila, nodoActual.col)]
            while nodoActual is not None:
                camino.append((nodoActual.fila, nodoActual.col))
                nodoActual = nodoPadre[(nodoActual.fila, nodoActual.col)]
            traza.append(f"- Camino encontrado: {camino[::-1]}")
            traza.append(f"- Coste total: {costeAcumulado[(destino.fila, destino.col)]:.2f}")
            traza.append(f"- Calorías totales: {sumaCalorias:.2f}")
            return costeAcumulado[(destino.fila, destino.col)], camino, sumaCalorias, traza, nodosExplorados
        
        traza.append(f"- Sacamos n de lista frontera y la metemos en lista interior.")
        traza.append("- Revisamos movimientos válidos desde n que no estén en lista interior:")
        
        #movimientosPosbibles devuelve una lista de tuplas (coordenadas de las celdas vecinas)
        for movI, movJ in movimientosPosibles(mapa, nodoActual):
            
            costeMov = mirarMov(movI, movJ, nodoActual) #Comprobar el tipo de movimiento
            tipoCelda = mapa.getCelda(movI, movJ) # Obtener el tipo de celda y calcular las calorías 
            caloriasMov = caloriasPorCelda(tipoCelda) # Calorías gastadas al moverse a esa celda.
            h = seleccionarHeuristica(tipoHeuristica, Casilla(movI, movJ), destino) # Calcular heurística según la elección del usuario
            #nuevo coste y calorias gastadas para el nodoVecino 
            nuevoCoste = costeAcumulado[(nodoActual.fila, nodoActual.col)] + costeMov
            nuevasCalorias = caloriasAcumuladas[(nodoActual.fila, nodoActual.col)] + caloriasMov
            
            
            #Comprobar si ha sido explorado o si el nuevoCoste es mejor
            if (movI, movJ) not in costeAcumulado or nuevoCoste < costeAcumulado[(movI, movJ)]:
                costeAcumulado[(movI, movJ)] = nuevoCoste
                caloriasAcumuladas[(movI, movJ)] = nuevasCalorias 
                f = nuevoCoste + h
                heappush(listaFrontera, (f, nuevoCoste, Casilla(movI, movJ))) #La pila va elegir la menor h para explorar los nodos
                nodoPadre[(movI, movJ)] = nodoActual
                
                traza.append(f"  -- ({movI},{movJ}): g={nuevoCoste:.2f}, h={h:.2f} -> nuevo nodo en lista frontera")
            else:
                traza.append(f"  -- ({movI},{movJ}): nodo que ya estaba en lista frontera, pero el nuevo g ({nuevoCoste:.2f}) es peor que el que había ({costeAcumulado[(movI, movJ)]:.2f}) por lo que no lo cambiamos")
    
    traza.append("- No se ha cambiado camino al destino.")
    return -1, [], 0, traza, nodosExplorados #devolver error, si no encuentro el camino

        
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
            
    
    