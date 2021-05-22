import sys
sys.path.append('src/components/casosComunas')
sys.path.append('src/components/casosRegiones')
sys.path.append('src/models/casosComunas_model')
sys.path.append('src/models/casosRegiones_model')

from casosComunas_model import CasoComuna
from casosRegiones_model import CasoRegion
import casosComunas_controller as controllerComunas
import casosRegiones_controller as controllerRegiones


def crearComuna(connection):
    COMUNA = input("Nombre de la comuna : ")
    CODIGO_COMUNA = input("Codigo de la comuna : ")
    CODIGO_REGION = input("Codigo de la región de la comuna : ")
    POBLACION = input("Población de la comuna : ")

    # POST Comuna
    casoComuna = CasoComuna(COMUNA, CODIGO_COMUNA, POBLACION, 0)
    controllerComunas.post(casoComuna, connection)
    
    # PATCH Region para añadir el nuevo codigo y la poblacion  
    casoRegion = controllerRegiones.getById(CODIGO_REGION, connection)
    newPoblacion = casoComuna.poblacion + casoRegion.poblacion
    newCodigos = casoRegion.codigosComunas + CODIGO_COMUNA + ","
    casoRegion = [None, None, newPoblacion , None, newCodigos]
    controllerRegiones.patch(CODIGO_REGION, casoRegion, connection)
    return

def crearRegion(connection):
    REGION = input("Nombre de la comuna : ")
    CODIGO_REGION = input("Codigo de la región de la comuna : ")
    casoRegion = CasoRegion(REGION, CODIGO_REGION, 0, 0, "")
    controllerRegiones.post(casoRegion, connection)
    return

def verCasosComunas(connection):
    id = input("Id de la comuna que quiere ver / No responda nada si desea el registro completo : ")
    print("Comuna | Casos Confirmados")
    if id != "":
        casosComunas = controllerComunas.getById(id, connection)
        print(casosComunas.nombre,"  ",casosComunas.casos)
    else:
        casosComunas = controllerComunas.getView(connection)
        for i in range(len(casosComunas[0])):
            while len(casosComunas[0][i]) < 25:
                casosComunas[0][i] = casosComunas[0][i] + " "
            print(casosComunas[0][i],"  ",casosComunas[1][i])
    return

def verCasosRegiones(connection):
    id = input("Id de la Region que quiere ver / No responda nada si desea el registro completo : ")
    print("Region | Casos Confirmados")
    if id != "":
        casosRegiones = controllerRegiones.getById(id, connection)
        print(casosRegiones.nombre,"  ",casosRegiones.casos)
    else:
        casosRegiones = controllerRegiones.getView(connection)
        for i in range(len(casosRegiones[0])):
            while len(casosRegiones[0][i]) < 25:
                casosRegiones[0][i] = casosRegiones[0][i] + " "
            print(casosRegiones[0][i],"  ",casosRegiones[1][i])
    return

def addCasos(connection):
    id = input("Id de la comuna a la que desea sumar : ")
    casos = int(input("Casos que desea sumar : "))
    
    casoComuna = controllerComunas.getById(id, connection)
    nCasos = casoComuna.casos + casos
    
    casoComuna = [None, None, None, nCasos]
    controllerComunas.patch(id, casoComuna, connection)
    return

def lessCasos(connection):
    id = input("Id de la comuna a la que desea restar : ")
    casos = int(input("Casos que desea restar : "))
    
    casoComuna = controllerComunas.getById(id, connection)
    nCasos = casoComuna.casos - casos
    
    casoComuna = [None, None, None, nCasos]
    controllerComunas.patch(id, casoComuna, connection)
    return

# Busca los id's ERASE ME en la tabla para ser borrados
def checkErase(connection):    
    casoRegion = controllerRegiones.getById("ERASE ME", connection)
    if casoRegion:
        if isinstance(casoRegion, list):
            for i in casoRegion:
                positividad = round((i.casos / i.poblacion) * 100, 4)
                print("Se eliminará la comuna ",i.nombre, " con positividad de ",positividad,"%")
        else:
            positividad = round((casoRegion.casos / casoRegion.poblacion) * 100, 4)
            print("Se eliminará la comuna ",casoRegion.nombre, " con positividad de ",positividad,"%")
    else:
        print("Nada que borrar")
    controllerRegiones.delete("ERASE ME", connection)
    return

def checkTopComunas(connection):
    listaTops = list()
    casosComunas = controllerComunas.getAll(connection)
    
    for caso in casosComunas:
        positividad = round((caso.casos/caso.poblacion)*100, 2)
        listaTops = checkTopAuxiliar(listaTops, [caso.nombre, positividad])
    print("Las comunas con TOP contagios son :")
    print("    Comuna          |    Contagios       ")
    for i,j in listaTops:
        while len(i) < 26:
            i = i + " "
        print(i, j)
    return        

def checkTopRegiones(connection):
    listaTops = list()
    casosRegiones = controllerRegiones.getAll(connection)
    
    for caso in casosRegiones:
        positividad = round((caso.casos/caso.poblacion)*100, 2)
        listaTops = checkTopAuxiliar(listaTops, [caso.nombre, positividad])
    print("Las regiones con TOP contagios son :")
    print("    Region          |    Contagios       ")
    for i,j in listaTops:
        while len(i) < 26:
            i = i + " "
        print(i, j)
    return

def checkTopAuxiliar(lista : list() , caso : list()):
    lenLista = len(lista)
    if lenLista == 0:
        lista.append(caso)
    
    elif lenLista < 5:
        for i in range(lenLista):
            if caso[1] > lista[i][1]:
                lista.insert(i, caso)
                break
        newLen = len(lista)
        if newLen == lenLista:
            lista.append(caso)
    
    else:
        for i in range(lenLista):
            if caso[1] > lista[i][1]:
                lista.insert(i, caso)
                break
        if len(lista) > 5:
            lista.pop()
    return lista

        




