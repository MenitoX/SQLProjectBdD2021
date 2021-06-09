@SQLProjectPrototipe

DEV: Pablo Contreras
ROL: 201973572-1

Este proyecto se divide en 5 capas:
    Components:
        Capa de componentes, cuentan con un repositorio que contiene las funciones relacionadas
        a la comunicación con SQL y un controlador que implementa esta funciones en métodos más externos.
    
    Middleware:
        Las funciones asignadas a la tarea en su mayoría, la capa de middleware funciona como puente entre nuestro backend y las funciones del controlador de los componentes.
    
    Models:
        Modelos de las filas de los componentes y sus atributos.

    Modules:
        Módulo de conección a Oracle.
    
    Templates:
        CSVs relacionados a la tarea.

Este código es ejecutable con un simple "python main.py"

Se necesita un archivo .env con los atributos USER, PASS y URL en root.

El booleano DEGUG en backend.py determina si se hace un display de información de DEBUG respecto a las tablas.

Las librerias utilizadas están listadas en requirements.txt, en cualquier caso si se está en windows, ejecutando init.bat se creará un virutal environment junto a las librerias necesarias para ejecutar el código.

Consideraciones:
    - No me manejo muy bien con los imports de python y puede ser algo desastroso a ratos, por alguna razón si no importo los controladores al backend.py el código falla.
    
    - Se valida la data de los inputs, pero intentar no introducir información erronea apropósito.

    - Cualquier otra consulta/duda será respondida durante la defensa.