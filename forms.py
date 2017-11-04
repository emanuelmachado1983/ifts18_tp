from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required
from logica.logica import *

class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')

class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')

class ProductosPorClienteForm(FlaskForm):
    cliente = StringField('Cliente', validators=[Required()])
    enviar = SubmitField('Buscar')

class ClientesPorProductosForm(FlaskForm):
    producto = StringField('Producto', validators=[Required()])
    enviar = SubmitField('Buscar')
