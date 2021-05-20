class CasoComuna:
  nombre : str
  codigo : str
  poblacion : int
  casos  : int 
  def __init__(self, nombre = None, codigo = None, poblacion = None, casos = None):
    self.nombre = nombre
    self.codigo = codigo
    
    if poblacion:
      self.poblacion = int(poblacion)
    else:
      self.poblacion = poblacion
    
    if casos:
      self.casos = int(casos)
    else:
      self.casos = casos