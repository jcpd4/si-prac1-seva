class Casilla():
    def __init__(self, f, c):
        self.fila=f
        self.col=c
        
    def getFila (self):
        return self.fila
    
    def getCol (self):
        return self.col
    
    def __lt__(self, other):
    # Priorizar columnas primero para favorecer movimientos hacia la derecha
        if self.col == other.col:
            return self.fila < other.fila
        return self.col > other.col

        
