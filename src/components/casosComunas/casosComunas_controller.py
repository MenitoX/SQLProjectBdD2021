import casosComunas_repository as repository
from casosComunas_model import CasoComuna

def init(connection):
    cursor = connection.cursor()
    # For dev, comment if initialized
    repository.init(cursor)
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
        print("No se pudo inicializar CASOS_POR_COMUNA en base al csv: ", error)
    else:
        print("Primera inicializacion de CASOS_POR_COMUNA finalizada en base a archivo csv")
        connection.commit()
    finally:
        file.close()
        cursor.close()
        return

def getById(id : str, connection):
    cursor = connection.cursor()
    casoComuna : CasoComuna = None
    try:
        casoComuna = repository.getById(id, cursor)
    except Exception as error:
        print("Error GET a CASOS_POR_COMUNA: ", error)
    else:
        print("GET exitoso a CASOS_POR_COMUNA")
    finally:
        cursor.close()
        return casoComuna

def getAll(connection):
    cursor  = connection.cursor()
    rList = None
    try:
        rList = repository.getAll(cursor)
    except Exception as error:
        print("Error al recuperar los datos de CASOS_POR_COMUNA: ", error)
    else:
        print("Consulta de casos en CASOS_POR_COMUNA realizada con éxito")
    finally:
        cursor.close()
        return rList

def post(casoComuna : CasoComuna, connection):
    cursor = connection.cursor()
    try:
        repository.post(casoComuna, cursor)
    except Exception as error:
        print("Error POST a CASOS_POR_COMUNA: ", error)
    else:
        print("POST exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

def delete(id : str, connection):
    cursor = connection.cursor()
    try:
        repository.delete(id, cursor)
    except Exception as error:
        print("Error DELETE a CASOS_POR_COMUNA: ", error)
    else:
        print("DELETE exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

def patch(id :str, casoComuna : list(), connection):
    cursor = connection.cursor()
    casoComuna = CasoComuna(casoComuna[0],casoComuna[1],casoComuna[2],casoComuna[3])
    try:
        repository.patch(id, casoComuna, cursor)
    except Exception as error:
        print("Error PATCH a CASOS_POR_COMUNA: ", error)
    else:
        print("PATCH exitoso a CASOS_POR_COMUNA")
        connection.commit()
    finally:
        cursor.close()
        return

def viewComuna(connection):
    cursor  = connection.cursor()
    try:
        repository.viewComuna(cursor)
    except Exception as error:
        print("Error al crear la view de CASOS_POR_COMUNA: ", error)
    else:
        print("Creación de view exitosa para CASOS_POR_COMUNA")
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
        print("Error de GET a la view de CASOS_POR_COMUNA: ", error)
    else:
        print("GET de view exitosa para CASOS_POR_COMUNA")
    finally:
        cursor.close()
        return rList