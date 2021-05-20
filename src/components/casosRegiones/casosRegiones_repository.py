import sys
sys.path.append('src/models')

from casosRegiones_model import CasoRegion

def init(cursor):
    cursor.execute (
        """
            CREATE TABLE CASOS_POR_REGION(
                REGION VARCHAR2(50) NOT NULL,
                CODIGO_DE_REGION VARCHAR2(50) NOT NULL,
                POBLACION NUMBER NOT NULL,
                CASOS_CONFIRMADOS NUMBER NOT NULL,
                PRIMARY KEY(CODIGO_DE_REGION)
            )
        """
    )
    print("Creada primera instancia de CASOS_POR_REGION")
    return

def get(id : str, cursor):
    casoRegion : CasoRegion = None
    cursor.execute(
        """
            SELECT *
            FROM CASOS_POR_REGION
            WHERE CODIGO_DE_REGION = :id
        """
        ,[id] 
        )
    for REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS in cursor:
        casoRegion = CasoRegion(REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS)
    return casoRegion

def post(casoRegion : CasoRegion, cursor):
    cursor.execute (
        """
        INSERT INTO
            CASOS_POR_REGION(REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS)
        VALUES
            (:1, :2, :3, :4)
        """
        , (casoRegion.nombre, casoRegion.codigo, casoRegion.poblacion, casoRegion.casos)
    )
    return

def delete(id : str, cursor):
    cursor.execute(
        """
        DELETE FROM CASOS_POR_REGION WHERE CODIGO_DE_REGION = :id
        """
        ,[id]
    )
    return

def patch(id : str, casoRegion : CasoRegion, cursor):
    cursor.execute(
        """
        UPDATE CASOS_POR_REGION
        SET
            REGION = NVL(:1, REGION),
            POBLACION = NVL(:2, POBLACION),
            CODIGO_DE_REGION = NVL(:3, CODIGO_DE_REGION),
            CASOS_CONFIRMADOS = NVL(:4, CASOS_CONFIRMADOS)
        WHERE
            CODIGO_DE_REGION = :5
        """
        ,(casoRegion.nombre, casoRegion.poblacion, casoRegion.codigo, casoRegion.casos, id)
    )
    return