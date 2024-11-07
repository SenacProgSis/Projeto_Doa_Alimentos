from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# config do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'doacao_comida'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        #verificação no banco de dados
        if usuario_autenticado: #parte que ainda está para fazer
            return redirect('/area_restrita')
        else:
            flash('Email ou senha inválidos')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/pessoa_fisica', methods=['GET', 'POST']) #cadastro de pessoa fisica
def pessoa_fisica():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        localizacao = request.form['localizacao']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pessoa_fisica(nome, email, telefone, localizacao) VALUES (%s, %s, %s, %s)", (nome, email, telefone, localizacao))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    
    return render_template('pessoa_fisica.html')

@app.route('/restaurante', methods=['GET', 'POST']) #cadastro do restaurante
def restaurante():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO restaurante(nome, cnpj, endereco, telefone) VALUES (%s, %s, %s, %s)", (nome, cnpj, endereco, telefone))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    
    return render_template('restaurante.html')

@app.route('/ong', methods=['GET', 'POST']) #cadastro de ONGs
def ong():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        responsavel = request.form['responsavel']
        email = request.form['email']
        telefone = request.form['telefone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ong(nome, cnpj, responsavel, email, telefone) VALUES (%s, %s, %s, %s, %s)", (nome, cnpj, responsavel, email, telefone))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    
    return render_template('ong.html')

if __name__ == '__main__':
    app.run(debug=True)
