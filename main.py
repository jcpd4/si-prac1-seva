import sys, pygame
from casilla import *
from mapa import *
from pygame.locals import *
from aestrella import *
from aestrellaEpsilon import *
from aepsilon import *


MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(250, 180, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(255, 255, 0) 

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino o como origen
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapi, posicion):
    res=-1
    
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+95 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+145 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=3

    
    return res
   
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

# Función para imprimir la traza (puede ser útil para depuración)
def imprimirTraza(traza):
    for linea in traza:
        print(linea)
# función principal
def main():
    pygame.init()    
    tipoHeuristica = 0
    nodosExplorados = 0
    epsilon = 1
    contenidoHeuristica = 'h = 0'
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa.txt'
    else:
        file=sys.argv[-1]
         
    mapi=Mapa(file)     
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])
    
    boton3=pygame.image.load("boton3.png").convert()
    boton3=pygame.transform.scale(boton3,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()      
                if pulsaBoton(mapi, pos)==1 or pulsaBoton(mapi, pos)==2:
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        print('Error: No hay origen o destino')
                    else:
                        camino=inic(mapi)
                        if pulsaBoton(mapi, pos)==1:
                            ###########################                                                 
                            #coste, cal=llamar a A estrella
                            coste, vCamino, cal, traza, nodosExplorados = a_aestrella(mapi, origen, destino, tipoHeuristica)
                            imprimirTraza(traza)
                            print(f"Nodos explorados: {nodosExplorados} ")
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            else:
                                
                                #print(f"Coste del camino: {coste}")
                                #for paso in vCamino:
                                #   print(f"Celda: Fila {paso[0]}, Columna {paso[1]}")
                                
                                for (fila, col) in vCamino:
                                    camino[fila][col] = '+'   
                        elif pulsaBoton(mapi, pos) == 2:
                            ###########################                                                   
                            #coste, cal=llamar a A estrella subepsilon
                            print("Inicializando estructuras de datos")

                            coste, vCamino, cal, traza, nodosExplorados = a_aestrella_epsilon(mapi, origen, destino, tipoHeuristica, epsilon)
                            imprimirTraza(traza)
                            print(f"Nodos explorados: {nodosExplorados} ")
                            
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            else:
                                for (fila, col) in vCamino:
                                    camino[fila][col] = '+'
                elif pulsaBoton(mapi, pos) == 3:
                    print(tipoHeuristica)
                    tipoHeuristica +=1
                    if(tipoHeuristica == 1):
                        contenidoHeuristica = "Euclídea"
                    elif(tipoHeuristica == 2):
                        contenidoHeuristica = "Manhattan nA"
                    elif(tipoHeuristica == 3):
                        contenidoHeuristica = "Manhattan A"
                    elif(tipoHeuristica == 4):
                        contenidoHeuristica = "Octile"
                    elif(tipoHeuristica == 5):
                        contenidoHeuristica = "Chebyshev"
                    elif(tipoHeuristica == 6):
                        contenidoHeuristica = "Diagonal"
                    elif tipoHeuristica > 6:
                        tipoHeuristica = 0
                        contenidoHeuristica = "h = 0"
                        
                            
                elif esMapa(mapi,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)                        
                        if bueno(mapi, casO):
                            origen=casO
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapi, casD):
                            destino=casD
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):                
                if camino[fil][col]!='.':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton3, [anchoVentana//2+95, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 22)
            textoCoste=fuente.render("Coste: "+str(coste), True, AMARILLO)            
            screen.blit(textoCoste, [anchoVentana-90, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render("Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoHeuristica=fuente.render("Tipo Heurística: "+contenidoHeuristica, True, AMARILLO)
            screen.blit(textoHeuristica, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+40])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
