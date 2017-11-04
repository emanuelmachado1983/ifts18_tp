#!/usr/bin/env python
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, RegistrarForm, ProductosPorClienteForm, ClientesPorProductosForm

from logica.logica import *

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

def tratarError(huboError):
#Hay ciertas funciones que devuelven un código de error, 
#esta función se encarga de devolver el texto que significa ese código
    if huboError == 1:
        flash("Error: Error indeterminado")
    if huboError == 2:
        flash("Error: No se pudo abrir el archivo")
    if huboError == 3:
        flash("Error: La cabecera tiene menos valores que los que se espera")
    if huboError == 4:
        flash("Error: Hay registros con menos valores de los que se espera")
    if huboError == 5:
        flash("Error: Hay un código que está vacío")
    if huboError == 6:
        flash("Error: Hay una cantidad que no es entera")
    if huboError == 7:
        flash("Error: Hay un precio que no es decimal")

@app.route('/')
def index():
#retorna la pagina principal
#si el usuario está logueado va a las últimas ventas, sino va al index
    if 'username' in session:
        listaResultado, huboError = traerUltimasVentas()
        tratarError(huboError)
        return render_template('ultimasVentas.html', lista = listaResultado)    
    return render_template('index.html', fecha_actual=datetime.utcnow())

@app.errorhandler(404)
def no_encontrado(e):
#devuelve error 404 
    if 'username' in session:
        return render_template('404_ingresado.html'), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
#devuelve error 500 
    if 'username' in session:
        return render_template('500_ingresado.html'), 404
    return render_template('500.html'), 500

@app.route('/ultimasVentas', methods =['GET'])
def ultimasVentas():
#En caso de estar logueado muestra la pagina de las 10 ultima ventas
#sino va a la pantalla de login
    if 'username' not in session:
        return redirect(url_for('ingresar'))
    listaResultado, huboError = traerUltimasVentas()
    tratarError(huboError)
    return render_template('ultimasVentas.html', lista = listaResultado)

@app.route('/productosMasVendidos', methods =['GET'])
def productosMasVendidos():
#En caso de estar logueado muestra la pagina donde se traen los 5 productos más vendidos 
#En caso de que haya varios productos que compartan el quinto puesto, los trae también
#si no está logueado, va a la pantalla de login
    if 'username' not in session:
        return redirect(url_for('ingresar'))
    listaResultado, huboError = traerProductosMasVendidos()
    tratarError(huboError)
    return render_template('productos_mas_vendidos.html', lista = listaResultado)

@app.route('/clientesMasCompradores', methods =['GET'])
def clientesMasCompradores():
#En caso de estar logueado muestra los 5 clientes más compradores
#En caso de que haya varios clientes que compartan el quinto puesto, los trae también
#si no está logueado, va a la pantalla de login
    if 'username' not in session:
        return redirect(url_for('ingresar'))
    listaResultado, huboError = traerClientesMasCompradores()
    tratarError(huboError)
    return render_template('clientes_mas_compradores.html', lista = listaResultado)

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
#realiza el ingreso del usuario
    if 'username' in session:
        return render_template('ingresado.html')
    formulario = LoginForm()
    if formulario.validate_on_submit():
        valor, huboError = buscarUsuario(formulario.usuario.data, formulario.password.data)
        tratarError(huboError)
        if valor == 1:
            session['username'] = formulario.usuario.data
            listaResultado, huboError = traerUltimasVentas()
            tratarError(huboError)
            return render_template('ingresado.html', lista = listaResultado, usuario=session['username'])
        else:
            flash('Error: Revisá nombre de usuario y contraseña')
            return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

@app.route('/productosPorCliente', methods=['GET', 'POST'])
def productosPorCliente():
#En caso de estar logueado me lleva a la pantalla donde se muestran los productos que haya comprado un cliente específico
#si no está logueado, va a la pantalla de login
    if 'username' not in session:
        return redirect(url_for('ingresar'))
    formulario = ProductosPorClienteForm()
    listaResultado = []
    if formulario.validate_on_submit():
        listaResultado, huboError = traerProductosPorCliente(formulario.cliente.data)
        tratarError(huboError)
    listaClientes, huboError = traerClientes()
    tratarError(huboError)
    return render_template('productos_por_cliente.html', lista = listaResultado, formulario=formulario, cliente = formulario.cliente.data, listaclientes = listaClientes)

@app.route('/clientesPorProducto', methods=['GET', 'POST'])
def clientesPorProducto():
#En caso de estar logueado me lleva a la pantalla donde se muestran los clientes que compraron un determinado producto
#si no está logueado, va a la pantalla de login
    if 'username' not in session:
        return redirect(url_for('ingresar'))
    formulario = ClientesPorProductosForm()
    listaResultado = []
    if formulario.validate_on_submit():
        listaResultado, huboError = traerClientesPorProducto(formulario.producto.data)
        tratarError(huboError)
    listaProductos, huboError = traerProductos()
    tratarError(huboError)
    return render_template('clientes_por_producto.html', lista = listaResultado, formulario=formulario, producto = formulario.producto.data, listaProductos = listaProductos)




@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
#me lleva a la pantalla de registración
    if 'username' in session:
        return render_template('ingresado.html')
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            valor, huboError = validarExisteUsuario(formulario.usuario.data)
            tratarError(huboError)
            if valor==0:
                flash("Error: El usuario ya existe")
                return render_template('registrar.html', form=formulario)
            registro = [formulario.usuario.data, formulario.password.data]
            valor, huboError = grabarUsuario(registro)
            tratarError(huboError)
            if valor == 1:
                flash('Mensaje: Usuario creado correctamente')
            else:
                flash('Error: Hubo un error en la creación del usuario')
            return redirect(url_for('ingresar'))
        else:
            flash('Error: Las passwords que acaba de ingresar no son la misma')
    return render_template('registrar.html', form=formulario)



@app.route('/salir', methods=['GET'])
def logout():
#funcion para que se desloguee un usuario
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    # manager.run()
