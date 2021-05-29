from casosComunas_model import CasoComuna
import casosRegiones_repository as repository
import casosComunas_controller as controllerComunas
from casosRegiones_model import CasoRegion

#REGION, CODIGO REGION, POBLACION, CASOS 

def init(connection):
    cursor = connection.cursor()
    # For dev, comment if initialized
    repository.init(cursor)
    # Trigger and View initialization
    trigger(connection)
    viewRegion(connection)
    try:
        file = open("src\\templates\\RegionesComunas.csv", "r", encoding='utf-8')
        firstLine = True
        Regiones = list()
        for i in file:
            if firstLine:
                firstLine = False
                continue
            NOMBRE, CODIGO_REGION, CODIGO_COMUNA  = i.strip("\n").split(",")
            if NOMBRE not in Regiones:
                casoComuna : CasoComuna = controllerComunas.getById(CODIGO_COMUNA, connection)
                if casoComuna:
                    CODIGO_COMUNA = ',' + CODIGO_COMUNA + ','
                    casoRegion = CasoRegion(NOMBRE, CODIGO_REGION, casoComuna.poblacion, casoComuna.casos, CODIGO_COMUNA)
                    post(casoRegion, connection)
                Regiones.append(NOMBRE)
            else:
                casoRegion : CasoRegion = getById(CODIGO_REGION, connection)
                casoComuna : CasoComuna = controllerComunas.getById(CODIGO_COMUNA, connection)
                if casoComuna:
                    newCasos = casoComuna.casos + casoRegion.casos
                    newPoblacion = casoComuna.poblacion + casoRegion.poblacion
                    newCodigos = casoRegion.codigosComunas + CODIGO_COMUNA + ','  
                    patch(CODIGO_REGION, [None, None, newPoblacion, newCasos, newCodigos], connection)
        # Check de positividad post-inicialización
        casosRegiones = getAll(connection)
        for i in casosRegiones:
            if i.casos/i.poblacion > 0.15:
                patch(i.codigo, [None, "ERASE ME", None, None, None], connection)
    except Exception as error:
        print("No se pudo inicializar CASOS_POR_REGION en base al csv: ", error)
    else:
        print("Primera inicializacion de CASOS_POR_REGION finalizada en base a archivo csv")
        connection.commit()
    finally:
        file.close()
        cursor.close()
        return

def getById(id : str, connection):
    cursor = connection.cursor()
    casoRegion : CasoRegion = None
    try:
        casoRegion = repository.getById(id, cursor)
    except Exception as error:
        print("Error GET a CASOS_POR_REGION: ", error)
        return 
    else:
        print("GET exitoso a CASOS_POR_REGION")
    finally:
        cursor.close()
        return casoRegion

def getAll(connection):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getAll(cursor)
    except Exception as error:
        print("Error al recuperar los datos de CASOS_POR_REGION: ", error)
    else:
        print("Consulta de casos en CASOS_POR_REGION realizada con éxito")
    finally:
        cursor.close()
        return rList

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
    casoRegion = CasoRegion(casoRegion[0],casoRegion[1],casoRegion[2],casoRegion[3], casoRegion[4])
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

# Setea los triggers declarados
def trigger(connection):
    cursor  = connection.cursor()
    try:
        repository.triggerInsertComunas(cursor)
        repository.triggerUpdateComunas(cursor)
        repository.triggerDeleteComunas(cursor)
    except Exception as error:
        print("Error al crear los triggers de CASOS_POR_REGION: ", error)
    else:
        print("Creación de triggers exitosa para CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

def viewRegion(connection):
    cursor  = connection.cursor()
    try:
        repository.viewRegion(cursor)
    except Exception as error:
        print("Error al crear la view de CASOS_POR_REGION: ", error)
    else:
        print("Creación de view exitosa para CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

def getView(connection):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getView(cursor)
    except Exception as error:
        print("Error al crear la view de CASOS_POR_REGION: ", error)
    else:
        print("Creación de view exitosa para CASOS_POR_REGION")
    finally:
        cursor.close()
        return rList