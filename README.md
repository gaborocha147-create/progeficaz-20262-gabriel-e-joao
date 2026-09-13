# API de Imóveis

API RESTful para gerenciamento de imóveis, desenvolvida com Flask e integrada a um banco de dados MySQL hospedado no Aiven.

## Deploy na AWS

A API está hospedada em uma instância EC2 da AWS e pode ser acessada pelo seguinte endereço:

**URL da API:** http://44.220.140.12/

**Listar imóveis:** http://44.220.140.12/imoveis

## Rotas

| Método   | Rota                               | Descrição                               |
| -------- | ---------------------------------- | --------------------------------------- |
| `GET`    | `/`                                | Verifica se o servidor está funcionando |
| `GET`    | `/imoveis`                         | Lista todos os imóveis                  |
| `GET`    | `/imoveis/<id>`                    | Retorna um imóvel pelo ID               |
| `POST`   | `/imoveis`                         | Adiciona um novo imóvel                 |
| `PUT`    | `/imoveis/<id>`                    | Atualiza um imóvel existente            |
| `DELETE` | `/imoveis/<id>`                    | Remove um imóvel                        |
| `GET`    | `/imoveis/search?tipo=Casa`        | Busca imóveis por tipo                  |
| `GET`    | `/imoveis/search?cidade=São Paulo` | Busca imóveis por cidade                |

## Tecnologias utilizadas

* Python
* Flask
* MySQL
* Aiven
* Gunicorn
* Nginx
* AWS EC2
* Pytest

## Executar os testes

Instale as dependências:

pip install -r requirements.txt

Execute os testes automatizados:

pytest
Autores
Gabriel Rocha
João Nunes