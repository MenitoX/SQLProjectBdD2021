from casosComunas_model import CasoComuna
import casosRegiones_repository as repository
import casosComunas_controller as controllerComunas
from casosRegiones_model import CasoRegion

#REGION, CODIGO REGION, POBLACION, CASOS 

def init(connection):
    cursor = connection.cursor()
    # For dev, comment if initialized
    repository.init(cursor)
    try:
        file = open("src\\templates\\RegionesComunas.csv", "r")
        firstLine = True
        Regiones = list()
        for i in file:
            if firstLine:
                firstLine = False
                continue
            NOMBRE, CODIGO_REGION, CODIGO_COMUNA  = i.strip("\n").split(",")
            if NOMBRE not in Regiones:
                casoComuna : CasoComuna = controllerComunas.get(CODIGO_COMUNA, connection)
                if casoComuna:
                    casoRegion = CasoRegion(NOMBRE, CODIGO_REGION, casoComuna.poblacion, casoComuna.casos)
                    post(casoRegion, connection)
                Regiones.append(NOMBRE)
            else:
                casoRegion : CasoRegion = get(CODIGO_REGION, connection)
                casoComuna : CasoComuna = controllerComunas.get(CODIGO_COMUNA, connection)
                if casoComuna:
                    newCasos = casoComuna.casos + casoRegion.casos
                    newPoblacion = casoComuna.poblacion + casoRegion.poblacion
                    patch(CODIGO_REGION, [None, None, newPoblacion, newCasos], connection)
    except Exception as error:
        print("No se pudo inicializar CASOS_POR_REGION en base al csv: ", error)
    else:
        print("Primera inicializacion de CASOS_POR_REGION finalizada en base a archivo csv")
        connection.commit()
    finally:
        file.close()
        cursor.close()
        return

def get(id : str, connection):
    cursor = connection.cursor()
    casoRegion : CasoRegion = None
    try:
        casoRegion = repository.get(id, cursor)
    except Exception as error:
        print("Error GET a CASOS_POR_REGION: ", error)
        return 
    else:
        print("GET exitoso a CASOS_POR_REGION")
    finally:
        cursor.close()
        return casoRegion

def post(casoRegion : CasoRegion, connection):
    cursor = connection.cursor()
    try:
        repository.post(casoRegion, cursor)
    except Exception as error:
        print("Error POST a CASOS_POR_REGION: ", error)
    else:
        print("POST exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

def delete(id : str, connection):
    cursor = connection.cursor()
    try:
        repository.delete(id, cursor)
    except Exception as error:
        print("Error DELETE a CASOS_POR_REGION: ", error)
    else:
        print("DELETE exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

def patch(id :str, casoRegion : list(), connection):
    cursor = connection.cursor()
    casoRegion = CasoRegion(casoRegion[0],casoRegion[1],casoRegion[2],casoRegion[3])
    try:
        repository.patch(id, casoRegion, cursor)
    except Exception as error:
        print("Error PATCH a CASOS_POR_REGION: ", error)
    else:
        print("PATCH exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return