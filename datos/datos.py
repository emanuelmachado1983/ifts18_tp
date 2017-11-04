import csv
from entidades.venta import *
from entidades.producto import *
from entidades.cliente import *

posCodigo = 0
posProducto = 0
posCliente = 0
posCantidad = 0
posPrecio = 0

#En este archivo están las funciones que consultan el csv

def leerRegistro(archivo_csv, valor):
#Lee un registro y devuelve los siguientes códigos de error:
#4: Hay registros con menos valores de los que se espera
#5: Hay un código que está vacío
#6: Hay una cantidad que no es entera
#7: Hay un precio que no es decimal
#0: Funcionó correctamente
    registro = next(archivo_csv, None)
    huboError = 0
    if registro is not None:
        if len(registro) != 5:
            huboError = 4
        if registro[posCodigo].strip() == "":
            huboError = 5
        if not registro[posCantidad].replace('.','',1).isdigit():
            huboError = 6
        else:
            valorAux = float(registro[posCantidad])
            if not valorAux.is_integer():
                huboError = 6
        if not registro[posPrecio].replace('.','',1).isdigit():
            huboError = 7
    return registro, huboError

def definirArchivo(archivo):
#A partir de la cabecera se fija en qué orden se van a leer los campos
#Devuelve codigo de error 3: La cabecera tiene menos valores que los que se espera
# Si funciona correctamente devuelve 0
    archivo_csv = csv.reader(archivo)
    registro, huboError = leerRegistro(archivo_csv, None)        
    global posCodigo
    global posProducto
    global posCliente
    global posCantidad
    global posPrecio
    if len(registro) != 5:
       return registro, archivo_csv, 3 
    for x in range(0, 5):
        if registro[x] == "CODIGO":
            posCodigo = x
        if registro[x] == "PRODUCTO":
            posProducto = x
        if registro[x] == "CLIENTE":
            posCliente = x
        if registro[x] == "CANTIDAD":
            posCantidad = x
        if registro[x] == "PRECIO":
            posPrecio = x
    return registro, archivo_csv, 0


def traerVentas():
#Devuelve una lista con todos los registros del csv
#Puede devolver los siguientes códigos de error
#1: Error indeterminado
#2: No se pudo abrir el archivo
#0: Funcionó correctamente
    try:
        with open('ventas.csv') as archivo:
            registro, archivo_csv, huboError = definirArchivo(archivo)
            if huboError > 0:
                return [], huboError
            registro, huboError = leerRegistro(archivo_csv,None)
            if huboError > 0:
                return [], huboError
            lista = []
            while registro:
                venta = Venta(registro[posCliente], registro[posCodigo], registro[posProducto], registro[posCantidad], registro[posPrecio])
                lista.append(venta)
                registro, huboError = leerRegistro(archivo_csv, None)
                if huboError > 0:
                    return [], huboError
            return lista, 0
    except OSError:
        return [], 2
    else: 
        return [], 1


def validarExisteUsuarioDatos(usuario):
#funcion que valida si existe un usuario determinado
#Puede devolver los siguientes códigos de error
#1: Error indeterminado
#2: No se pudo abrir el archivo
#0: Funcionó correctamente
    try:
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if usuario == registro[0]:
                    return 0, 0
                registro = next(archivo_csv, None)
            return 1, 0
    except OSError:
        return 0, 2
    else: 
        return 0, 1

def grabarUsuarioDatos(registro):
#se graba el Usuario en usuarios.csv
    try:
        with open('usuarios.csv', 'a+') as archivo:
            archivo_csv = csv.writer(archivo)
            archivo_csv.writerow(registro) 
        return 1, 0       
    except OSError:
        return 0, 2
    else: 
        return 0, 1

def buscarUsuarioDatos(nombreUsuario, password):
#busca usuario y contraseña en el archivo usuarios.csv
    try:
        with open('usuarios.csv') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if nombreUsuario == registro[0] and password == registro[1]:
                    return 1, 0
                registro = next(archivo_csv, None)
            else:
                return 0, 0
    except OSError:
        return 0, 2
    else: 
        return 0, 1