import sys
sys.path.append('src/models')

from casosRegiones_model import CasoRegion

# GENERAL: Implementados por el controlador, solo que en vez de la conexión reciben 
# el cursor y en vez de listas con nulos, el CasoRegion

def init(cursor):
    cursor.execute (
        """
            CREATE TABLE CASOS_POR_REGION(
                REGION NVARCHAR2(150) NOT NULL,
                CODIGO_DE_REGION VARCHAR(100) NOT NULL,
                POBLACION NUMBER(38,0) NOT NULL,
                CASOS_CONFIRMADOS NUMBER(38,0) NOT NULL,
                CODIGOS_COMUNAS VARCHAR2(1000) NOT NULL,
                CONSTRAINT PK_REGION PRIMARY KEY (CODIGO_DE_REGION, REGION)
            )
        """
    )
    return

def getById(id : str, cursor):
    casoRegion : CasoRegion = None
    cursor.execute(
        """
            SELECT *
            FROM CASOS_POR_REGION
            WHERE CODIGO_DE_REGION = CAST(:id AS VARCHAR(100))
        """
        ,[id] 
        )
    rList = list()
    for REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS, CODIGOS_COMUNAS in cursor:
        casoRegion = CasoRegion(REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS, CODIGOS_COMUNAS)
        rList.append(casoRegion)
    if len(rList) > 1:
        return rList
    else:
        return casoRegion

def getAll(cursor):
    casoRegion : CasoRegion = None
    cursor.execute(
        """
            SELECT *
            FROM CASOS_POR_REGION
        """
        )
    rList = list()
    for REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS, CODIGOS_COMUNAS in cursor:
        casoRegion = CasoRegion(REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS, CODIGOS_COMUNAS)
        rList.append(casoRegion)
    return rList

def post(casoRegion : CasoRegion, cursor):
    cursor.execute (
        """
        INSERT INTO
            CASOS_POR_REGION(REGION, CODIGO_DE_REGION, POBLACION, CASOS_CONFIRMADOS, CODIGOS_COMUNAS)
        VALUES
            (:1, :2, :3, :4, :5)
        """
        , (casoRegion.nombre, casoRegion.codigo, casoRegion.poblacion, casoRegion.casos, casoRegion.codigosComunas)
    )
    return

def delete(id : str, cursor):
    cursor.execute(
        """
        DELETE FROM CASOS_POR_REGION WHERE CODIGO_DE_REGION = CAST(:id AS VARCHAR(100))
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
            CASOS_CONFIRMADOS = NVL(:4, CASOS_CONFIRMADOS),
            CODIGOS_COMUNAS = NVL(:5, CODIGOS_COMUNAS)
        WHERE
            CODIGO_DE_REGION = :6
        """
        ,(casoRegion.nombre, casoRegion.poblacion, casoRegion.codigo, casoRegion.casos, casoRegion.codigosComunas, id)
    )
    return

# Trigger para actualizar la región donde se insertó la comuna
def triggerInsertComunas(cursor):
    cursor.execute(
        """
        CREATE OR REPLACE TRIGGER regiones_trigger_insert_comunas
        AFTER INSERT 
        ON CASOS_POR_COMUNA
        FOR EACH ROW
        BEGIN 
            UPDATE CASOS_POR_REGION
            SET
                POBLACION = POBLACION + :new.POBLACION,
                CASOS_CONFIRMADOS = CASOS_CONFIRMADOS + :new.CASOS_CONFIRMADOS
            WHERE INSTR(CODIGOS_COMUNAS, ','||:new.CODIGO_DE_COMUNA||',') > 0;
        END regiones_trigger_insert_comunas;
        """
    )
    return

# Trigger para actualizar la región donde se actualizó una comuna
def triggerUpdateComunas(cursor):
    cursor.execute(
        """
        CREATE OR REPLACE TRIGGER regiones_trigger_update_comunas
        AFTER UPDATE 
        ON CASOS_POR_COMUNA
        FOR EACH ROW
        DECLARE
            v_erase VARCHAR(100) := 'ERASE ME';
        BEGIN 
            UPDATE CASOS_POR_REGION
            SET
                POBLACION = POBLACION + :new.POBLACION - :old.POBLACION,
                CASOS_CONFIRMADOS = CASOS_CONFIRMADOS + :new.CASOS_CONFIRMADOS - :old.CASOS_CONFIRMADOS,
                CODIGO_DE_REGION = CASE WHEN ((CASOS_CONFIRMADOS + :new.CASOS_CONFIRMADOS - :old.CASOS_CONFIRMADOS) / (POBLACION + :new.POBLACION - :old.POBLACION)) > 0.15 then v_erase else CODIGO_DE_REGION end
            WHERE INSTR(CODIGOS_COMUNAS, ','||:new.CODIGO_DE_COMUNA||',') > 0;
        END regiones_trigger_update_comunas;
        """
    )
    return

# Borra poblacion, casos y codigo de la región donde se borro una comuna
def triggerDeleteComunas(cursor):
    cursor.execute(
        """
        CREATE OR REPLACE TRIGGER regiones_trigger_delete_comunas
        AFTER DELETE 
        ON CASOS_POR_COMUNA
        FOR EACH ROW
        BEGIN 
            UPDATE CASOS_POR_REGION
            SET
                POBLACION = POBLACION - :old.POBLACION,
                CASOS_CONFIRMADOS = CASOS_CONFIRMADOS - :old.CASOS_CONFIRMADOS,
                CODIGOS_COMUNAS = REPLACE(CODIGOS_COMUNAS,:old.CODIGO_DE_COMUNA||',','')  
            WHERE INSTR(CODIGOS_COMUNAS, ','||:old.CODIGO_DE_COMUNA||',') > 0;
        END regiones_trigger_delete_comunas;
        """
    )
    return

def viewRegion(cursor):
    cursor.execute(
        """
        CREATE OR REPLACE VIEW VIEW_REGION AS
            SELECT REGION, CASOS_CONFIRMADOS, CODIGO_DE_REGION FROM CASOS_POR_REGION
        """
    )
    return

def getView(cursor):
    cursor.execute(
        """
        SELECT * FROM VIEW_REGION
        """
    )
    rList = [[],[]]
    for i,j,z in cursor:
        rList[0].append(i+"("+z+")")
        rList[1].append(j)
    return rList