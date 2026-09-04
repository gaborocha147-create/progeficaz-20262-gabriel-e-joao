from flask import Flask, render_template_string, request, redirect
import json
import utils

server = Flask(__name__)

config = server.config
test_client = server.test_client

@server.route('/')
def pagina_imoveis():
    return render_template_string('''
        <p>Servidor rodando...</p>
        <p>Acesse /imoveis para acessar a API.</p>
    ''')
