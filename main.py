import sys
sys.path.append('./src/modules')
sys.path.append('./src/components/casosComunas')
sys.path.append('./src/components/casosRegiones')

import oracle_module
import casosComunas_controller
import casosRegiones_controller


if __name__ == '__main__':
    connection = oracle_module.connect()

    casosComunas_controller.init(connection)
    casosRegiones_controller.init(connection)

    oracle_module.disconnect(connection)


