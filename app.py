from flask import Flask, render_template, json, request, Response, session, redirect, url_for, jsonify
import config
import banco as banco
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
    return render_template('index/triagem.html', titulo='Triagem de Sintomas,')

@app.get('/login')
def login():
    erro = None
    if request.method == 'POST':
        email = request.form.get('username')
        senha = request.form.get('password')
        usuario = banco.buscar_usuario_por_email(email)
        if usuario and usuario['senha'] == senha:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('dashboard'))
        else:
            erro = 'Usuário ou senha inválidos'
    return render_template('index/login.html', erro=erro, titulo='Login')

@app.get('/dados')
def dados():
    return render_template('index/dados.html', titulo='Dados do usuário')

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
