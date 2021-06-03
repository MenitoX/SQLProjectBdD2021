import sys
sys.path.append('src/components/casosComunas')
sys.path.append('src/components/casosRegiones')
sys.path.append('src/models/casosComunas_model')
sys.path.append('src/models/casosRegiones_model')

from casosComunas_model import CasoComuna
from casosRegiones_model import CasoRegion
import casosComunas_controller as controllerComunas
import casosRegiones_controller as controllerRegiones


def init(connection):
    controllerComunas.init(connection)
    controllerRegiones.init(connection)

# Postea una comuna a la base de datos
def crearComuna(connection):
    COMUNA = input("Nombre de la comuna : ")
    CODIGO_COMUNA = input("Codigo de la comuna : ")
    CODIGO_REGION = input("Codigo de la región de la comuna : ")
    POBLACION = input("Población de la comuna : ")
    
    # PATCH para añadir el código a la región para propio funcionamiento del trigger de updates
    casoRegion = controllerRegiones.getById(CODIGO_REGION, connection)
    newCodigos = casoRegion.codigosComunas + CODIGO_COMUNA + ","
    casoRegion = [None, None, None , None, newCodigos]
    controllerRegiones.patch(CODIGO_REGION, casoRegion, connection)

    # POST Comuna
    casoComuna = CasoComuna(COMUNA, CODIGO_COMUNA, POBLACION, 0)
    controllerComunas.post(casoComuna, connection)
    return

# Postea una región a la base de datos
def crearRegion(connection):
    REGION = input("Nombre de la region : ")
    CODIGO_REGION = input("Codigo de la región : ")
    casoRegion = CasoRegion(REGION, CODIGO_REGION, 0, 0, ",")
    controllerRegiones.post(casoRegion, connection)
    return

# Muestra la comuna indicada, o el registro completo en la view de comuna que 
# contiene la comuna y los casos confirmados
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

# Muestra la región indicada, o el registro completo en la view de regiones que 
# contiene la region y los casos confirmados
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

# Añade la n cantidad de casos ingresada
def addCasos(connection):
    id = input("Id de la comuna a la que desea sumar : ")
    casos = int(input("Casos que desea sumar : "))
    
    casoComuna = controllerComunas.getById(id, connection)
    nCasos = casoComuna.casos + casos
    
    casoComuna = [None, None, None, nCasos]
    controllerComunas.patch(id, casoComuna, connection)
    return

# Descuenta la n cantidad de casos ingresada
def lessCasos(connection):
    id = input("Id de la comuna a la que desea restar : ")
    casos = int(input("Casos que desea restar : "))
    
    casoComuna = controllerComunas.getById(id, connection)
    nCasos = casoComuna.casos - casos
    
    casoComuna = [None, None, None, nCasos]
    controllerComunas.patch(id, casoComuna, connection)
    return

# Busca los id's ERASE ME en la tabla para ser borrados y borra sus códigos de 
# comuna relacionados.
def checkErase(connection):    
    casoRegion = controllerRegiones.getById("ERASE ME", connection)
    if casoRegion:
        if isinstance(casoRegion, list):
            for i in casoRegion:
                positividad = round((i.casos / i.poblacion) * 100, 4)
                print("Se eliminará la comuna ",i.nombre, " con positividad de ",positividad,"%")
                codigos = i.codigosComunas.split(",")
                for codigo in codigos:
                    if codigo != ",":
                        controllerComunas.delete(codigo, connection)
        else:
            positividad = round((casoRegion.casos / casoRegion.poblacion) * 100, 4)
            print("Se eliminará la comuna ",casoRegion.nombre, " con positividad de ",positividad,"%")
            codigos = casoRegion.codigosComunas.split(",")
            for codigo in codigos:
                if codigo != ",":
                    controllerComunas.delete(codigo, connection)
    else:
        print("Nada que borrar")
    controllerRegiones.delete("ERASE ME", connection)
    return

# Muestra en consola las top 5 positividades de comunas, listTops almacena estos valores
# durante la ejecución
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

# Muestra en consola las top 5 positividades de regiones, listTops almacena estos valores
# durante la ejecución
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

# Función para mantener en memoria una lista con los top 5 valores
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

