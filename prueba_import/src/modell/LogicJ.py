import random
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from src.controller.BD import BD
from src.conecction.db_connection import DBConnection


class LogicJuego:
    """
    Clase que maneja la lógica del juego BattleShip, incluyendo la colocación de barcos y los turnos de ataque.
    """

    def __init__(self, tablero_jugador, tablero_maquina):
        self.tablero_jugador = tablero_jugador
        self.tablero_maquina = tablero_maquina
        self.barcos_jugador = []
        self.barcos_maquina = []
        self.turno_jugador = True
        self.botones_atacados = set()  # conjunto para almacenar botones atacados por la maquina
        self.colocar_barcos_maquina()
        self.juego_iniciado = False


        # Inicializar la conexión a la base de datos ↓
        db_connection = DBConnection.get_instance()
        self.bd = BD(db_connection.connection)

    def colocar_barcos_jugador(self, instance):
        if len(self.barcos_jugador) < 10 and instance in self.tablero_jugador.buttons and instance.text == '':
            instance.text = 'X'
            instance.background_color = get_color_from_hex("#FF0000")
            instance.tiene_barco = True
            self.barcos_jugador.append(instance)
        elif len(self.barcos_jugador) == 10 and len(self.barcos_maquina) == 10:
            self.tablero_jugador.mostrar_mensaje_luchar()
            self.juego_iniciado = True 


    def colocar_barcos_maquina(self):
        """
        Coloca los barcos de la máquina de forma aleatoria en su tablero.
        """
        botones_disponibles = [btn for btn in self.tablero_maquina.buttons if not btn.tiene_barco]
        for _ in range(10):
            boton = random.choice(botones_disponibles)
            boton.tiene_barco = True
            self.barcos_maquina.append(boton)
            botones_disponibles.remove(boton)

    def realizar_ataque(self, instance):
        """
        Realiza un ataque en el tablero correspondiente basado en el turno actual.

        Args:
            instance (Button): El botón que representa una celda del tablero.
        """
        if self.juego_iniciado:  # Verificar si el juego ha comenzado
            if self.turno_jugador:
                self.ataque_jugador(instance)
            else:
                self.ataque_maquina()
        else:
            self.mostrar_mensaje_colocar_barcos()
            # No realizar ninguna acción en el botón
            return

        # El resto del código para realizar el ataque
        if not instance.disabled:
            if self.turno_jugador:
                self.ataque_jugador(instance)
            else:
                self.ataque_maquina()
        instance.disabled = True
    
    def ataque_jugador(self, instance):
        """
        Maneja el ataque del jugador en el tablero de la máquina.

        Args:
            instance (Button): El botón que representa una celda del tablero.
        """
        if instance in self.tablero_maquina.buttons and not instance.disabled:
            if hasattr(instance, 'tiene_barco') and instance.tiene_barco:
                instance.text = 'X'
                instance.background_color = get_color_from_hex("#FF0000")
                self.barcos_maquina.remove(instance)
                if not self.barcos_maquina:
                    self.mostrar_mensaje_victoria_jugador()
            else:
                instance.text = '-'
                instance.background_color = get_color_from_hex("#6495ED")
            instance.disabled = True
            self.turno_jugador = False

    def ataque_maquina(self):
        """
        Maneja el ataque de la máquina en el tablero del jugador.
        """
        botones_disponibles = [btn for btn in self.tablero_jugador.buttons if btn not in self.botones_atacados]
        if botones_disponibles:
            boton = random.choice(botones_disponibles)
            self.botones_atacados.add(boton)
            if boton in self.barcos_jugador:
                boton.text = 'X'
                boton.background_color = get_color_from_hex("#FF0000")
                self.barcos_jugador.remove(boton)
                self.mostrar_mensaje_hundimiento_maquina()
                if not self.barcos_jugador:
                    self.mostrar_mensaje_victoria_maquina()
            else:
                boton.text = '-'
                boton.background_color = get_color_from_hex("#6495ED")
            boton.disabled = True
            self.turno_jugador = True

    def mostrar_mensaje_victoria_jugador(self):
        """
        Muestra un popup indicando que el jugador ha ganado la batalla
        y actualiza las estadísticas en la base de datos.
        """
        content = Label(text="¡Felicidades! Has ganado la batalla.", font_size=40)
        popup = Popup(title="Victoria", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

        # Actualizar las estadísticas en la base de datos ↓
        self.bd.insert_victoria_jugador()
        self.bd.insert_derrota_ia()

    def mostrar_mensaje_victoria_maquina(self):
        """
        Muestra un popup indicando que la máquina ha ganado la batalla
        y actualiza las estadísticas en la base de datos.
        """
        content = Label(text="¡Lo siento! Has perdido la batalla.", font_size=40)
        popup = Popup(title="Derrota", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

        # Actualizar las estadísticas en la base de datos ↓
        self.bd.insert_victoria_ia()
        self.bd.insert_derrota_jugador()

    def mostrar_mensaje_colocar_barcos(self):
        """
        Muestra un popup indicando que ambos jugadores deben colocar sus barcos antes de atacar.
        """
        content = Label(text="Ambos jugadores deben colocar sus barcos antes de atacar.", font_size=20)
        popup = Popup(title="Colocar barcos", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()    

    def mostrar_mensaje_hundimiento_maquina(self):
        """
        Muestra un mensaje indicando que la máquina ha hundido un barco del jugador.
        """
        content = Label(text="¡La máquina ha hundido uno de tus barcos!", font_size=20)
        popup = Popup(title="Hundimiento", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
