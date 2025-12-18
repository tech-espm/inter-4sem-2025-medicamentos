from flask import Flask, render_template, json, request, Response, session, redirect, url_for, jsonify
from sqlalchemy import create_engine, text
import config
import banco as banco
from datetime import datetime

from models.recommender import recomendar
from regras import aplicar_regras

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

        # ✅ lista de sintomas (snake_case) vinda do front
        sintomas_list = [s for s in request.form.getlist("sintomas") if s]

        # texto livre opcional
        sintomas_extra = (request.form.get("sintomas_texto") or "").strip()

        # texto consolidado para salvar/exibir
        sintomas_texto = ", ".join(sintomas_list)
        if sintomas_extra:
            sintomas_texto = f"{sintomas_texto}, {sintomas_extra}" if sintomas_texto else sintomas_extra

        # ✅ peso SEMPRE definido (fora do try)
        peso_raw = (request.form.get("peso") or "").strip()
        try:
            peso = float(peso_raw) if peso_raw else None
        except ValueError:
            peso = None

        # fallback de recomendação (caso falhe)
        recomendacoes_txt = (
            "Avaliação inicial registrada. "
            "Consulte um profissional se os sintomas persistirem."
        )

        # 🔎 recomendações + regras
        try:
            if sintomas_list:
                df_recs = recomendar(sintomas_list, top_k=10)

                resultado = aplicar_regras(
                    sintomas_list,
                    df_recs,
                    texto_col="doc",
                    score_col="score"
                )

                top5 = resultado.df.head(5)
                alertas = resultado.alertas

                nomes = (
                    top5["nomeMedicamento"].astype(str).tolist()
                    if "nomeMedicamento" in top5.columns else []
                )

                recomendacoes_txt = ""
                if alertas:
                    recomendacoes_txt += "ALERTAS: " + " | ".join(alertas) + " || "

                if nomes:
                    recomendacoes_txt += "Recomendações: " + ", ".join(nomes)
                else:
                    recomendacoes_txt += "Recomendações geradas."
        except Exception as e:
            recomendacoes_txt = (
                "Não foi possível gerar recomendações automaticamente. "
                f"({type(e).__name__})"
            )

        dados_triagem = {
            "idusuario": session["user_id"],
            "peso": peso,
            "sintomas": sintomas_texto or "Sintomas não informados",
            "recomendacoes": recomendacoes_txt
        }

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO triagem (idusuario, peso, sintomas, recomendacoes)
                VALUES (:idusuario, :peso, :sintomas, :recomendacoes)
            """), dados_triagem)

        return redirect(url_for("perfil"))

    return render_template("index/triagem.html", titulo="Triagem de Sintomas")


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
