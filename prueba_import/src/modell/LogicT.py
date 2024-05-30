#Uso de la base de datos en linea 135
import random
from kivy.utils import get_color_from_hex
from src.controller.BD import BD
from src.conecction.db_connection import DBConnection



class LogicIA:
    """
    Clase que maneja la lógica de la inteligencia artificial (IA) en el juego BattleShip.
    """

    def __init__(self, tablero_maquina, tablero_jugador):
        """
        Inicializa la lógica de la IA con los tableros de la máquina y del jugador.

        Args:
            tablero_maquina (TableroMaquina): El tablero de la máquina.
            tablero_jugador (TableroJugador): El tablero del jugador.
        """
        self.tablero_maquina = tablero_maquina
        self.tablero_jugador = tablero_jugador
        self.barcos_maquina = []
        self.disparos_anteriores = []

    def colocar_barcos_maquina(self):
        """
        Coloca los barcos de la máquina de forma aleatoria en su tablero.
        """
        barcos_colocados = 0
        botones_disponibles = self.tablero_maquina.buttons.copy()
        while barcos_colocados < 10:
            if not botones_disponibles:
                raise ValueError("No hay suficientes casillas disponibles para colocar los barcos.")
            boton = random.choice(botones_disponibles)
            boton.tiene_barco = True
            boton.text = 'X'
            boton.background_color = get_color_from_hex("#FF0000")
            self.barcos_maquina.append(boton)
            botones_disponibles.remove(boton)
            barcos_colocados += 1

    def realizar_ataque_maquina(self):
        """
        Realiza un ataque en el tablero del jugador, utilizando una estrategia de inteligencia artificial.
        """
        botones_disponibles = self.get_botones_disponibles()
        if botones_disponibles:
            boton = self.disparo_ordenador_medio_listo(botones_disponibles)
            resultado = self.atacar_boton(boton)
            self.disparos_anteriores.append((boton, resultado))

    def get_botones_disponibles(self):
        """
        Obtiene una lista de botones disponibles para el ataque en el tablero del jugador.

        Returns:
            list: Una lista de botones disponibles.
        """
        botones_disponibles = []
        for btn in self.tablero_jugador.buttons:
            if btn.text == '' and not btn.disabled:
                botones_disponibles.append(btn)
        return botones_disponibles

    def disparo_ordenador_medio_listo(self, botones_disponibles):
        """
        Realiza un disparo por parte de la máquina en el tablero del jugador, dando prioridad
        a los botones vecinos de los botones que contienen un barco conocido.

        Args:
        - botones_disponibles (list): La lista de botones disponibles en el tablero del jugador.

        Returns:
        - Button: El botón seleccionado para realizar el disparo.
        """
        # Se generan los botones prioritarios, que son aquellos vacíos y tienen al menos un vecino con un barco conocido
        botones_prioritarios = [
            btn for btn in botones_disponibles
            if self.algun_vecino_es_X(btn)
        ]

        if botones_prioritarios:  # Si hay botones prioritarios disponibles
            return random.choice(botones_prioritarios)  # Se elige uno de forma aleatoria
        else:
            return random.choice(botones_disponibles)  # Si no hay botones prioritarios, se elige uno al azar

    def algun_vecino_es_X(self, boton):
        """
        Comprueba si alguno de los vecinos de un botón contiene una 'X'.

        Args:
            boton (Button): El botón cuyo vecindario se va a verificar.

        Returns:
            bool: True si alguno de los vecinos contiene una 'X', False en caso contrario.
        """
        botones_vecinos = self.get_botones_adyacentes(boton)
        return any(btn.text == 'X' for btn in botones_vecinos)

    def get_botones_adyacentes(self, boton):
        """
        Obtiene una lista de botones adyacentes a un botón dado.

        Args:
            boton (Button): El botón de referencia.

        Returns:
            list: Una lista de botones adyacentes disponibles.
        """
        fila = self.tablero_jugador.buttons.index(boton) // 8
        columna = self.tablero_jugador.buttons.index(boton) % 8
        botones_adyacentes = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nueva_fila = fila + i
                nueva_columna = columna + j
                if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                    indice = nueva_fila * 8 + nueva_columna
                    boton_adyacente = self.tablero_jugador.buttons[indice]
                    botones_adyacentes.append(boton_adyacente)
        return botones_adyacentes

    def atacar_boton(self, boton):
        """
        Realiza un ataque en el botón especificado.

        Args:
            boton (Button): El botón a atacar.

        Returns:
            str: 'X' si el ataque fue exitoso, '-' si no lo fue.
        """
        if boton in self.tablero_jugador.buttons and boton.text == '':
            if boton in LogicJugador.barcos_jugador:
                boton.text = 'X'
                boton.background_color = get_color_from_hex("#FF0000")
                LogicJugador.barcos_jugador.remove(boton)
                if not LogicJugador.barcos_jugador:
                    
                    # Mostrar mensaje de victoria de la máquina ↓
                    db_connection = DBConnection.get_instance()
                    self.bd = BD(db_connection.connection)
                    
                    bd.insert_victoria_ia()
                    bd.insert_derrota_jugador()
                resultado = 'X'
            else:
                boton.text = '-'
                boton.background_color = get_color_from_hex("#6495ED")
                resultado = '-'
            boton.disabled = True
            return resultado


class LogicJugador:
    """
    Clase que maneja la lógica del jugador en el juego BattleShip.
    """

    def __init__(self, tablero_jugador, tablero_maquina):
        """
        Inicializa la lógica del jugador con los tableros del jugador y de la máquina.

        Args:
            tablero_jugador (TableroJugador): El tablero del jugador.
            tablero_maquina (TableroMaquina): El tablero de la máquina.
        """
        self.tablero_jugador = tablero_jugador
        self.tablero_maquina = tablero_maquina
        self.barcos_jugador = []
        self.barcos_colocados = 0

    def colocar_barco_jugador(self, instance):
        """
        Coloca un barco del jugador en el tablero.

        Args:
            instance (Button): El botón que representa una celda del tablero.
        """
        if self.barcos_colocados < 10 and instance in self.tablero_jugador.buttons and instance.text == '':
            instance.text = 'X'
            instance.background_color = get_color_from_hex("#FF0000")
            self.barcos_jugador.append(instance)
            self.barcos_colocados += 1
            if self.barcos_colocados == 10:
                self.tablero_jugador.mostrar_mensaje_luchar()
                for barco in self.barcos_jugador:
                    barco.background_color = get_color_from_hex("#808080")  # Cambiar color a gris

    def realizar_ataque_jugador(self, instance):
        """
        Realiza un ataque del jugador en el tablero de la máquina.

        Args:
            instance (Button): El botón que representa una celda del tablero.
        """
        if instance in self.tablero_maquina.buttons and instance.text == '':
            if random.random() < 0.2:
                instance.text = 'X'
                instance.background_color = get_color_from_hex("#FF0000")
            else:
                instance.text = '-'
                instance.background_color = get_color_from_hex("#6495ED")
            instance.disabled = True
