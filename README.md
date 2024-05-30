## BattleShip
Este es un juego de BattleShip desarrollado en Python utilizando el framework Kivy.

## Por
David Zabala y Brahian Osorio

## Estructura del Proyecto
El programa está estructurado siguiendo el patrón de diseño Modelo-Vista-Controlador (MVC). Los archivos se organizan de la siguiente manera:

 ## Main.py: Es el archivo principal que inicia la aplicación Kivy y carga la pantalla del menú principal.
 ## src/view/: Este directorio contiene los archivos relacionados con la interfaz de usuario (Vista):
 ## Menu.py: Contiene la clase MenuScreen que representa la pantalla del menú principal.
 ## Tablero.py: Contiene las clases TableroJugador y TableroMaquina que crean los tableros de juego.
 ## src/model/: Este directorio contiene los archivos relacionados con la lógica del juego (Modelo):
 ## LogicJ.py: Contiene la clase LogicJuego que maneja la lógica principal del juego.
 ## LogicT.py: Contiene las clases LogicIA y LogicJugador que manejan la lógica de la inteligencia artificial y el jugador, respectivamente.
 ## src/controller/: Este directorio contiene los archivos relacionados con el controlador:
 ## BD.py: Contiene la clase BD que se encarga de interactuar con la base de datos PostgreSQL.
 ## src/config/: Este directorio contiene los archivos de configuración:
 ## Config.py: Contiene la información de configuración para conectarse a la base de datos PostgreSQL.
 ## src/connection/: Este directorio contiene los archivos relacionados con la conexión a la base de datos:
 ## db_connection.py: Contiene la clase DBConnection que establece la conexión a la base de datos PostgreSQL.

## Patrón Modelo-Vista-Controlador (MVC)
El programa sigue el patrón de diseño Modelo-Vista-Controlador (MVC), que separa la lógica del programa en tres componentes principales:

  ## Modelo: Representa la lógica del juego y los datos. Las clases LogicJuego, LogicIA y LogicJugador se encargan de esta parte.
  ## Vista: Representa la interfaz de usuario. Las clases MenuScreen, TableroJugador y TableroMaquina se encargan de esta parte.
  ## Controlador: Maneja la interacción entre el Modelo y la Vista. La clase BD se encarga de esta parte, interactuando con la base de datos PostgreSQL.
  ## Esta separación de responsabilidades promueve un código más modular, mantenible y fácil de entender. Además, facilita la realización de cambios y la ampliación del programa en el futuro.

## Requisitos previos
Antes de ejecutar el juego, asegúrate de tener instalados los siguientes componentes:

Python 3.x (https://www.python.org/downloads/)
Kivy (https://kivy.org/#gettingstarted)
psycopg2 (https://pypi.org/project/psycopg2/)
Git (https://git-scm.com/)

## Instalación
Clona el repositorio del juego:


git clone <URL-del-repositorio>
Navega hasta el directorio del juego:

cd <nombre-del-repositorio>
Crea un entorno virtual:

python -m venv env
Activa el entorno virtual:

En Windows:

env\Scripts\activate.bat
En macOS/Linux:

source env/bin/activate
Instala las dependencias del proyecto utilizando el archivo requirements.txt:

pip install -r requirements.txt
Configura la conexión a la base de datos:

Abre el archivo src/config/Config.py.
Actualiza la información de conexión con tus credenciales.

Ejecuta el juego:
En la consola escribe:
python Main.py
Esto iniciará la aplicación Kivy y se abrirá la ventana principal del juego. Sigue las instrucciones en la ventana del juego para jugar.



## Base de datos
por efectos de la practica tuve que bajar la base de datos por lo que no correra el programa ni los test. Adiciono el codigo para crear la tabla que funciona con este programa en Table.sql.
Lo unico que debes hacer es crear en esa tabla en una base de datos de neon.tech y actualizar las credenciales
"# codigolimpio"  
"# codigolimpio"  