# Fusión de regiones
def fusionRegiones(connection):
    region1 = input("Codigo de la region 1: ")
    region2 = input("Codigo de la region 2: ")
    nombre = input("Nombre de la fusión : ")
    
    region1 = controllerRegiones.getById(region1, connection)
    region2 = controllerRegiones.getById(region2, connection)
    controllerRegiones.delete(region1.codigo, connection)
    controllerRegiones.delete(region2.codigo, connection)
    
    # Fix para las comunas que sean fusiones y estén en ambas regiones
    reguladorCasos = 0
    reguladorPoblacion = 0
    for codigo in region1.codigosComunas.split(","):
        if (','+codigo+',') in region2.codigosComunas:
            casoComuna = controllerComunas.getById(codigo, connection)
            reguladorCasos += casoComuna.casos
            reguladorPoblacion += casoComuna.poblacion

    # Nuevos valores
    casos = region1.casos + region2.casos - reguladorCasos
    poblacion = region1.poblacion + region2.poblacion - reguladorPoblacion
    codigoComunas = region1.codigosComunas + region2.codigosComunas[1::]
    
    # El nuevo codigo de region es la suma de los anteriores códigos
    codigoRegion = int(region1.codigo) + int(region2.codigo)
    
    # Comprobación para ver si el código está en uso, si está en uso es el mismo codigo + 1
    while controllerRegiones.getById(codigoRegion, connection):
        codigoRegion += 1
    
    casoRegion = CasoRegion(nombre, str(codigoRegion), poblacion, casos, codigoComunas)
    controllerRegiones.post(casoRegion, connection)
    return

def fusionComunas(connection):
    comuna1 = input("Codigo de la comuna 1: ")
    comuna2 = input("Codigo de la comuna 2: ")
    nombre = input("Nombre de la fusión : ")
    comuna1 = controllerComunas.getById(comuna1, connection)
    comuna2 = controllerComunas.getById(comuna2, connection)
    

    regionesPadres = []
    regiones = controllerRegiones.getAll(connection)
    breakPoint = 0
    # Verifica las regiones de las comunas ingresadas
    for region in regiones:
        CODIGO_DE_REGION = region.codigo 
        CODIGOS_COMUNAS = region.codigosComunas
        if breakPoint == 2:
            break
        if (','+comuna1.codigo+',') in CODIGOS_COMUNAS:
            regionesPadres.append([1,CODIGO_DE_REGION, CODIGOS_COMUNAS])
            breakPoint += 1
        elif (','+comuna2.codigo+',') in CODIGOS_COMUNAS:
            regionesPadres.append([2,CODIGO_DE_REGION, CODIGOS_COMUNAS])
            breakPoint += 1
    
    controllerComunas.delete(comuna1.codigo, connection)
    controllerComunas.delete(comuna2.codigo, connection)
    regionesPadres.sort()
    codigoFusion = comuna1.codigo+'-'+comuna2.codigo
    codigoRegion1 = regionesPadres[0][1]
    
    # Para que funcione si solo existe una región
    if len(regionesPadres) > 1:
        codigoRegion2 = regionesPadres[1][1]
    else:
        codigoRegion2 = codigoRegion1

    # Caso distintas regiones
    if codigoRegion1 != codigoRegion2:
        codigosComunas1 = regionesPadres[0][2]
        codigosComunas2 = regionesPadres[1][2]
        verificacion = input("""Las comunas forman parte de distintas regiones, desea
        que formen parte de la región 1, región 2 o ambas (1/2/3) : """)
        if verificacion == "1":
            nuevoCodigosComunas = codigosComunas1.replace(comuna1.codigo, codigoFusion)
            controllerRegiones.patch(codigoRegion1, [None, None, None, None, nuevoCodigosComunas], connection)
        elif verificacion == "2":
            nuevoCodigosComunas = codigosComunas2.replace(comuna2.codigo, codigoFusion)
            controllerRegiones.patch(codigoRegion2, [None, None, None, None, nuevoCodigosComunas], connection)
        else:
            nuevoCodigosComunas1 = codigosComunas1.replace(comuna1.codigo, codigoFusion)
            nuevoCodigosComunas2 = codigosComunas2.replace(comuna2.codigo, codigoFusion)
            controllerRegiones.patch(codigoRegion1, [None, None, None, None, nuevoCodigosComunas1], connection)
            controllerRegiones.patch(codigoRegion2, [None, None, None, None, nuevoCodigosComunas2], connection)
    # Caso mismas regiones
    else:
        codigoRegion = regionesPadres[0][1]
        codigosComunas = regionesPadres[0][2]
        nuevoCodigosComunas = codigosComunas.replace(comuna2.codigo+',', "")
        nuevoCodigosComunas = nuevoCodigosComunas.replace(comuna1.codigo, codigoFusion)
        controllerRegiones.patch(codigoRegion, [None, None, None, None, nuevoCodigosComunas], connection)
    
    # Post de la fusión
    fusionPoblacion = comuna1.poblacion + comuna2.poblacion
    fusionCasos = comuna1.casos + comuna2.casos
    casoComuna = CasoComuna(nombre, codigoFusion, fusionPoblacion, fusionCasos)
    controllerComunas.post(casoComuna, connection)
    return


        




