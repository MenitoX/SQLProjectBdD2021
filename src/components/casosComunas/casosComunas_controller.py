import casosComunas_repository as repository
from casosComunas_model import CasoComuna

def init(connection):
    cursor = connection.cursor()
    # For dev, comment if initialized
    repository.init(cursor)
    try:
        file = open("src\\templates\\CasosConfirmadosPorComuna.csv", "r")
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

def get(id : str, connection):
    cursor = connection.cursor()
    casoComuna : CasoComuna = None
    try:
        casoComuna = repository.get(id, cursor)
    except Exception as error:
        print("Error GET a CASOS_POR_COMUNA: ", error)
        return 
    else:
        print("GET exitoso a CASOS_POR_COMUNA")
    finally:
        cursor.close()
        return casoComuna

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