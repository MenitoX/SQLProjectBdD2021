import sys
sys.path.append('./src/components/casosComunas')
sys.path.append('./src/components/casosRegiones')

import importlib
import casosComunas_controller
import casosRegiones_controller

def borrarlaWea(connection):
    cursor = connection.cursor()
    cursor.execute("""
            DROP TABLE CASOS_POR_REGION       
                """)
    cursor.execute("""
            DROP TABLE CASOS_POR_COMUNA       
                """)
    cursor.close()
    connection.commit()
    return

def main():
    # Debug Bool
    __DEBUG__ = False
    text = "1. Crear comuna\n2. Crear región\n3. Ver casos de comunas\n4. Ver casos de regiones\n5. Sumar casos\n6. Restar casos\n7. Top casos comunas\n8. Top casos regiones\n9. Fusionar regiones\n10. Fusionar comunas\nexit. Salir\n\nInput: "
    oracle_module = importlib.import_module('.oracle_module', package='modules')
    mw = importlib.import_module('.middleware', package='middleware')
    
    
    connection = oracle_module.connect()
    
    # ACUERDATE DE BORRAR ESTO POR EL AMOR DE DIOS
    borrarlaWea(connection)
    
    mw.init(connection)
    mw.checkErase(connection)
    methods = [mw.crearComuna, mw.crearRegion, mw.verCasosComunas, mw.verCasosRegiones, mw.addCasos, mw.lessCasos, mw.checkTopComunas, mw.checkTopRegiones, mw.fusionRegiones, mw.fusionComunas]
    command = "place_holder"
    while command != "exit":
        command = input(text).strip("\n").strip(" ")
        if command == 'exit':
            print("Gracias por usar mi programa! :D ")
            break
        index = int(command) - 1
        try:
            methods[index](connection, __DEBUG__)
        except Exception as error:
            print(error)
        print("\n")
        mw.checkErase(connection)
        print("\n")
    


    oracle_module.disconnect(connection)
