from flask import Flask, render_template, json, request, Response, session, redirect, url_for, jsonify
from sqlalchemy import create_engine, text
import config
import banco as banco
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sintomed-secret-key"

engine = create_engine(config.conexao_banco)

def garantir_tabela_triagem():
    """Cria tabela de triagem se ainda não existir."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS triagem (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idusuario INT NOT NULL,
                peso FLOAT NULL,
                sintomas TEXT NOT NULL,
                duracao VARCHAR(50) NULL,
                intensidade VARCHAR(50) NULL,
                recomendacoes TEXT NULL,
                data_triagem DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.route('/triagem', methods=["GET", "POST"])
def triagem():
    if request.method == "POST":
        if "user_id" not in session:
            return redirect(url_for("login"))

        garantir_tabela_triagem()

        sintomas_list = request.form.getlist("sintomas")
        sintomas_extra = request.form.get("sintomas_texto") or ""
        sintomas = ", ".join([s for s in sintomas_list if s])
        if sintomas_extra:
            sintomas = f"{sintomas}, {sintomas_extra}" if sintomas else sintomas_extra

        dados_triagem = {
            "idusuario": session["user_id"],
            "peso": request.form.get("peso"),
            "duracao": request.form.get("duracao"),
            "intensidade": request.form.get("intensidade"),
            "sintomas": sintomas or "Sintomas não informados",
            "recomendacoes": "Avaliação inicial registrada. Consulte um profissional se os sintomas persistirem."
        }

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO triagem (idusuario, peso, sintomas, duracao, intensidade, recomendacoes)
                VALUES (:idusuario, :peso, :sintomas, :duracao, :intensidade, :recomendacoes)
            """), dados_triagem)

        return redirect(url_for("perfil"))

    return render_template('index/triagem.html', titulo='Triagem de Sintomas,')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email") or request.form.get("username")
        senha = request.form.get("senha") or request.form.get("password")

        with engine.connect() as conn:
            user = conn.execute(text("""
                SELECT * FROM usuario
                WHERE email = :email AND senha = :senha
            """), {"email": email, "senha": senha}).fetchone()

        if user:
            mapping = getattr(user, "_mapping", {})
            user_id = mapping.get("idusuario") or mapping.get("idUsuario") or mapping.get("id") or user[0]
            session["user_id"] = user_id
            return redirect(url_for("perfil"))
        else:
            return "Login inválido", 401
        
    cadastro_sucesso = request.args.get("cadastro") == "ok"
    return render_template("index/login.html", cadastro_sucesso=cadastro_sucesso)

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        name = request.form["name"]
        dataNascimento = request.form["age"]
        email = request.form["email"]
        senha = request.form["senha"]
        genero = request.form["genero"]

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO usuario (nomeUsuario, dataNascimento, email, senha, genero)
                VALUES (:nomeUsuario, :dataNascimento, :email, :senha, :genero)
            """), {
                "nomeUsuario": name,
                "dataNascimento": dataNascimento,
                "email": email,
                "senha": senha,
                "genero": genero
            })
            conn.commit()

        return redirect(url_for("login", cadastro="ok"))
    
    return render_template("index/cadastro.html")


@app.get('/perfil')
def perfil():
    triagens = []
    user_id = session.get("user_id")

    if user_id:
        garantir_tabela_triagem()
        with engine.connect() as conn:
            resultado = conn.execute(text("""
                SELECT id, data_triagem, sintomas, recomendacoes
                FROM triagem
                WHERE idusuario = :idusuario
                ORDER BY data_triagem DESC
                LIMIT 50
            """), {"idusuario": user_id}).mappings().all()

        for linha in resultado:
            data_formatada = ""
            if linha.get("data_triagem"):
                data_formatada = linha["data_triagem"].strftime("%d/%m/%Y %H:%M")

            triagens.append({
                "id": linha.get("id"),
                "data": data_formatada,
                "sintomas": linha.get("sintomas", ""),
                "recomendacoes": linha.get("recomendacoes", "")
            })

    return render_template('index/perfil.html', titulo='Dados do usuário', triagens=triagens)


@app.post("/triagem/<int:triagem_id>/excluir")
def excluir_triagem(triagem_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    garantir_tabela_triagem()
    with engine.begin() as conn:
        conn.execute(text("""
            DELETE FROM triagem
            WHERE id = :triagem_id AND idusuario = :idusuario
        """), {"triagem_id": triagem_id, "idusuario": user_id})

    return redirect(url_for("perfil"))

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
