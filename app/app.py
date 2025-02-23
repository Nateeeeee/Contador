from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelo da Tabela de Usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Funções para gerenciar códigos de convite (usando CSV)
def verificar_codigo_convite(codigo):
    try:
        with open('convites.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            codigos = [linha[0] for linha in reader]
            return codigo.upper() in codigos
    except FileNotFoundError:
        return False

def remover_codigo_utilizado(codigo):
    try:
        with open('convites.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            codigos = [linha[0] for linha in reader if linha[0] != codigo.upper()]
        
        with open('convites.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for c in codigos:
                writer.writerow([c])
    except FileNotFoundError:
        pass

def gerar_codigo_convite():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def salvar_codigos(codigos, arquivo='convites.csv'):
    with open(arquivo, 'a', newline='') as f:
        writer = csv.writer(f)
        for codigo in codigos:
            writer.writerow([codigo])

# Rotas principais
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('contador.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, password):
            session['logged_in'] = True
            session['username'] = usuario.username
            return redirect(url_for('index'))
        else:
            error = 'Usuário ou senha incorretos.'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        invite_code = request.form['invite_code'].strip().upper()

        if not verificar_codigo_convite(invite_code):
            error = "Código de convite inválido ou já utilizado!"
            return render_template('register.html', error=error)

        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            error = "Usuário já existe!"
        else:
            remover_codigo_utilizado(invite_code)
            
            # Salva o código utilizado em CSV
            with open('convites_utilizados.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([invite_code, username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            novo_usuario = Usuario(username=username, password=hashed_password)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso! Faça login.")
            return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Painel de Admin
@app.route('/admin')
def admin():
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    try:
        with open('convites.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            codigos = [linha[0] for linha in reader]
    except FileNotFoundError:
        codigos = []
    
    try:
        with open('convites_utilizados.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            codigos_utilizados = list(reader)
    except FileNotFoundError:
        codigos_utilizados = []
    
    return render_template('admin.html', codigos=codigos, codigos_utilizados=codigos_utilizados)

@app.route('/admin/gerar_convites', methods=['POST'])
def gerar_convites():
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    quantidade = int(request.form.get('quantidade', 5))
    novos_codigos = [gerar_codigo_convite() for _ in range(quantidade)]
    salvar_codigos(novos_codigos)
    
    flash(f"{quantidade} novos códigos gerados com sucesso!")
    return redirect(url_for('admin'))

@app.route('/admin/apagar_codigo/<codigo>', methods=['POST'])
def apagar_codigo(codigo):
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    try:
        with open('convites.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            codigos = [linha[0] for linha in reader if linha[0] != codigo.upper()]
        
        with open('convites.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for c in codigos:
                writer.writerow([c])
        
        flash(f"Código {codigo} apagado com sucesso!")
    except FileNotFoundError:
        flash("Erro: Arquivo de códigos não encontrado.")
    
    return redirect(url_for('admin'))

# Gerenciamento de Usuários
@app.route('/admin/usuarios')
def admin_usuarios():
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    # Lista todos os usuários
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        novo_username = request.form.get('username')
        nova_senha = request.form.get('password')
        
        # Atualiza o nome de usuário (se fornecido)
        if novo_username:
            usuario_existente = Usuario.query.filter_by(username=novo_username).first()
            if usuario_existente and usuario_existente.id != usuario.id:
                flash("Nome de usuário já existe!", "error")
            else:
                usuario.username = novo_username
        
        # Atualiza a senha (se fornecida)
        if nova_senha:
            usuario.password = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
        
        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for('admin_usuarios'))
    
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/admin/excluir_usuario/<int:id>', methods=['POST'])
def excluir_usuario(id):
    if not session.get('logged_in') or session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for('admin_usuarios'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

        if not Usuario.query.filter_by(username='admin').first():
            hashed_password = bcrypt.generate_password_hash('senha_admin').decode('utf-8')
            admin = Usuario(username='admin', password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
    app.run(host="0.0.0.0", port=5000,debug=True)