from casosComunas_model import CasoComuna

def init(cursor):
    cursor.execute (
        """
            CREATE TABLE CASOS_POR_COMUNA(
                COMUNA VARCHAR2(50) NOT NULL,
                CODIGO_DE_COMUNA VARCHAR2(50) NOT NULL,
                CASOS_CONFIRMADOS NUMBER NOT NULL,
                PRIMARY KEY(CODIGO_DE_COMUNA)
            )
        """
    )
    print("Creada primera instancia de CASOS_POR_COMUNA")
    return

def post(casoComuna : CasoComuna, cursor):
    cursor.execute (
        """
        INSERT INTO
            CASOS_POR_COMUNA(COMUNA, CODIGO_DE_COMUNA, CASOS_CONFIRMADOS)
        VALUES
            (:1, :2, :3)
        """
        , (casoComuna.nombre, casoComuna.codigo, casoComuna.casos)
    )
    return