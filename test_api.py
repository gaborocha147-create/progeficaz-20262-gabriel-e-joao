import pytest
from flask import Flask, jsonify
import json
from unittest.mock import MagicMock, Mock, patch
import server

MOCK_IMOVEIS = [
    {
        "id": 1,
        "logradouro": 'Nicole Common',
        "tipo_logradouro": 'Travessa',
        "bairro": 'Lake Danielle',
        "cidade": 'Judymouth',
        "cep": '85184',
        "tipo": 'casa em condominio',
        "valor": 488423.52,
        "data_aquisicao": '2017-07-29'
    },
    {
        "id": 2,
        "logradouro": 'Price Prairie',
        "tipo_logradouro": 'Travessa',
        "bairro": 'Colonton',
        "cidade": 'North Garyville',
        "cep": '93354',
        "tipo": 'casa em condominio',
        "valor": 260069.89,
        "data_aquisicao": '2021-11-30'
    },
    {
        "id": 3,
        "logradouro": 'Taylor Ranch',
        "tipo_logradouro": 'Avenida',
        "bairro": 'West Jennashire',
        "cidade": 'Katherinefurt',
        "cep": '51116',
        "tipo": 'apartamento',
        "valor": 815969.92,
        "data_aquisicao": '2020-04-24'
    }
]

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""  
    server.config["TESTING"] = True  
    with server.test_client() as client:
        yield client

def test_get_imoveis(client):
    # GET /imoveis - retorna uma lista de todos os imóveis
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        (1, "Nicole Common", "Travessa", "Lake Danielle", "Judymouth", "85184", "casa em condominio", 488423.52, "2017-07-29"),
        (2, "Price Prairie", "Travessa", "Colonton", "North Garyville", "93354", "casa em condominio", 260069.89, "2021-11-30"),
        (3, "Taylor Ranch", "Avenida", "West Jennashire", "Katherinefurt", "51116", "apartamento", 815969.92, "2020-04-24")
    ]
    
    response = client.get("/imoveis")

    assert response.status_code == 200
    
    expected_response = json.dumps(MOCK_IMOVEIS)
    
    assert response.data.decode("utf-8") == expected_response
    
def test_get_imovel(client):
    # GET /imoveis/<id> - retorna um imóvel da lista
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
        
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = MOCK_IMOVEIS[0]
    
    response = client.get("/imoveis/1")
    
    assert response.status_code == 200
        
    expected_response = json.dumps(MOCK_IMOVEIS[0])
        
    assert response.data.decode("utf-8") == expected_response
    
def test_get_imovel_inexistente(client):
    # GET /imoveis/<id> - dá erro se o imóvel não existe
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
        
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    response = client.get("/imoveis/8723743873")
    
    assert response.status_code == 404
        
    assert response.data.decode("utf-8") == "Imóvel não encontrado"
    
def test_get_imoveis_filtrado(client):
    # GET /imoveis?cidade=<cidade> - retorna imóveis filtrados pela cidade
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [MOCK_IMOVEIS[2]]
    
    response = client.get("/imoveis?cidade=Katherinefurt")

    assert response.status_code == 200
    
    expected_response = json.dumps(MOCK_IMOVEIS[2])
    
    assert response.data.decode("utf-8") == expected_response
    
def test_get_imoveis_filtrado_tipo(client):
    # GET /imoveis?tipo=<tipo> - retorna imóveis filtrados pelo tipo
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [MOCK_IMOVEIS[0], MOCK_IMOVEIS[1]]
    
    response = client.get("/imoveis?tipo=casa em condominio")

    assert response.status_code == 200
    
    expected_response = json.dumps(MOCK_IMOVEIS[0], MOCK_IMOVEIS[1])
    
    assert response.data.decode("utf-8") == expected_response
    
def test_post_imovel(client):
    # POST /imoveis - adiciona um novo imóvel
    novo_imovel = {
        "logradouro": "New Street",
        "tipo_logradouro": "Rua",
        "bairro": "New Neighborhood",
        "cidade": "New City",
        "cep": "12345",
        "tipo": "casa em condominio",
        "valor": 300000.00,
        "data_aquisicao": "2022-01-01"
    }
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 4
    
    response = client.post("/imoveis", json=json.dumps(novo_imovel), content_type='application/json')

    assert response.status_code == 201
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["id"] == 4
    assert response_data["mensagem"] == "Imóvel adicionado com sucesso"
    
def test_post_imovel_dados_incompletos(client):
    # POST /imoveis - retorna erro se os dados estão incompletos
    novo_imovel = {
        "logradouro": "New Street",
        "tipo_logradouro": "Rua",
        "bairro": "New Neighborhood",
        "cidade": "New City",
        "cep": "12345",
    }
    
    response = client.post("/imoveis", json=json.dumps(novo_imovel), content_type='application/json')

    assert response.status_code == 400
    assert response.data.decode("utf-8") == "Dados insuficientes para adicionar o imóvel"
    
def test_post_imovel_dados_invalidos(client):
    # POST /imoveis - retorna erro se parte dos dados são inválidos
    novo_imovel = {
        "logradouro": "New Street",
        "tipo_logradouro": "Rua",
        "bairro": "New Neighborhood",
        "cidade": "New City",
        "cep": "12345",
        "tipo": "casa em condominio",
        "valor": "valor aqui",
        "data_aquisicao": "2022-01-01"
    }
    
    response = client.post("/imoveis", json=json.dumps(novo_imovel), content_type='application/json')

    assert response.status_code == 400
    assert response.data.decode("utf-8") == "Dados inválidos para adicionar o imóvel"
    
def test_put_imovel(client):
    # PUT /imoveis/<id> - atualiza os detalhes de um imóvel existente
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    imovel_atualizado = {
        "valor": 600000.00,
        "bairro": "Bairro Atualizado"
    }

    response = client.put("/imoveis/1", data=json.dumps(imovel_atualizado), content_type='application/json')

    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["message"] == "Imóvel atualizado com sucesso"
    
def test_put_imovel_nao_encontrado(client):
    # PUT /imoveis/<id> - retorna erro se o imóvel a ser atualizado não for encontrado
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    imovel_atualizado = {
        "valor": 600000.00,
        "bairro": "Bairro Atualizado"
    }

    response = client.put("/imoveis/999", data=json.dumps(imovel_atualizado), content_type='application/json')

    assert response.status_code == 404
    assert response.data.decode("utf-8") == "Imóvel não encontrado"
    
def test_delete_imovel(client):
    # DELETE /imoveis/<id> - remove um imóvel existente
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete("/imoveis/1")

    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["message"] == "Imóvel removido com sucesso"
    
def test_delete_imovel_nao_encontrado(client):
    # DELETE /imoveis/<id> - retorna erro se o imóvel removido não foi encontrado
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0

    response = client.delete("/imoveis/3235536")

    assert response.status_code == 404
    assert response.data.decode("utf-8") == "Imóvel não encontrado"