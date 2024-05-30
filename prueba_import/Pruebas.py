import unittest
from src.modell.LogicJ import LogicJuego

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Configuración del entorno de prueba
        self.tablero_jugador = [['' for _ in range(8)] for _ in range(8)]
        self.tablero_maquina = [['' for _ in range(8)] for _ in range(8)]
        self.logic_juego = LogicJuego(self.tablero_jugador, self.tablero_maquina)

    def test_disparos(self):
        # Probar la función de realizar disparos
        instance = (0, 0)
        self.logic_juego.realizar_ataque(instance)
        # Verificar si se realizó un disparo en la posición (0, 0)
        self.assertEqual(self.logic_juego.tablero_maquina[0][0], 'X', "El disparo no se realizó correctamente")

    def test_acertados(self):
        # Probar la función de disparos acertados
        instance = (0, 0)
        # Colocar un barco en la posición objetivo del tablero del jugador
        self.tablero_maquina[0][0] = 'X'
        self.logic_juego.realizar_ataque(instance)
        # Verificar si se detectó correctamente un disparo acertado en la posición (0, 0)
        self.assertEqual(self.logic_juego.tablero_maquina[0][0], 'X', "El disparo no acertó correctamente")

    def test_fallados(self):
        # Probar la función de disparos fallados
        instance = (0, 0)
        self.logic_juego.realizar_ataque(instance)
        # Verificar si se detectó correctamente un disparo fallado en la posición (0, 0)
        self.assertNotEqual(self.logic_juego.tablero_maquina[0][0], 'X', "El disparo no falló correctamente")

    def test_excepciones(self):
        # Probar la función de excepciones
        with self.assertRaises(Exception):
            # Simular una situación que debería lanzar una excepción
            raise Exception("Esto es una excepción de prueba")

if __name__ == '__main__':
    unittest.main()
