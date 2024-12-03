from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_mysqldb import MySQL
# Inicio da Aplicação
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
            session['tipo'] = usuario['tipo'] 
            session['nome'] = usuario['nome']
            session['email'] = usuario['email']
            
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

# Cadastro de restaurante
@app.route('/restaurante', methods=['GET', 'POST'])
def restaurante():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
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

    return render_template('restaurante.html')

# Cadastro de ONG
@app.route('/ong', methods=['GET', 'POST'])
def ong():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
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
        tipo = request.form['tipo']
        localizacao = request.form['localizacao']
        descricao = request.form['descricao']

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO doacoes (tipo, descricao, data, hora, localizacao) VALUES (%s, %s, %s, %s)",
                (tipo, descricao, localizacao, session.get('usuario_id'))
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
    cur.execute("SELECT email FROM usuarios WHERE tipo = 'ong' ")
    emails = cur.fetchall()
    cur.close()

    # Simulação de envio de notificações (apenas para demonstração)
    for email in emails:
        print(f"Notificação enviada para: {email[0]}")

    flash('Notificações enviadas com sucesso!', 'success')
    return redirect('/area_restrita')

if __name__ == '__main__':
    app.run(debug=True)
