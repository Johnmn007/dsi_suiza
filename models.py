# models.py
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class LoginNot(db.Model):
    __tablename__ = 'login_not'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'<LoginNot {self.usuario}>'
