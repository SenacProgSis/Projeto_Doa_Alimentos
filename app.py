from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_mysqldb import MySQL

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

        # Configura o cursor para retornar resultados como dicionários
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
        usuario = cur.fetchone()
        cur.close()

        if usuario:
            session['tipo'] = usuario[3]  # Supondo que a coluna tipo seja a quarta na tabela
            session['nome'] = usuario[1]  # Supondo que a coluna nome seja a segunda
            session['email'] = usuario[2]  # Supondo que a coluna email seja a terceira
            
            flash('Login realizado com sucesso!', 'success')
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
    cur.execute("SELECT * FROM doacoes")
    doacoes = cur.fetchall()
    cur.close()
    return render_template('area_restrita.html', doacoes=doacoes)

# Cadastro de pessoa física
@app.route('/pessoa_fisica', methods=['GET', 'POST'])
def pessoa_fisica():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        localizacao = request.form['localizacao']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pessoa_fisica (nome, email, telefone, localizacao) VALUES (%s, %s, %s, %s)",
                    (nome, email, telefone, localizacao))
        mysql.connection.commit()
        cur.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect('/')

    return render_template('pessoa_fisica.html')

# Cadastro de restaurante
@app.route('/restaurante', methods=['GET', 'POST'])
def restaurante():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO restaurante (nome, cnpj, endereco, telefone) VALUES (%s, %s, %s, %s)",
                    (nome, cnpj, endereco, telefone))
        mysql.connection.commit()
        cur.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect('/')

    return render_template('restaurante.html')

# Cadastro de ONG
@app.route('/ong', methods=['GET', 'POST'])
def ong():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        responsavel = request.form['responsavel']
        email = request.form['email']
        telefone = request.form['telefone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ong (nome, cnpj, responsavel, email, telefone) VALUES (%s, %s, %s, %s, %s)",
                    (nome, cnpj, responsavel, email, telefone))
        mysql.connection.commit()
        cur.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect('/')

    return render_template('ong.html')

# Rota para adicionar doações
@app.route('/doar', methods=['GET', 'POST'])
def doar():
    # Verifique se o usuário está logado e se o tipo é permitido
    #if 'tipo' not in session or session['tipo'] not in ['admin', 'restaurante']:
    if session['tipo'] == 'admin' or session['tipo'] == 'restaurante':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect('/area_restrita')

    if request.method == 'POST':
        alimento = request.form['alimento']
        quantidade = request.form['quantidade']
        descricao = request.form['descricao']

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO doacoes (alimento, quantidade, descricao, usuario_id) VALUES (%s, %s, %s, %s)",
                (alimento, quantidade, descricao, session.get('usuario_id'))
            )
            mysql.connection.commit()
            cur.close()

            flash('Doação cadastrada com sucesso!', 'success')
            return redirect('/area_restrita')
        except Exception as e:
            flash(f'Erro ao cadastrar doação: {str(e)}', 'danger')
            return render_template('doar.html')

    return render_template('doar.html')



# Rota para notificar pessoas sobre doações
@app.route('/notificar', methods=['POST'])
def notificar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM pessoa_fisica")
    emails = cur.fetchall()
    cur.close()

    # Simulação de envio de notificações (apenas para demonstração)
    for email in emails:
        print(f"Notificação enviada para: {email[0]}")

    flash('Notificações enviadas com sucesso!', 'success')
    return redirect('/area_restrita')

if __name__ == '__main__':
    app.run(debug=True)
