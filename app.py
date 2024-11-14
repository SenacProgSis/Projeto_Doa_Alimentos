from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Rota para exibir a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para receber os dados de doação
@app.route('/doar', methods=['POST'])
def doar():
    # Recebe os dados do formulário
    nome = request.form['nome']
    alimento = request.form['alimento']
    quantidade = request.form['quantidade']

    if not nome or not alimento or not quantidade:
        return jsonify({"status": "erro", "message": "Por favor, preencha todos os campos."}), 400

    # Aqui você pode salvar os dados em um banco de dados, por enquanto vamos apenas simular
    print(f"Doação recebida: {nome} doou {quantidade} kg de {alimento}")

    # Envia a resposta de sucesso
    return jsonify({"status": "sucesso", "message": "Doação registrada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)