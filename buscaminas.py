#%%
import random
from typing import Any
import os

# Constantes para dibujar
BOMBA =  chr(128163)  # simbolo de una mina
BANDERA =  chr(128681)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def colocar_minas(filas: int, columnas: int, minas: int) -> list[list[int]]:
    """Elige posiciones aleatorias y crea un tablero con minas en esas posiciones"""
    posiciones:list[tuple[int, int]] = [] # Todas las posiciones que va a tener el tablero
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i,j))

    minas_pos:list[tuple[int, int]] = random.sample(posiciones, minas) # Elige 3 posiciones random y las guarda en una lista de tuplas
    res: list[list[int]]= [[0 for _ in range(columnas)] for _ in range(filas)] #Crea el tablero iniciando todo en 0
    for i, j in minas_pos:  # Recorre las posiciones en las que van las minas
        res[i][j] = -1  # Pone una mina en la posicion
    return res

def calcular_numeros(tablero: list[list[int]]) -> None: 
    """Calcula los numeros que van a estar en cada posicion, los cuales indican cuantas minas adyacentes tiene"""
    dimensiones:tuple[int, int]=(len(tablero), len(tablero[0])) # Para evitar adyacentes no validas
    adyacentes: list[tuple[int,int]]=[] # Esta lista va a tener todas las posiciones que sean adyacentes a una mina
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if tablero[f][c]== -1: adyacentes+=(calcular_adyacentes((f,c), dimensiones)) # Cuando encuentra una mina en una posicion, agrega las posiciones adyacentes
    for pos in adyacentes:
        if tablero[pos[0]][pos[1]]!=-1: # Evita cambiar minas por numeros
            tablero[pos[0]][pos[1]]+=1  # Cada vez que esa posicion aparecio como adyacente a una mina

def calcular_adyacentes (pos:tuple[int, int], dimensiones:tuple[int, int]) -> list[tuple[int, int]]:
    """Calcula las posiciones adyacentes a una posicion (x,y) dentro de un tablero de dimensiones (filas, columnas), argumentos que se toman para evitar adyacentes fuera del tablero"""
    adyacentes: list[tuple[int,int]]=[]
    for i in range(-1, 2): # Las posiciones adyacentes a (x,y) se calculan sumando -1, 0 ó 1 a x
        for j in range(-1, 2): # Las posiciones adyacentes a (x,y) se calculan sumando -1, 0 ó 1 a y
            x: int=pos[0]+i
            y: int=pos[1]+j
            if ((i,j)!=(0,0) # Evita que (x,y) quede como adyacente a si misma
                and x>=0 and y>=0 and x<dimensiones[0] and y<dimensiones[1]): # Evita que las adyacentes esten fuera del tablero
                adyacentes.append((x,y))
    return adyacentes

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    res:EstadoJuego={
        'filas': filas,
        'columnas': columnas,
        'minas': minas,
        'tablero': colocar_minas(filas, columnas, minas),
        'tablero_visible': [[VACIO for _ in range(columnas)] for _ in range(filas)], 
        'juego_terminado': False,
    }
    calcular_numeros(res['tablero'])  # Calcula los numeros del tablero
    return res

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """Devuelve una copia del tablero visible del estado del juego"""
    tablero_visible = estado['tablero_visible']
    res: list[list[str]]=[]
    for f in range(len(tablero_visible)): # Recorre cada fila del tablero visible
        fila: list[int]=[] # Inicializa lo que va a ser una copia de esa fila
        for c in range(len(tablero_visible[f])): # Por cada elemento de esa fila que se esta recorriendo
            fila.append(tablero_visible[f][c])  # Lo añade a la copia de la fila
        res.append(fila)    # Agrega la copia de la fila a la copia del tablero y sigue con la siguiente fila
    return res

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    posicion:str = estado['tablero_visible'][fila][columna] # Lee lo que hay en la posicion ingresada del tablero
    if estado['juego_terminado']: return    # Si el juego esta terminado, no deja que se modifica nada
    if posicion==VACIO:estado['tablero_visible'][fila][columna]=BANDERA # Si la posicion estaba tapada, la "marca" con bandera
    elif posicion==BANDERA:estado['tablero_visible'][fila][columna]=VACIO # Si la posicion tenia una bandera, la "desmarca"
    # No es necesario poner un caso en el que la posición no es ni vacio ni bandera

