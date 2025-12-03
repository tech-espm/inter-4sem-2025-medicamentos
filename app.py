from flask import Flask, render_template, json, request, Response, session, redirect, url_for, jsonify
from sqlalchemy import create_engine, text
import config
import banco as banco
from datetime import datetime

app = Flask(__name__)

engine = create_engine(config.conexao_banco)

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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with engine.connect() as conn:
            user = conn.execute(text("""
                SELECT * FROM users
                WHERE email = :email AND password = :password
            """), {"email": email, "password": password}).fetchone()

        if user:
            return redirect(url_for("index"))
        else:
            return "Login inválido", 401

    return render_template("index/login.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        name = request.form["name"]
        dataNascimento = request.form["age"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        senha = request.form["password"]

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO usuario (name, dataNascimento, cpf, email, senha)
                VALUES (:name, :dataNascimento, :cpf, :email, :senha)
            """), {
                "name": name,
                "dataNascimento": dataNascimento,
                "cpf": cpf,
                "email": email,
                "senha": senha
            })
            conn.commit()

        return redirect(url_for("login"))
    
    return render_template("index/cadastro.html")


@app.get('/resultados')
def resultados():
    return render_template('index/resultados.html', titulo='Dados do usuário')

@app.route("/api/grafico_marcas")
def grafico_marcas():
    with engine.connect() as conn:
        resultado = conn.execute(text("""
            SELECT m.nomeMarca AS marca, COUNT(md.idMedicamentos) AS total
            FROM medicamentos md
            JOIN marca m ON md.marca = m.idmarca
            GROUP BY m.nomeMarca
            ORDER BY total DESC;
        """))

        dados = resultado.fetchall()

    marcas = [linha[0] for linha in dados]
    totais = [linha[1] for linha in dados]

    return jsonify({"marcas": marcas, "totais": totais})

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
