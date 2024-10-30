import matplotlib.pyplot as plt
import numpy as np

# Función que permite introducir el número de nodos explorados para cada heurística
def introducir_nodos_explorados():
    heuristicas = ['Trivial', 'Euclídea', 'Manhattan nA', 'Manhattan A', 'Octile', 'Chebyshev', 'Diagonal']
    resultados = {}

    for heuristica in heuristicas:
        nodos = int(input(f"Introduce el número de nodos explorados para la heurística {heuristica}: "))
        resultados[heuristica] = nodos

    return resultados

# Función para crear la gráfica
def crear_grafico(resultados, nombre_mapa):
    heuristicas = list(resultados.keys())
    
    # Datos para la gráfica
    nodos_explorados_por_heuristica = np.array([resultados[h] for h in heuristicas])
    indices = np.arange(len(heuristicas))
    bar_width = 0.4  # Ancho de las barras
    
    # Colores para cada barra
    colores = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink']
    
    # Crear gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(indices, nodos_explorados_por_heuristica, bar_width, color=colores)
    
    # Configuración del gráfico
    ax.set_xlabel('Heurísticas')
    ax.set_ylabel('Nodos Explorados')
    ax.set_title(f'Comparativa de Nodos Explorados por Heurística - {nombre_mapa}')
    ax.set_xticks(indices)
    ax.set_xticklabels(heuristicas, rotation=25, ha='right')  # Rotar las etiquetas y alinearlas a la derecha
    plt.subplots_adjust(bottom=0.2)  # Ajustar el margen inferior para evitar el solapamiento de etiquetas
    
    # Mostrar gráfica
    plt.show()

# Pedir el nombre del mapa
nombre_mapa = input("Introduce el nombre del mapa: ")

# Introducir los nodos explorados
resultados = introducir_nodos_explorados()

# Crear y mostrar la gráfica
crear_grafico(resultados, nombre_mapa)