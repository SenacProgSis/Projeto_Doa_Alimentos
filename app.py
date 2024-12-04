from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Início da aplicação
app = Flask(__name__)
app.secret_key = 'sala12345'

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Coloque sua senha aqui
app.config['MYSQL_DB'] = 'doacao_comida'

mysql = MySQL(app)

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()

        if usuario and check_password_hash(usuario['senha'], senha):  # Verifica o hash da senha
            session['tipo'] = usuario['tipo']
            session['nome'] = usuario['nome']
            session['email'] = usuario['email']
            session['usuario_id'] = usuario['id']
            
            flash('Login realizado com sucesso!', 'success')
            
            # Redireciona dependendo do tipo de usuário
            if usuario['tipo'] == 'restaurante':
                return redirect('/restaurante')
            elif usuario['tipo'] == 'ong':
                return redirect('/ong')
            else:  # Caso seja admin
                return redirect('/area_restrita')
        else:
            flash('Email ou senha inválidos!', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Limpa todos os dados da sessão
    return redirect('/')

# Área restrita para gerenciamento de doações
@app.route('/area_restrita')
def area_restrita():
    cur = mysql.connection.cursor()
    cur.execute("SELECT tipo, descricao, data_hora, localizacao FROM doacoes")
    doacoes = cur.fetchall()
    cur.close()
    return render_template('area_restrita.html', doacoes=doacoes)

# Cadastro de usuário (Restaurante ou ONG)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])  # Hash da senha
        nome = request.form['nome']
        cnpj = request.form['cpf_cnpj']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        tipo = request.form['tipo']  # 'Restaurante' ou 'ONG'

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (email, senha, nome, endereco, cpf_cnpj, telefone, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (email, senha, nome, cnpj, endereco, telefone, tipo))
        mysql.connection.commit()
        cur.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect('/')

    return render_template('cadastro.html')

# Rota para adicionar doações
@app.route('/doar', methods=['GET', 'POST'])
def doar():
    if 'tipo' not in session or session['tipo'] != 'restaurante':
        flash('Apenas restaurantes podem cadastrar doações.', 'danger')
        return redirect('/area_restrita')

    if request.method == 'POST':
        tipo = request.form['tipo']
        localizacao = request.form['localizacao']
        descricao = request.form['descricao']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO doacoes (tipo, descricao, localizacao, usuario_id) VALUES (%s, %s, %s, %s)",
            (tipo, descricao, localizacao, session['usuario_id'])
        )
        mysql.connection.commit()
        cur.close()

        flash('Doação cadastrada com sucesso!', 'success')
        return redirect('/area_restrita')

    return render_template('doar.html')

# Rota para notificar ONGs sobre doações
@app.route('/notificar', methods=['POST'])
def notificar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM usuarios WHERE tipo = 'ong'")
    emails = [email[0] for email in cur.fetchall()]
    cur.close()

    # Simulação de envio de e-mails
    for email in emails:
        print(f"Notificação enviada para: {email}")

    flash('Notificações enviadas com sucesso!', 'success')
    return redirect('/area_restrita')

if __name__ == '__main__':
    app.run(debug=True)
