import sys
sys.path.append('src/models')

from casosComunas_model import CasoComuna

def init(cursor):
    cursor.execute (
        """
            CREATE TABLE CASOS_POR_COMUNA(
                COMUNA NVARCHAR2(150) NOT NULL,
                CODIGO_DE_COMUNA NVARCHAR2(50) NOT NULL,
                POBLACION NUMBER(38,0) NOT NULL,
                CASOS_CONFIRMADOS NUMBER(38,0) NOT NULL,
                CONSTRAINT PK_COMUNA PRIMARY KEY (CODIGO_DE_COMUNA, COMUNA)
            )
        """
    )
    return

def getById(id : str, cursor):
    casoComuna : CasoComuna = None
    cursor.execute(
        """
            SELECT *
            FROM CASOS_POR_COMUNA
            WHERE CODIGO_DE_COMUNA = :id
        """
        ,[id] 
        )
    for COMUNA, CODIGO_DE_COMUNA, POBLACION, CASOS_CONFIRMADOS in cursor:
        casoComuna = CasoComuna(COMUNA, CODIGO_DE_COMUNA, POBLACION, CASOS_CONFIRMADOS)
    return casoComuna

def getAll(cursor):
    casoComuna : CasoComuna = None
    cursor.execute(
        """
            SELECT *
            FROM CASOS_POR_COMUNA
        """
        )
    rList = list()
    for COMUNA, CODIGO_DE_COMUNA, POBLACION, CASOS_CONFIRMADOS in cursor:
        casoComuna = CasoComuna(COMUNA, CODIGO_DE_COMUNA, POBLACION, CASOS_CONFIRMADOS)
        rList.append(casoComuna)
    return rList

def post(casoComuna : CasoComuna, cursor):
    cursor.execute (
        """
        INSERT INTO
            CASOS_POR_COMUNA(COMUNA, CODIGO_DE_COMUNA, POBLACION, CASOS_CONFIRMADOS)
        VALUES
            (:1, :2, :3, :4)
        """
        , (casoComuna.nombre, casoComuna.codigo, casoComuna.poblacion, casoComuna.casos)
    )
    return

def delete(id : str, cursor):
    cursor.execute(
        """
        DELETE FROM CASOS_POR_COMUNA WHERE CODIGO_DE_COMUNA = :id
        """
        ,[id]
    )
    return

def patch(id : str, casoComuna : CasoComuna, cursor):
    cursor.execute(
        """
        UPDATE CASOS_POR_COMUNA
        SET
            COMUNA = NVL(:1, COMUNA),
            POBLACION = NVL(:2, POBLACION),
            CODIGO_DE_COMUNA = NVL(:3, CODIGO_DE_COMUNA),
            CASOS_CONFIRMADOS = NVL(:4, CASOS_CONFIRMADOS)
        WHERE
            CODIGO_DE_COMUNA = :5
        """
        ,(casoComuna.nombre, casoComuna.poblacion, casoComuna.codigo, casoComuna.casos, id)
    )
    return

def viewComuna(cursor):
    cursor.execute(
        """
        CREATE OR REPLACE VIEW VIEW_COMUNA AS
            SELECT COMUNA, CASOS_CONFIRMADOS, CODIGO_DE_COMUNA FROM CASOS_POR_COMUNA
        """
    )
    return

def getView(cursor):
    cursor.execute(
        """
        SELECT * FROM VIEW_COMUNA
        """
    )
    rList = [[],[]]
    for i,j,z in cursor:
        rList[0].append(i+"("+z+")")
        rList[1].append(j)
    return rList