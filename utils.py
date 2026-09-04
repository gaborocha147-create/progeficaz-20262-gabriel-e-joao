from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv('.cred')

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=os.getenv("MYSQL_PORT"),
        ssl_ca=os.getenv("MYSQL_CA")
    )
    
def get_imoveis(cidade=None, tipo=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM imoveis"
    params = []
    
    if cidade:
        query += " WHERE cidade = %s"
        params.append(cidade)
        
    if tipo:
        if "WHERE" in query:
            query += " AND tipo = %s"
        else:
            query += " WHERE tipo = %s"
        params.append(tipo)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    conn.close()
    
    imoveis = []
    for row in rows:
        imoveis.append({
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": float(row[7]),
            "data_aquisicao": str(row[8])
        })
        
    return imoveis

def get_imovel(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM imoveis WHERE id = %s", (imovel_id,)
    )

    row = cursor.fetchone()

    conn.close()
    
    if not row:
        return None
    
    return {
        "id": row[0],
        "logradouro": row[1],
        "tipo_logradouro": row[2],
        "bairro": row[3],
        "cidade": row[4],
        "cep": row[5],
        "tipo": row[6],
        "valor": float(row[7]),
        "data_aquisicao": str(row[8])
    }
    
def create_imovel(data):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO imoveis
    (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        data["logradouro"],
        data["tipo_logradouro"],
        data["bairro"],
        data["cidade"],
        data["cep"],
        data["tipo"],
        data["valor"],
        data["data_aquisicao"]
    ))

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return new_id

def update_imovel(imovel_id, data):
    conn = connect_db()
    cursor = conn.cursor()

    query = "UPDATE imoveis SET "
    fields = []
    params = []

    for key, value in data.items():
        fields.append(f"{key} = %s")
        params.append(value)

    query += ", ".join(fields)
    query += " WHERE id = %s"

    params.append(imovel_id)

    cursor.execute(query, params)

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated

def delete_imovel(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM imoveis WHERE id = %s",
        (imovel_id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted