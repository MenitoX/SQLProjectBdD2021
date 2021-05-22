import sys
sys.path.append('./src/modules')
sys.path.append('./src/components/casosComunas')
sys.path.append('./src/components/casosRegiones')
sys.path.append('./src/middleware')

import oracle_module
import casosComunas_controller
import casosRegiones_controller
import middleware as mw

if __name__ == '__main__':
    connection = oracle_module.connect()

    #casosComunas_controller.init(connection)
    #casosRegiones_controller.init(connection)
    #casosRegiones_controller.delete("ERASE ME", connection)
    #casosRegiones_controller.trigger(connection)
    #casosRegiones_controller.trigger(connection)
    #casosComunas_controller.patch("15101", [None, None,"5000" ,None], connection)
    mw.addCasos(connection)
    #mw.crearComuna(connection)
    mw.checkErase(connection)
    mw.checkTopRegiones(connection)
    mw.checkTopComunas(connection)
    oracle_module.disconnect(connection)

