from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from pathlib import Path
import json
import uuid

jonh = Flask(__name__)


# _____________________ começo dos cartões _____________________

arquivo_cartoes = Path(__file__).resolve().parent / "cartoes.json"

def carregar_cartoes():
    if not arquivo_cartoes.exists():
        return []

    try:
        with open(arquivo_cartoes, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []

def salvar_cartoes(cartoes):
    with open(arquivo_cartoes, "w", encoding="utf-8") as arquivo:
        json.dump(cartoes,arquivo, ensure_ascii=False, indent=4)

@jonh.route("/redes")
def redes():
    cartoes = carregar_cartoes()
    return render_template("redes.html", listagem=cartoes)

@jonh.route("/cartao", methods=["post"])
def colocar():
    titulo = request.form.get("titulo")
    texto = request.form.get("texto")

    if titulo and texto:
        cartoes = carregar_cartoes()

        novo_cartao = {
            "id": str(uuid.uuid4()),
            "titulo": titulo,
            "texto": texto,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        cartoes.append(novo_cartao)
        salvar_cartoes(cartoes)
    return redirect(url_for("redes"))

@jonh.route("/excluir/<id_cartao>", methods=["POST"])
def excluir_cartao(id_cartao):
    cartoes = carregar_cartoes()

    cartoes = [
        carta for carta in cartoes if carta["id"] != id_cartao
    ]

    salvar_cartoes(cartoes)

    return redirect(url_for("redes"))

# _____________________ termino dos cartões _____________________

dados_usuario = ""
lista_tarefas = ["Exemplo", "trabalhar"]
listagem=[]

@jonh.route("/")
def home():
    return render_template(
        "index.html", 
        usuario=dados_usuario, 
        tarefas=lista_tarefas,
        listo=listagem, 
        solver=None
    )

# Rota exclusiva para salvar o nome do usuário
@jonh.route("/salvar_nome", methods=["POST"])
def nome():
    global dados_usuario
    nome_digitado = request.form.get("seu_nome")
    if nome_digitado:
        dados_usuario = nome_digitado
    return redirect(url_for("home"))

# Rota para colocar nova tarefa
@jonh.route("/enviar", methods=["POST"])
def adicionar_tarefa():
    item = request.form.get("nova_tarefa")
    if item:
        lista_tarefas.append(item)
    return redirect(url_for("home"))

# Rota da calculadora
@jonh.route("/calcular", methods=["get","post"])
def calculador():
    solver = None
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('numero1', 0))
            num2 = float(request.form.get('numero2', 0))
            operacao = request.form.get('operacao')

            if operacao == 'soma':
                solver = num1 + num2
            elif operacao == 'subtracao':
                solver = num1 - num2
            elif operacao == 'multiplicacao':
                solver = num1 * num2
            elif operacao == 'divisao':
                solver = num1 / num2 if num2 != 0 else "Erro: Divisão por zero"
        except (ValueError, TypeError):
            solver = "Erro: Entrada inválida"

    return render_template('index.html', solver=solver, 
                           usuario=dados_usuario, 
                           tarefas=lista_tarefas,
                           listo=listagem)

if __name__ == "__main__":
    jonh.run(debug=True)
