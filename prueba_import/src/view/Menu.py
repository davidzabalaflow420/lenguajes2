#Uso de la base de datos en las lineas:37,52,86
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from src.view.Tablero import TableroJugador, TableroMaquina
from src.modell.LogicT import LogicIA, LogicJugador
from src.modell.LogicJ import LogicJuego
from src.controller.BD import BD
from src.conecction.db_connection import DBConnection


class MenuScreen(BoxLayout):
    """
    Clase que representa la pantalla del menú principal de la aplicación.
    """

    def __init__(self, **kwargs):
        """
        Inicializa la pantalla del menú con botones para Jugar, Nosotros, Estadísticas y Salir.

        Args:
            **kwargs: Argumentos clave adicionales para la inicialización del BoxLayout.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 20]

        self.btn_jugar = Button(text='Jugar', size_hint_y=0.1)
        self.btn_jugar.bind(on_press=self.jugar_pressed)
        self.add_widget(self.btn_jugar)

        self.btn_nosotros = Button(text='Nosotros', size_hint_y=0.1)
        self.btn_nosotros.bind(on_press=self.nosotros_pressed)
        self.add_widget(self.btn_nosotros)
        
        #Botón de las estadisticas ↓
        self.btn_estadisticas = Button(text='Estadísticas', size_hint_y=0.1)
        self.btn_estadisticas.bind(on_press=self.estadisticas_pressed)
        self.add_widget(self.btn_estadisticas)

        self.btn_salir = Button(text='Salir', size_hint_y=0.1)
        self.btn_salir.bind(on_press=self.salir_pressed)
        self.add_widget(self.btn_salir)

        self.chess_layout = BoxLayout(orientation='horizontal')
        self.tablero_jugador = TableroJugador()
        self.tablero_maquina = TableroMaquina()
        self.chess_layout.add_widget(self.tablero_jugador)
        self.chess_layout.add_widget(self.tablero_maquina)
        
        #Conexión a la base de datos ↓
        db_connection = DBConnection.get_instance()
        self.bd = BD(db_connection.connection)

    def jugar_pressed(self, instance):
        """
        Método que se ejecuta al presionar el botón 'Jugar'.
        Cambia la vista al tablero del juego y configura la lógica del juego.

        Args:
            instance: La instancia del botón presionado.
        """
        self.clear_widgets()
        self.add_widget(self.chess_layout)
        self.logic_juego = LogicJuego(self.tablero_jugador, self.tablero_maquina)

        for btn in self.tablero_jugador.buttons:
            btn.bind(on_press=self.logic_juego.colocar_barcos_jugador)

        for btn in self.tablero_maquina.buttons:
            btn.bind(on_press=self.logic_juego.realizar_ataque)

    def nosotros_pressed(self, instance):
        """
        Método que se ejecuta al presionar el botón 'Nosotros'.
        Muestra un popup con información sobre los desarrolladores.

        Args:
            instance: La instancia del botón presionado.
        """
        content = Label(text="Somos David y Andrés. Bienvenido a BattleShip.")
        popup = Popup(title="Acerca de Nosotros", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    #Logica para el botón de estadisticas y la base de datos ↓
    def estadisticas_pressed(self, instance):
        """
        Método que se ejecuta al presionar el botón 'Estadísticas'.
        Muestra un popup con las estadísticas del juego.

        Args:
            instance: La instancia del botón presionado.
        """
        estadisticas = self.bd.obtener_estadisticas()
        content = Label(text=f"Victorias jugador: {estadisticas[0]}\nDerrotas jugador: {estadisticas[1]}\nVictorias IA: {estadisticas[2]}\nDerrotas IA: {estadisticas[3]}")
        popup = Popup(title="Estadísticas del juego", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def salir_pressed(self, instance):
        """
        Método que se ejecuta al presionar el botón 'Salir'.
        Detiene la aplicación.

        Args:
            instance: La instancia del botón presionado.
        """
        App.get_running_app().stop()
