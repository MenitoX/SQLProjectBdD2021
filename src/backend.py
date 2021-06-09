import sys
sys.path.append('./src/components/casosComunas')
sys.path.append('./src/components/casosRegiones')

import importlib
import casosComunas_controller
import casosRegiones_controller

def main():
    # Debug Bool | True -> Info de DEBUG , False -> Ejecución normal
    __DEBUG__ = True
    text = "1. Crear comuna\n2. Crear región\n3. Ver casos de comunas\n4. Ver casos de regiones\n5. Sumar casos\n6. Restar casos\n7. Top casos comunas\n8. Top casos regiones\n9. Fusionar regiones\n10. Fusionar comunas\nexit. Salir\n\nInput: "
    oracle_module = importlib.import_module('.oracle_module', package='modules')
    mw = importlib.import_module('.middleware', package='middleware')
    
    connection = oracle_module.connect()
    
    mw.init(connection)
    mw.checkErase(connection)
    methods = [mw.crearComuna, mw.crearRegion, mw.verCasosComunas, mw.verCasosRegiones, mw.addCasos, mw.lessCasos, mw.checkTopComunas, mw.checkTopRegiones, mw.fusionRegiones, mw.fusionComunas]
    commandList = [i for i in "1.2.3.4.5.6.7.8.9.10".split(".")]
    command = "place_holder"
    while command != "exit":
        command = input(text).strip("\n").strip(" ")
        if command == 'exit':
            print("Gracias por usar mi programa! :D ")
            break
        if command not in commandList:
            print('Input inválido\n')
            continue
        index = int(command) - 1
        try:
            methods[index](connection, __DEBUG__)
            print("\n")
            mw.checkErase(connection)
            print("\n")
        except Exception as error:
            print(error)
        
    


    oracle_module.disconnect(connection)