def descubrir_bombas(tablero:list[list[int]], estado:EstadoJuego) -> None: 
    for f in range(len(tablero)):
            for c in range(len(tablero)): # Recorre el tablero y
                if tablero[f][c]==-1: estado['tablero_visible'][f][c]=BOMBA # Donde encuentra una bomba cambia el visible

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    posicion:int = estado['tablero'][fila][columna] # Guarda lo que hay en la posicion ingresada
    tablero:list[list[int]]=estado['tablero']

    if posicion==-1: # Si se ingreso una bomba
        estado['juego_terminado']=True # Se termina el juego
        descubrir_bombas(tablero, estado) # Se muestran todas las bombas que habia

    elif posicion != -1: # Si la posición no es una bomba
        estado['tablero_visible'][fila][columna] = str(posicion) # Se muestra lo que hay "debajo"
        if posicion == 0: estado['tablero_visible'] = descubrir_ceros(tablero, estado['tablero_visible'], fila, columna)
        estado['juego_terminado'] = todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible'])

def todas_celdas_seguras_descubiertas(tablero:list[list[int]], tablero_visible:list[list[str]]) -> bool:
    for f in range(len(tablero)):
        for c in range(len(tablero[f])):
            if (tablero[f][c]==-1 and not(tablero_visible[f][c]==VACIO or tablero_visible[f][c]==BANDERA)): return False
            elif (tablero[f][c]!=-1 and tablero_visible[f][c]!=str(tablero[f][c])): return False
    return True

def descubrir_ceros(tablero:list[list[int]], visible:list[list[str]], f:int, c:int) -> list[list[str]]:
    adyacentes:list[tuple[int, int]] = calcular_adyacentes((f, c), (len(tablero), len(tablero[0])))
    for pos in adyacentes:
        if tablero[pos[0]][pos[1]]==0 and visible[pos[0]][pos[1]]==VACIO:
            visible[pos[0]][pos[1]]='0'
            descubrir_ceros(tablero, visible, pos[0], pos[1])
        elif tablero[pos[0]][pos[1]]!=-1 and visible[pos[0]][pos[1]]==VACIO:
            visible[pos[0]][pos[1]]=str(tablero[pos[0]][pos[1]])
    return visible

def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible'])


def reiniciar_juego(estado: EstadoJuego) -> None:
    filas = estado['filas']
    columnas = estado['columnas']
    minas = estado['minas']

    nuevo = crear_juego(filas, columnas, minas)
    while(nuevo['tablero'] == estado['tablero']):nuevo=crear_juego(filas, columnas, minas)
    estado.clear()
    estado['filas'] = nuevo['filas']
    estado['columnas'] = nuevo['columnas']
    estado['minas'] = nuevo['minas']
    estado['tablero'] = nuevo['tablero']
    estado['tablero_visible'] = nuevo['tablero_visible']
    estado['juego_terminado'] = nuevo['juego_terminado']


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    ruta_tablero: str = os.path.join(ruta_directorio, 'tablero.txt')
    ruta_visible: str = os.path.join(ruta_directorio, 'tablero_visible.txt')
    tablero: list[list[int]] = estado['tablero']
    visible: list[list[str]] = estado['tablero_visible']
    
    archivo = open(ruta_tablero, 'w')
    f: int
    i: int
    for f in range(len(tablero)):
        fila = tablero[f]
        for i in range(len(fila)):
            archivo.write(str(fila[i]))
            if i < len(fila) - 1:
                archivo.write(',')
        if f < len(tablero) - 1:
            archivo.write('\n')
    archivo.close()

    archivo = open(ruta_visible, 'w')
    for f in range(len(visible)):
        fila = visible[f]
        for i in range(len(fila)):
            if fila[i] == BANDERA:
                archivo.write('*')
            elif fila[i] == VACIO:
                archivo.write('?')
            else:
                archivo.write(fila[i])
            if i < len(fila) - 1:
                archivo.write(',')
        if f < len(visible) - 1:
            archivo.write('\n')
    archivo.close()


