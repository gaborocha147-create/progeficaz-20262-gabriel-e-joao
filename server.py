from flask import Flask, render_template_string, request, redirect, jsonify
import json
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

server = Flask(__name__)

config = server.config
test_client = server.test_client

def conectar_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

def converter_para_dict(cursor_result):
    """Converte resultado do cursor em dicionário pra poder virar json."""
    if cursor_result is None:
        return None
    
    columns = ['id', 'logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor', 'data_aquisicao']
    return dict(zip(columns, cursor_result))

@server.route('/')
def pagina_imoveis():
    return render_template_string('''
        <p>Servidor rodando...</p>
        <p>Acesse /imoveis para acessar a API.</p>
    ''')

@server.route('/imoveis', methods=['GET'])
def get_imoveis():
    """GET /imoveis - Lista todos os imóveis."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM imoveis")
        resultados = cursor.fetchall()
        
        imoveis = [converter_para_dict(row) for row in resultados]
        
        cursor.close()
        conn.close()
        
        return jsonify(imoveis), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500