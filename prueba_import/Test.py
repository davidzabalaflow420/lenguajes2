#Estos son Test que yo personalmente debía hacer así que no los voy a quitar.

from unittest import TestCase, mock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import unittest
from unittest.mock import patch, MagicMock
from src.view.Menu import LogicIA, LogicJugador, MenuScreen
from src.view.Tablero import TableroJugador, TableroMaquina
from src.modell.LogicJ import LogicJuego
from src.controller.BD import BD

class TestLogicJugador(unittest.TestCase):
    """
    Pruebas unitarias para la clase LogicJugador.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.tablero_maquina = TableroMaquina()
        self.tablero_jugador = TableroJugador()
        self.logic_jugador = LogicJugador(self.tablero_jugador, self.tablero_maquina)

    def test_colocar_barco_jugador(self):
        """
        Prueba la colocación de barcos por parte del jugador.
        """
        for btn in self.tablero_jugador.buttons[:10]:
            self.logic_jugador.colocar_barco_jugador(btn)
        self.assertEqual(len(self.logic_jugador.barcos_jugador), 10)

    @patch('random.random', return_value=0.1)
    def test_realizar_ataque_jugador(self, mock_random):
        """
        Prueba que se realiza un ataque de manera adecuada.
        """
        self.logic_jugador.realizar_ataque_jugador(self.tablero_maquina.buttons[0])
        self.assertTrue(self.tablero_maquina.buttons[0].text in ['X', '-'])

class TestMenuScreen(unittest.TestCase):
    """
    Pruebas unitarias para la clase MenuScreen.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.menu_screen = MenuScreen()

    def test_initialization(self):
        """
        Prueba que los widgets se inicializan correctamente.
        """
        self.assertIsInstance(self.menu_screen.btn_jugar, Button)
        self.assertIsInstance(self.menu_screen.btn_nosotros, Button)
        self.assertIsInstance(self.menu_screen.btn_salir, Button)
        self.assertIsInstance(self.menu_screen.chess_layout, BoxLayout)
        self.assertIsInstance(self.menu_screen.tablero_jugador, TableroJugador)
        self.assertIsInstance(self.menu_screen.tablero_maquina, TableroMaquina)

class TestLogicIA(unittest.TestCase):
    """
    Pruebas unitarias para la clase LogicIA.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.tablero_maquina = TableroMaquina()
        self.tablero_jugador = TableroJugador()
        self.logic_ia = LogicIA(self.tablero_maquina, self.tablero_jugador)

    def test_colocar_barcos_maquina(self):
        """
        Prueba que la IA coloca los barcos correctamente.
        """
        self.logic_ia.colocar_barcos_maquina()
        barcos_colocados = sum(1 for btn in self.tablero_maquina.buttons if btn.tiene_barco)
        self.assertEqual(barcos_colocados, 10, "La máquina no colocó 10 barcos")

class TestLogicJuego(TestCase):
    """
    Pruebas unitarias para la clase LogicJuego.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.tablero_jugador = TableroJugador()
        self.tablero_maquina = TableroMaquina()
        self.logic_juego = LogicJuego(self.tablero_jugador, self.tablero_maquina)

    def test_realizar_ataque_sin_barcos(self):
        """
        Prueba que se muestra el popup adecuado cuando se intenta realizar un ataque sin barcos colocados.
        """
        boton_jugador = Button()
        self.tablero_jugador.buttons.append(boton_jugador)

        boton_maquina = Button()
        self.tablero_maquina.buttons.append(boton_maquina)

        with mock.patch('modell.LogicJ.Popup') as mock_popup:
            self.logic_juego.realizar_ataque(boton_maquina)

            mock_popup.assert_called_once_with(
                title="Colocar barcos",
                content=mock.ANY,
                size_hint=(None, None),
                size=(400, 200)
            )

        self.assertEqual(boton_maquina.text, '')
        self.assertFalse(boton_maquina.disabled)

class TestBD(unittest.TestCase):
    """
    Pruebas unitarias para la clase BD.
    """

    @patch('controller.BD.psycopg2.connect')
    def setUp(self, mock_connect):
        """
        Configuración inicial para cada prueba.
        """
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        connection_string = "postgresql://user:password@host/database"
        self.bd = BD(connection_string)

    def test_insert_victoria_jugador(self):
        """
        Prueba que la función insert_victoria_jugador actualiza correctamente la base de datos.
        """
        self.bd.insert_victoria_jugador()
        self.mock_cursor.execute.assert_called_with("UPDATE estadisticas SET victorias_jugador = victorias_jugador + 1")
        self.mock_conn.commit.assert_called_once()

    def test_insert_derrota_jugador(self):
        """
        Prueba que la función insert_derrota_jugador actualiza correctamente la base de datos.
        """
        self.bd.insert_derrota_jugador()
        self.mock_cursor.execute.assert_called_with("UPDATE estadisticas SET derrotas_jugador = derrotas_jugador + 1")
        self.mock_conn.commit.assert_called_once()

    def test_insert_victoria_ia(self):
        """
        Prueba que la función insert_victoria_ia actualiza correctamente la base de datos.
        """
        self.bd.insert_victoria_ia()
        self.mock_cursor.execute.assert_called_with("UPDATE estadisticas SET victorias_ia = victorias_ia + 1")
        self.mock_conn.commit.assert_called_once()

    def test_insert_derrota_ia(self):
        """
        Prueba que la función insert_derrota_ia actualiza correctamente la base de datos.
        """
        self.bd.insert_derrota_ia()
        self.mock_cursor.execute.assert_called_with("UPDATE estadisticas SET derrotas_ia = derrotas_ia + 1")
        self.mock_conn.commit.assert_called_once()

    def test_obtener_estadisticas(self):
        """
        Prueba que la función obtener_estadisticas devuelve los valores correctos de la base de datos.
        """
        expected_stats = (10, 5, 8, 7)
        self.mock_cursor.fetchone.return_value = expected_stats
        stats = self.bd.obtener_estadisticas()
        self.mock_cursor.execute.assert_called_with("SELECT victorias_jugador, derrotas_jugador, victorias_ia, derrotas_ia FROM estadisticas")
        self.assertEqual(stats, expected_stats)

if __name__ == '__main__':
    unittest.main()
