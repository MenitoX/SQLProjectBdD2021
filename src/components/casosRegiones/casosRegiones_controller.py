from casosComunas_model import CasoComuna
import casosRegiones_repository as repository
import casosComunas_controller as controllerComunas
from casosRegiones_model import CasoRegion

#REGION, CODIGO REGION, POBLACION, CASOS 

# Inicializa la tabla de Regiones. Recibe la conexión a oracle y un bool debug
def init(connection, DEBUG = False):
    cursor = connection.cursor()
    # For dev, comment if initialized
    if initAux(cursor, DEBUG):
        return
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
                casoComuna : CasoComuna = controllerComunas.getById(CODIGO_COMUNA, connection, DEBUG)
                if casoComuna:
                    CODIGO_COMUNA = ',' + CODIGO_COMUNA + ','
                    casoRegion = CasoRegion(NOMBRE, CODIGO_REGION, casoComuna.poblacion, casoComuna.casos, CODIGO_COMUNA)
                    post(casoRegion, connection)
                Regiones.append(NOMBRE)
            else:
                casoRegion : CasoRegion = getById(CODIGO_REGION, connection, DEBUG)
                casoComuna : CasoComuna = controllerComunas.getById(CODIGO_COMUNA, connection, DEBUG)
                if casoComuna:
                    newCasos = casoComuna.casos + casoRegion.casos
                    newPoblacion = casoComuna.poblacion + casoRegion.poblacion
                    newCodigos = casoRegion.codigosComunas + CODIGO_COMUNA + ','  
                    patch(CODIGO_REGION, [None, None, newPoblacion, newCasos, newCodigos], connection, DEBUG)
        # Check de positividad post-inicialización
        casosRegiones = getAll(connection)
        for i in casosRegiones:
            if i.casos/i.poblacion > 0.15:
                patch(i.codigo, [None, "ERASE ME", None, None, None], connection, DEBUG)
    except Exception as error:
        if DEBUG:
            print("No se pudo inicializar CASOS_POR_REGION en base al csv: ", error)
    else:
        if DEBUG:
            print("Primera inicializacion de CASOS_POR_REGION finalizada en base a archivo csv")
        connection.commit()
    finally:
        file.close()
        cursor.close()
        return

# Auxiliar de inicialización de la tabla, que la crea. Recibe un cursor y el bool debug
def initAux(cursor, DEBUG = False):
    try:
        repository.init(cursor)
    except Exception as error:
        if DEBUG:
            print("No se pudo crear la tabla CASOS_POR_REGION : ", error)
        bool = True
    else:
        if DEBUG:
            print("Creada tabla CASOS_POR_REGION")
        bool = False
    finally:
        return bool

# Busca una región por código de comuna, recibe el código, la conexión a oracle y un bool debug
def getById(id : str, connection, DEBUG = False):
    cursor = connection.cursor()
    casoRegion : CasoRegion = None
    try:
        casoRegion = repository.getById(id, cursor)
    except Exception as error:
        if DEBUG:
            print("Error GET a CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("GET exitoso a CASOS_POR_REGION")
    finally:
        cursor.close()
        return casoRegion

# Retorna todas las regiones, recibe la conexión a oracle y un bool debug
def getAll(connection, DEBUG = False):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getAll(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al recuperar los datos de CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("Consulta de casos en CASOS_POR_REGION realizada con éxito")
    finally:
        cursor.close()
        return rList

# Método POST de regiones, recibe una clase CasoRegion, la conexión y un bool debug
def post(casoRegion : CasoRegion, connection, DEBUG = False):
    cursor = connection.cursor()
    try:
        repository.post(casoRegion, cursor)
    except Exception as error:
        if DEBUG:
            print("Error POST a CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("POST exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

# Método DELETE de regiones, recibe un codigo de comuna, la conexión y un bool debug    
def delete(id : str, connection, DEBUG = False):
    cursor = connection.cursor()
    try:
        repository.delete(id, cursor)
    except Exception as error:
        if DEBUG:
            print("Error DELETE a CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("DELETE exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

# Método PATCH de regiones, recibe un codigo de region, una lista con los atributos de CasoRegion,
# siendo nulos los campos que no se desea actualizar, la conexión y un bool debug
def patch(id :str, casoRegion : list(), connection, DEBUG = False):
    cursor = connection.cursor()
    casoRegion = CasoRegion(casoRegion[0],casoRegion[1],casoRegion[2],casoRegion[3], casoRegion[4])
    try:
        repository.patch(id, casoRegion, cursor)
    except Exception as error:
        if DEBUG:
            print("Error PATCH a CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("PATCH exitoso a CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

# Setea los triggers declarados, recibe la conexión y un bool debug
def trigger(connection, DEBUG = False):
    cursor  = connection.cursor()
    try:
        repository.triggerInsertComunas(cursor)
        repository.triggerUpdateComunas(cursor)
        repository.triggerDeleteComunas(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al crear los triggers de CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("Creación de triggers exitosa para CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

# Crea la view de regiones, recibe la conexión y un bool debug
def viewRegion(connection, DEBUG = False):
    cursor  = connection.cursor()
    try:
        repository.viewRegion(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al crear la view de CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("Creación de view exitosa para CASOS_POR_REGION")
        connection.commit()
    finally:
        cursor.close()
        return

# Retorna los valores de la view de regiones, recibe la conexión y un bool debug
def getView(connection, DEBUG = False):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getView(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al crear la view de CASOS_POR_REGION: ", error)
    else:
        if DEBUG:
            print("Creación de view exitosa para CASOS_POR_REGION")
    finally:
        cursor.close()
        return rList