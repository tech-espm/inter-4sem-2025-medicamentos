from flask import Flask, render_template, json, request, Response
import config
from datetime import datetime

app = Flask(__name__)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/triagem')
def triagem():
    return render_template('index/triagem.html', titulo='Triagem de Sintomas')

@app.get('/login')
def login():
    return render_template('index/login.html', titulo='Login', mensagem='Faça seu login para acessar o sistema.')

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
