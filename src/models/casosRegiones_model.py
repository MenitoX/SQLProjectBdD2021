class CasoRegion:
    nombre : str
    codigo: str
    casos: int
    poblacion : int
    codigosComunas : str
    def __init__(self, nombre = None, codigo = None, poblacion = None, casos = None, codigosComunas = None):
        self.nombre = nombre
        self.codigo = codigo
        if casos:
            self.casos = int(casos)
        else:
            self.casos = casos

        if poblacion:
            self.poblacion = int(poblacion)
        else:
            self.poblacion = poblacion

        self.codigosComunas = codigosComunas 

