from flask import Flask, render_template, request, redirect, url_for

jonh = Flask(__name__)

dados_usuario = "Maria"
lista_tarefas =  ["Exemplo","/trabalhar"]

@jonh.route("/")
def home():
    return render_template("index.html", 
     usuario=dados_usuario, 
       tarefas=lista_tarefas,
       solver=None)

@jonh.route("/enviar", methods=["post"])
def adicionar_tarefa():
    item = request.form.get("nova_tarefa")

    if item:
        lista_tarefas.append(item)

    return redirect(url_for("home"))


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

    return render_template('index.html', solver=solver, usuario=dados_usuario, tarefas=lista_tarefas)
if __name__ == "__main__":
    jonh.run(debug=True)
   
#return redirect(url_for("home"))    


