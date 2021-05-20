import sys
sys.path.append('./src/modules')
sys.path.append('./src/components/casosComunas')

import oracle_module
import casosComunas_controller

connection = oracle_module.connect()

casosComunas_controller.init(connection)

oracle_module.disconnect(connection)


#cursor.execute(
#    """
#        SELECT first_name, last_name, person_id
#        FROM Persona
#    """
#)
#for fname, lname, person_id in cursor:
#    print("Values:", fname, lname, person_id)
