import os

import psycopg2

def get_connection():
    '''
    Retorna una conexión a la base de datos.

    Nota: debe ser cerrada posteriormente
    '''
    # Los datos de conexión se leen de variables de entorno (ver .env.example)
    # para no dejar credenciales escritas en el código
    try:
        conn = psycopg2.connect(dbname=os.getenv("DB_NAME", "blog"),
                                user=os.getenv("DB_USER", "postgres"),
                                password=os.getenv("DB_PASSWORD", ""),
                                host=os.getenv("DB_HOST", "localhost"),
                                port=os.getenv("DB_PORT", "5432"))

        # En Java (JDBC), por defecto las conexiones se crean con la opción
        # "autocommit = true". Esto quiere decir que cada sentencia SQL se
        # ejecuta en una transacción independiente y se acepta automáticamente.
        # En psycopg2, por defecto las conexiones se crean con la opción
        # "autocommit = false". Esto quiere decir que las sentencias SQL se
        # ejecutan en una transacción que debe ser confirmada explícitamente.
        # Por simplicidad, vamos a establecer autocommit a True para que
        # funcione como en Java.
        conn.autocommit = True

    except psycopg2.Error as e:
        # Mostramos el problema y relanzamos la excepción: si no, se devolvería
        # una variable 'conn' sin asignar (UnboundLocalError)
        print("ERROR:\n{0}".format(e))
        raise

    return conn
