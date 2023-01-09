from crudlivros import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    livros = database.relationship('Livro', backref='leitor', lazy=True)

    def contar_livros(self):
        return len(self.livros)

class Livro(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    autor = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=True, default="")
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id') ,nullable=False)



    