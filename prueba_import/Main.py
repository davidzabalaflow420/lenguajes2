# Main.py
from kivy.app import App
from src.view.Menu import MenuScreen
from src.conecction.db_connection import DBConnection


class Main(App):
    """
    Clase principal que hereda de la clase App de Kivy. Este es el punto de entrada
    para la aplicación Kivy.
    """

    def build(self):
        """
        Construye el widget raíz de la aplicación.

        Devuelve:
            MenuScreen: El widget raíz de la aplicación.
        """
        return MenuScreen()

if __name__ == '__main__':
    """
    Si este módulo se ejecuta como el programa principal, crea una instancia
    de la clase Main y ejecuta la aplicación Kivy.
    """
    Main().run()
