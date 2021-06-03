import sys
sys.path.append('./src/modules')
sys.path.append('./src/components/casosComunas')
sys.path.append('./src/components/casosRegiones')
sys.path.append('./src/middleware')

import oracle_module
import casosComunas_controller
import casosRegiones_controller
import middleware as mw

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

if __name__ == '__main__':
    connection = oracle_module.connect()

    #borrarlaWea(connection)
    #casosComunas_controller.init(connection)
    #casosRegiones_controller.init(connection)

    
    #mw.crearRegion(connection)
    #mw.crearComuna(connection)
    mw.crearComuna(connection)
    mw.fusionComunas(connection)

    # BUG AL FUSIONAR COMUNAS QUE FORMAN PARTE DE 2 REGIONES CON COMUNAS NUEVAS

    oracle_module.disconnect(connection)
