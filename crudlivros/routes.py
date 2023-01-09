from crudlivros import app, bcrypt, database
from flask import render_template, url_for, redirect, flash, request
from crudlivros.forms import FormLivro, FormLogin, FormCriarConta
from crudlivros.models import Usuario, Livro
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/')
def home():
    if current_user.is_authenticated:
        livros = Livro.query.filter_by(id_usuario=current_user.id)
        return render_template('home.html', livros=livros)
    else:
        return render_template('home.html')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            flash("Login feito com sucesso", "alert-success")
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash("Falha no login. Usuario e/ou senha incorretos!", "alert-danger")

    return render_template('login.html', form_login=form_login)

@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crip = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crip)
        database.session.add(usuario)
        database.session.commit()
        flash("Conta criada com sucesso", "alert-success")
        return redirect(url_for('home')) 
    return render_template('criarconta.html', form_criarconta=form_criarconta)

@app.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_livro():
    form_livro = FormLivro()
    if form_livro.validate_on_submit():
        livro = Livro(nome=form_livro.nome.data, autor=form_livro.autor.data, descricao=form_livro.descricao.data, leitor=current_user)
        database.session.add(livro)
        database.session.commit()
        flash('Livro adicionado com sucesso.', 'alert-success')
        return redirect(url_for('home'))
    return render_template('adicionarlivro.html', form_livro=form_livro)

@app.route('/sair')
def sair():
    logout_user()
    return redirect(url_for('home'))

@app.route('/editar/<livro_id>', methods=['GET', 'POST'])
def editar(livro_id):
    livro = Livro.query.get(livro_id)
    form = FormLivro()
    if request.method == 'GET':
        form.nome.data = livro.nome
        form.autor.data = livro.autor
        form.descricao.data = livro.descricao
    elif form.validate_on_submit():
        livro.nome = form.nome.data
        livro.autor = form.autor.data
        livro.descricao = form.descricao.data
        database.session.commit()
        flash('Livro editado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('editar.html', form=form)

@app.route('/excluir/<livro_id>', methods=['GET', 'POST'])
def excluir_livro(livro_id):
    livro = Livro.query.get(livro_id)
    database.session.delete(livro)
    database.session.commit()
    flash('Livro excluido com sucesso', 'alert-danger')
    return redirect(url_for('home'))
