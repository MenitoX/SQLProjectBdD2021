import sys
sys.path.append('src/models')

from casosComunas_model import CasoComuna

def init(cursor):
    cursor.execute (
        """
            CREATE TABLE CASOS_POR_COMUNA(
                COMUNA VARCHAR2(50) NOT NULL,
                CODIGO_DE_COMUNA VARCHAR2(50) NOT NULL,
                POBLACION NUMBER NOT NULL,
                CASOS_CONFIRMADOS NUMBER NOT NULL,
                PRIMARY KEY(CODIGO_DE_COMUNA)
            )
        """
    )
    print("Creada primera instancia de CASOS_POR_COMUNA")
    return

def get(id : str, cursor):
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