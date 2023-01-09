from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from crudlivros.models import Usuario

class FormLivro(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    autor = StringField("Autor", validators=[DataRequired()])
    descricao = TextAreaField("Descrição")
    botao_submit_adicionar = SubmitField("Adicionar Livro")

class FormCriarConta(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(2,10)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField("Criar Conta")


    def validate_email(self, email):
        usuario =  Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.")


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(2,10)])
    lembrar = BooleanField("Lembrar Dados")
    botao_submit_login = SubmitField("Fazer Login")
