import casosComunas_repository as repository
from casosComunas_model import CasoComuna

# Inicializa la tabla de Comunas. Recibe la conexión a oracle y un bool debug
def init(connection, DEBUG = False):
    cursor = connection.cursor()
    # For dev, comment if initialized
    if initAux(cursor, DEBUG):
        return
    # View initialization
    viewComuna(connection)
    try:
        file = open("src\\templates\\CasosConfirmadosPorComuna.csv", "r", encoding='utf-8')
        firstLine = True
        for i in file:
            if firstLine:
                firstLine = False
                continue
            NOMBRE, CODIGO, POBLACION, CASOS = i.strip("\n").split(",")
            casoComuna = CasoComuna(NOMBRE, CODIGO, POBLACION, CASOS)
            repository.post(casoComuna, cursor)
    except Exception as error:
        if DEBUG:
            print("No se pudo inicializar CASOS_POR_COMUNA en base al csv: ", error)
    else:
        if DEBUG:
            print("Primera inicializacion de CASOS_POR_COMUNA finalizada en base a archivo csv")
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
            print("No se pudo crear la tabla CASOS_POR_COMUNA : ", error)
        bool = True
    else:
        bool = False
    finally:
        return bool

# Busca una comuna por código de comuna, recibe el código, la conexión a oracle y un bool debug
def getById(id : str, connection, DEBUG = False):
    cursor = connection.cursor()
    casoComuna : CasoComuna = None
    try:
        casoComuna = repository.getById(id, cursor)
    except Exception as error:
        if DEBUG:
            print("Error GET a CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("GET exitoso a CASOS_POR_COMUNA")
    finally:
        cursor.close()
        return casoComuna

# Retorna todas las comunas, recibe la conexión a oracle y un bool debug
def getAll(connection, DEBUG = False):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getAll(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al recuperar los datos de CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("Consulta de casos en CASOS_POR_COMUNA realizada con éxito")
    finally:
        cursor.close()
        return rList

# Método POST de comunas, recibe una clase CasoComuna, la conexión y un bool debug
def post(casoComuna : CasoComuna, connection, DEBUG = False):
    cursor = connection.cursor()
    try:
        repository.post(casoComuna, cursor)
    except Exception as error:
        if DEBUG:
            print("Error POST a CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("POST exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

# Método DELETE de comunas, recibe un codigo de comuna, la conexión y un bool debug
def delete(id : str, connection, DEBUG = False):
    cursor = connection.cursor()
    try:
        repository.delete(id, cursor)
    except Exception as error:
        if DEBUG:
            print("Error DELETE a CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("DELETE exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

# Método PATCH de comunas, recibe un codigo de comuna, una lista con los atributos de CasoComuna,
# siendo nulos los campos que no se desea actualizar, la conexión y un bool debug
def patch(id :str, casoComuna : list(), connection, DEBUG = False):
    cursor = connection.cursor()
    casoComuna = CasoComuna(casoComuna[0],casoComuna[1],casoComuna[2],casoComuna[3])
    try:
        repository.patch(id, casoComuna, cursor)
    except Exception as error:
        if DEBUG:
            print("Error PATCH a CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("PATCH exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

# Crea la view de comuna, recibe la conexión y un bool debug
def viewComuna(connection, DEBUG = False):
    cursor  = connection.cursor()
    try:
        repository.viewComuna(cursor)
    except Exception as error:
        if DEBUG:
            print("Error al crear la view de CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("Creación de view exitosa para CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

# Retorna los valores de la view de comuna, recibe la conexión y un bool debug
def getView(connection, DEBUG = False):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getView(cursor)
    except Exception as error:
        if DEBUG:
            print("Error de GET a la view de CASOS_POR_COMUNA: ", error)
    else:
        if DEBUG:
            print("GET de view exitosa para CASOS_POR_COMUNA")
    finally:
        cursor.close()
        return rList