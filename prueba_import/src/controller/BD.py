import psycopg2

class BD:
    """
    Clase que maneja la conexión y operaciones con la base de datos PostgreSQL.
    """

    def __init__(self, connection_string):
        """
        Inicializa una conexión con la base de datos utilizando la cadena de conexión proporcionada.

        Args:
            connection_string (str): La cadena de conexión para conectarse a la base de datos.
        """
        try:
            self.connection = psycopg2.connect(connection_string)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def insert_victoria_jugador(self):
        """
        Inserta una nueva victoria del jugador en la base de datos.
        """
        self.cursor.execute("UPDATE estadisticas SET victorias_jugador = victorias_jugador + 1")
        self.connection.commit()

    def insert_derrota_jugador(self):
        """
        Inserta una nueva derrota del jugador en la base de datos.
        """
        self.cursor.execute("UPDATE estadisticas SET derrotas_jugador = derrotas_jugador + 1")
        self.connection.commit()

    def insert_victoria_ia(self):
        """
        Inserta una nueva victoria de la IA en la base de datos.
        """
        self.cursor.execute("UPDATE estadisticas SET victorias_ia = victorias_ia + 1")
        self.connection.commit()

    def insert_derrota_ia(self):
        """
        Inserta una nueva derrota de la IA en la base de datos.
        """
        self.cursor.execute("UPDATE estadisticas SET derrotas_ia = derrotas_ia + 1")
        self.connection.commit()

    def obtener_estadisticas(self):
        """
        Obtiene las estadísticas actuales de victorias y derrotas desde la base de datos.

        Returns:
            tuple: Una tupla que contiene el número de victorias del jugador, derrotas del jugador, victorias de la IA y derrotas de la IA.
        """
        self.cursor.execute("SELECT victorias_jugador, derrotas_jugador, victorias_ia, derrotas_ia FROM estadisticas")
        estadisticas = self.cursor.fetchone()
        return estadisticas

    def eliminar_estadisticas(self):
        """
        Elimina todas las estadísticas de la base de datos.
        """
        self.cursor.execute("DELETE FROM estadisticas")
        self.connection.commit()

    def actualizar_estadisticas(self, victorias_jugador, derrotas_jugador, victorias_ia, derrotas_ia):
        """
        Actualiza las estadísticas con los valores proporcionados.

        Args:
            victorias_jugador (int): El nuevo valor de victorias del jugador.
            derrotas_jugador (int): El nuevo valor de derrotas del jugador.
            victorias_ia (int): El nuevo valor de victorias de la IA.
            derrotas_ia (int): El nuevo valor de derrotas de la IA.
        """
        self.cursor.execute("""
            UPDATE estadisticas
            SET victorias_jugador = %s,
                derrotas_jugador = %s,
                victorias_ia = %s,
                derrotas_ia = %s
        """, (victorias_jugador, derrotas_jugador, victorias_ia, derrotas_ia))
        self.connection.commit()