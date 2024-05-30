from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex

class TableroJugador(GridLayout):
    """
    Clase que representa el tablero del jugador en el juego de BattleShip.
    Hereda de GridLayout y crea una cuadrícula de botones y etiquetas.
    """

    def __init__(self, **kwargs):
        """
        Inicializa el tablero del jugador con una cuadrícula de 9x9.

        Args:
            **kwargs: Argumentos clave adicionales para la inicialización del GridLayout.
        """
        super().__init__(**kwargs)
        self.cols = 9
        self.rows = 9
        self.buttons = []
        self.size_hint = (1, 1)  # Ajuste automático al tamaño de la ventana
        self.create_board()

    def create_board(self):
        """
        Crea el tablero del jugador añadiendo etiquetas para las columnas y filas
        y botones para cada celda del tablero.
        """
        for col in range(8):
            label = Label(text=chr(ord('A') + col))
            self.add_widget(label)

        for row in range(8):
            label = Label(text=str(row + 1))
            self.add_widget(label)
            for col in range(8):
                btn = Button()
                self.add_widget(btn)
                self.buttons.append(btn)

    def mostrar_mensaje_luchar(self):
        """
        Muestra un popup con el mensaje "¡A LUCHAR!!" para indicar que el juego ha comenzado.
        """
        content = Label(text="¡A LUCHAR!!", font_size=40)
        popup = Popup(title="Preparados para la batalla", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

class TableroMaquina(GridLayout):
    """
    Clase que representa el tablero de la máquina en el juego de BattleShip.
    Hereda de GridLayout y crea una cuadrícula de botones y etiquetas.
    """

    def __init__(self, **kwargs):
        """
        Inicializa el tablero de la máquina con una cuadrícula de 9x9.

        Args:
            **kwargs: Argumentos clave adicionales para la inicialización del GridLayout.
        """
        super().__init__(**kwargs)
        self.cols = 9
        self.rows = 9
        self.buttons = []
        self.size_hint = (1, 1)  # Ajuste automático al tamaño de la ventana
        
        self.create_board()

    def create_board(self):
        """
        Crea el tablero de la máquina añadiendo etiquetas para las columnas y filas
        y botones para cada celda del tablero. Los botones tienen un color de fondo
        predeterminado y una propiedad adicional `tiene_barco`.
        """
        for col in range(8):
            label = Label(text=chr(ord('A') + col))
            self.add_widget(label)

        for row in range(8):
            label = Label(text=str(row + 1))
            self.add_widget(label)
            for col in range(8):
                btn = Button(text='', background_color=get_color_from_hex("#6495ED"))
                btn.tiene_barco = False  # Agregar esta propiedad
                self.add_widget(btn)
                self.buttons.append(btn)
