import unittest
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,calcular_adyacentes,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True

def es_matriz(m:list[list[int]]) -> bool:
    for i in range(0, len(m)-1):
        if len(m[i]) != len(m[i+1]):return False
    return True


class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        self.assertTrue(es_matriz(tablero))
        self.assertTrue(dimension_correcta(tablero, filas, columnas))

def todas_adyacentes_en_el_tablero(posiciones, filas, columnas):
    for pos in posiciones:
        if pos[0]>filas or pos[0]<0:return False 
        if pos[1]>columnas or pos[1]<0: return False
    return True

def todas_las_esperadas(posiciones, esperadas):
    for pos in posiciones:
        if pos not in esperadas: return False
    return True

class calcular_adyacentesTest(unittest.TestCase):
    def test_adyacentes_centro(self):
        filas= 3
        columnas= 3
        posicion= (1,1)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas=[(0,0), (0,1), (0,2), (1,0), (1,2), (2, 0), (2,1), (2,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes) #Testea que no se cuente a si mismo como adyacente
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))
    
    def test_adyacentes_borde_1(self):
        filas=3
        columnas=3
        posicion= (0,0)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(1,0),(0,1),(1,1)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_2(self):
        filas=3
        columnas=3
        posicion= (1,0)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(0,0),(0,1),(1,1),(2,1),(2,0)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_3(self):
        filas=3
        columnas=3
        posicion= (2,0)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(1,0),(1,1),(2,1)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_4(self):
        filas=3
        columnas=3
        posicion= (0,1)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(0,0),(1,0),(1,1),(1,2),(0,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_5(self):
        filas=3
        columnas=3
        posicion= (0,2)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(0,1),(1,1),(1,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_6(self):
        filas=3
        columnas=3
        posicion= (1,2)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(0,2),(0,1),(1,1),(2,1),(2,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_7(self):
        filas=3
        columnas=3
        posicion= (2,1)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(2,0),(1,0),(1,1),(1,2),(2,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

    def test_adyacentes_borde_8(self):
        filas=3
        columnas=3
        posicion= (2,2)

        adyacentes=calcular_adyacentes(posicion, (filas, columnas))
        adyacentes_esperadas = [(2,1),(1,1),(1,2)]
        self.assertTrue(todas_adyacentes_en_el_tablero(adyacentes, filas, columnas))
        self.assertFalse((filas, columnas) in adyacentes)
        self.assertTrue(todas_las_esperadas(adyacentes, adyacentes_esperadas))

class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])


class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)



class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])


class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 3,
            'tablero': [
                [-1, -1],
                [ -1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, -1],
            [ -1, 1]
        ])

# Tarea: Pensar cómo testear  guardar_estado y cargar_estado

class guardar_estadoTest(unittest.TestCase):
    def setUp(self):
        self.estado_base: EstadoJuego = {
        'filas': 4,
        'columnas': 4,
        'minas': 2,
        'tablero': [
            [-1, 2, 1, 0],
            [2, -1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0]
        ],
        'tablero_visible': [
            [' ', ' ', '1', '0'],
            [' ', '🚩', '1', '0'],
            ['1', '1', '1', '0'],
            ['0', '0', '0', '0']
        ],
        'juego_terminado': False
    }

    def test_guardar_estado (self):
        ruta_archivo = './tableros_testing/guardar_estados'
        estado = self.estado_base
        guardar_estado(estado, ruta_archivo)
        self.assertTrue(cargar_estado(estado, ruta_archivo))
        return

class cargar_estadoTest(unittest.TestCase):
    def setUp(self):
        self.estado_base: EstadoJuego = {
        'filas': 4,
        'columnas': 4,
        'minas': 2,
        'tablero': [
            [-1, 2, 1, 0],
            [2, -1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0]
        ],
        'tablero_visible': [
            [' ', ' ', '1', '0'],
            [' ', '🚩', '1', '0'],
            ['1', '1', '1', '0'],
            ['0', '0', '0', '0']
        ],
        'juego_terminado': False
    }

    def test_comas_duplicadas(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_comas_duplicadas'
        self.assertFalse(cargar_estado(estado, ruta_archivo))

    def test_comas_duplicadas_tablero_visible(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_comas_duplicadas_visible'
        self.assertFalse(cargar_estado(estado, ruta_archivo))

    def test_tablero_valores_invalidos(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_valores_invalidos'
        self.assertFalse(cargar_estado(estado, ruta_archivo))

    def test_tablero_sin_minas(self):
        estado = self.estado_base
        ruta_archivo =  './tableros_testing/caso_sin_minas'
        self.assertFalse(cargar_estado(estado, ruta_archivo))

    def test_tablero_visible_no_coincide(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_visible_no_coincide'
        self.assertFalse(cargar_estado(estado, ruta_archivo))
    
    def test_fila_coma_al_final(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_fila_coma_al_final'
        self.assertFalse(cargar_estado(estado, ruta_archivo))
    
    def test_fila_coma_al_principio(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_fila_coma_al_principio'
        self.assertFalse(cargar_estado(estado, ruta_archivo))
    
    def test_visible_no_numerico(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_visible_no_numerico'
        self.assertFalse(cargar_estado(estado, ruta_archivo))

    def test_caso_valido(self):
        estado = self.estado_base
        ruta_archivo = './tableros_testing/caso_valido'
        self.assertTrue(cargar_estado(estado, ruta_archivo))


"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

if __name__ == '__main__':
    unittest.main(verbosity=2)
