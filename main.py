import sys
sys.path.append('./src/modules')
sys.path.append('./src/components/casosComunas')

import oracle_module
import casosComunas_controller


connection = oracle_module.connect()

#casosComunas_controller.init(connection)

casosComunas_controller.get("666", connection)

oracle_module.disconnect(connection)


