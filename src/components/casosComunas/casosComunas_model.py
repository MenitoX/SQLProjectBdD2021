class CasoComuna:
  codigo : str
  nombre : str
  casos  : int 
  def __init__(self, nombre, codigo, casos ):
    self.nombre = nombre
    self.codigo = codigo
    self.casos = int(casos)