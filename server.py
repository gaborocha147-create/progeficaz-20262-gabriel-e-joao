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


@server.route('/imoveis/<int:imovel_id>', methods=['GET'])
def get_imovel(imovel_id):
    """GET /imoveis/<id> - Retorna um imóvel específico pelo ID."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            return jsonify({"erro": "Imóvel não encontrado"}), 404
        
        imovel = converter_para_dict(resultado)
        
        cursor.close()
        conn.close()
        
        return jsonify(imovel), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@server.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    """POST /imoveis - Adiciona um novo imóvel."""
    try:
        dados = request.get_json()
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dados['logradouro'],
            dados['tipo_logradouro'],
            dados['bairro'],
            dados['cidade'],
            dados['cep'],
            dados['tipo'],
            dados['valor'],
            dados['data_aquisicao']
        ))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"mensagem": "Imóvel adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@server.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def deletar_imovel(imovel_id):
    """DELETE /imoveis/<id> - Deleta um imóvel específico pelo ID."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"erro": "Imóvel não encontrado"}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({"mensagem": "Imóvel deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@server.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    """PUT /imoveis/<id> - Atualiza um imóvel específico pelo ID."""
    try:
        dados = request.get_json()
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE imoveis
            SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s
            WHERE id = %s
        """, (
            dados['logradouro'],
            dados['tipo_logradouro'],
            dados['bairro'],
            dados['cidade'],
            dados['cep'],
            dados['tipo'],
            dados['valor'],
            dados['data_aquisicao'],
            imovel_id
        ))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"erro": "Imóvel não encontrado"}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({"mensagem": "Imóvel atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@server.route('/imoveis/search', methods=['GET'])
def buscar_imoveis():
    """GET /imoveis/search - Busca imóveis com base em parâmetros de consulta."""
    try:
        params = request.args
        query = "SELECT * FROM imoveis WHERE 1=1"
        values = []

        if 'cidade' in params:
            query += " AND cidade = %s"
            values.append(params['cidade'])
        if 'bairro' in params:
            query += " AND bairro = %s"
            values.append(params['bairro'])
        if 'tipo' in params:
            query += " AND tipo = %s"
            values.append(params['tipo'])

        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute(query, tuple(values))
        resultados = cursor.fetchall()
        
        imoveis = [converter_para_dict(row) for row in resultados]
        
        cursor.close()
        conn.close()
        
        return jsonify(imoveis), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    server.run(debug=True)
    