#%%
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    if not (existe_archivo(ruta_directorio, 'tablero.txt') and
            existe_archivo(ruta_directorio, 'tablero_visible.txt')): return False    

    archivo = open(os.path.join(ruta_directorio, "tablero.txt"), 'r')
    tablero_cargado: list[str] = eliminar_lineas_vacias(archivo.readlines())
    archivo.close()

    archivo = open(os.path.join(ruta_directorio, "tablero_visible.txt"), 'r')
    visible_cargado: list[str] = eliminar_lineas_vacias(archivo.readlines())
    archivo.close()

    columnas_esperadas:int = estado['columnas']

    if not validar_columnas(tablero_cargado, columnas_esperadas): return False
    if not validar_columnas(visible_cargado, columnas_esperadas): return False

    if not filas_validas(tablero_cargado):return False
    if not filas_validas(visible_cargado):return False

    tablero_int: list[list[int]] = pasar_a_tablero(tablero_cargado)

    if not adyacentes_validas(tablero_int): return False

    if contar_minas(tablero_int) <= 0: return False

    visible_terminado: list[list[str]] = pasar_a_tablero_visible(visible_cargado)

    if not visibles_validas(visible_terminado, tablero_int): return False

    estado['tablero'] = tablero_int
    estado['tablero_visible'] = visible_terminado
    estado['minas'] = contar_minas(tablero_int)
    estado['filas'] = len(tablero_int)
    estado['columnas'] = len(tablero_int[0])
    estado['juego_terminado'] = False
    return True

def validar_columnas(lista:list[str], cantidad:int)->bool:
    for elem in lista:
        if len(separar_por_caracter(elem, ','))!=cantidad:return False
    return True


def eliminar_lineas_vacias(l:list[str])->list[str]:
    res:list[str]=[]
    for elem in l:
        if len(elem)==0 or elem=='\n':continue
        borrar_ultimo_salto:str=''
        for c in elem:
            if c!='\n':
                borrar_ultimo_salto=borrar_ultimo_salto+c
        res.append(borrar_ultimo_salto)
    return res

def filas_validas(lista: list[str]) -> bool:
    for linea in lista:
        i: int = 0
        anterior_coma: bool = False
        while i < len(linea):
            c: str = linea[i]
            if c == ',':
                if anterior_coma:
                    return False  # dos comas seguidas
                anterior_coma = True
            else:
                anterior_coma = False
            i += 1
    return True

def pasar_a_tablero(lineas: list[str]) -> list[list[int]]:
    res: list[list[int]] = []
    for linea in lineas:
        fila: list[int] = []
        actual: str = ''
        i: int = 0
        while i < len(linea):
            c: str = linea[i]
            if c == ',':
                fila.append(int(actual))
                actual = ''
            else:
                actual = actual + c
            i += 1
        fila.append(int(actual))  # último valor
        res.append(fila)
    return res

def adyacentes_validas(matriz: list[list[int]]) -> bool:
    for fila in matriz:
        for valor in fila:
            if valor < -1 or valor > 8:
                return False
    return True

def contar_minas(tabero: list[list[int]]) -> int:
    contador: int= 0
    for fila in tabero:
        for celda in fila:
            if celda == -1:  # Si la celda es una mina
                contador += 1
    return contador

def pasar_a_tablero_visible(l: list[str]) -> list[list[str]]:
    res: list[list[str]] = []
    for fila in l:
        fila_resultado: list[str] = []
        valores: list[str] = separar_por_caracter(fila, ',')
        for char in valores:
            if char == '*':
                fila_resultado.append(BANDERA)
            elif char == '?':
                fila_resultado.append(VACIO)
            else:
                fila_resultado.append(char)
        res.append(fila_resultado)
    return res

def separar_por_caracter(cadena: str, caracter: str) -> list[str]:
    resultado: list[str]= []
    actual: str= ""
    for c in cadena:
        if c == caracter:
            resultado.append(actual)
            actual = ""
        else:
            actual += c
    resultado.append(actual)
    return resultado

def visibles_validas(visible: list[list[str]], tablero: list[list[int]]) -> bool:
    filas: int = len(visible)
    columnas: int = len(visible[0])
    for i in range(filas):
        for j in range(columnas):
            celda = visible[i][j]
            if celda not in [VACIO, BANDERA]:
                if not es_numero(celda):
                    return False
                if int(celda) != tablero[i][j]:
                    return False
    return True

def es_numero(cadena: str) -> bool:
    for c in cadena:
        if c < '0' or c > '9':
            return False
    return True


# %%
#   __
# <(o )___
#  ( ._> /
#   `---'   zZz
#