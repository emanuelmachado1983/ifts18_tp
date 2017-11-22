from datos.datos import *
import time
from datetime import datetime
#Aquí estarán las funciones que se dedican a realizar la lógica del programa

pathExportados = "archivoSalida/"

def traerClientes():
#Devuelve una lista de clientes ordenada por nombre
    lista, huboError = traerVentas() 
    if huboError > 0:
        return [], huboError
    try:
        listaAux = []
        for venta in lista:
            cliente = Cliente(venta.cliente, 0)
            enc = 0
            for aux in listaAux:
                if aux.nombre == venta.cliente:
                    enc = 1
            if enc==0:
                listaAux.append(cliente)
        listaClientes = sorted(listaAux, key=lambda cliente: cliente.nombre)
        listaClientesFinal = []
        for x in listaClientes:
            listaClientesFinal.append(x)
        return listaClientesFinal, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerProductos():
#Devuelve una lista de productos ordenada por el nombre del producto
    lista, huboError = traerVentas() 
    if huboError > 0:
        return [], huboError
    try:
        listaAux = []
        for venta in lista:
            producto = Producto(venta.codigo, venta.producto, 0, 0)
            enc = 0
            for aux in listaAux:
                if aux.producto == venta.producto:
                    enc = 1
            if enc==0:
                listaAux.append(producto)
        listaProductos = sorted(listaAux, key=lambda producto: producto.producto)
        listaProductosFinal = []
        for x in listaProductos:
            listaProductosFinal.append(x)
        return listaProductosFinal, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerUltimasVentas():
#Devuelve una lista con las últimas 10 ventas
    lista, huboError = traerVentas() 
    listaResultado = []   
    if huboError > 0:
        return listaResultado, huboError
    try:
        x=10 #traigo las ultimas diez ventas
        while x>0:
            if len(lista)>0:
                listaResultado.append(lista.pop())
            else:
                x = 0
            x=x-1
        return listaResultado, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerProductosPorCliente(cliente):
#Devuelve una lista con las ventas que se le hicieron a un determinado cliente
    try:
        lista, huboError = traerVentas()  
        if huboError > 0:
            return [], huboError
        listaResultado = []
        for venta in lista:
            if venta.cliente == cliente:
            	listaResultado.append(venta)
        listaResultado = sorted(listaResultado, key=lambda venta: venta.producto)
        return listaResultado, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerClientesPorProducto(producto):
#Devuelve una lista con las ventas de un determinado producto 
    try:
        lista, huboError = traerVentas()  
        if huboError > 0:
            return [], huboError
        listaResultado = []
        for venta in lista:
            if venta.producto == producto:
                listaResultado.append(venta)
        listaResultado = sorted(listaResultado, key=lambda venta: venta.cliente)
        return listaResultado, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerProductosMasVendidos():
#Devuelve una lista con los 5 productos más vendidos.
#Si el quinto puesto está compartido por varios productos, también los trae
    try:
        lista, huboError = traerVentas()  
        if huboError > 0:
            return [], huboError
        listaProductos = []
        for venta in lista:
            enc = 0
            for auxiliar in listaProductos:
                if auxiliar.producto == venta.producto:
                    auxiliar.cantidad = float(auxiliar.cantidad) + float(venta.cantidad)
                    enc =1
            if enc == 0:
                producto = Producto(venta.codigo, venta.producto, float(venta.cantidad), 0)
                listaProductos.append(producto)
        listaProductos = sorted(listaProductos, key=lambda producto: producto.cantidad)
        listaResultado = []
        x= 5 #para que me traiga los 5 mas vendidos
        cantAnterior = -1;
        while x>0:
            if len(listaProductos)>0:
                auxProduc = listaProductos.pop()
                listaResultado.append(auxProduc)
                #este codigo que comento es por si quiero mostrar el dia de mañana las 5 cantidades mas vendidas
                #if auxProduc.cantidad != cantAnterior:
                #    x=x-1 
                x= x - 1
                cantAnterior = auxProduc.cantidad
            else:
                x = -1     
        encFin = 0
        while encFin ==0:
            if len(listaProductos)>0:
                auxProduc = listaProductos.pop()
                if auxProduc.cantidad == cantAnterior:
                    listaResultado.append(auxProduc)
                else:
                    encFin = 1
            else:
                encFin = 1
        return listaResultado, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def traerClientesMasCompradores():
#Devuelve una lista con los 5 clientes más compradores.
#Si el quinto puesto está compartido por varios clientes, también los trae
    try:
        lista, huboError = traerVentas()  
        if huboError > 0:
            return [], huboError
        listaClientes = []
        for venta in lista:
            enc = 0
            for auxiliar in listaClientes:
                if auxiliar.nombre == venta.cliente:
                    auxiliar.valor = auxiliar.valor + float(venta.cantidad) * float(venta.precio)
                    enc =1
            if enc == 0:
                cliente = Cliente(venta.cliente, float(venta.cantidad) * float(venta.precio))
                listaClientes.append(cliente)
        listaClientes = sorted(listaClientes, key=lambda cliente: cliente.valor)
        listaResultado = []
        x= 5 #para que me traiga los 5 más compradores
        valorAnterior = -1;
        while x>0:
            if len(listaClientes)>0:
                auxCliente = listaClientes.pop()
                listaResultado.append(auxCliente)
                #este codigo que comento es por si quiero mostrar el dia de mañana las 5 cantidades mas compradoras
                #if auxCliente.valor != valorAnterior:
                #    x=x-1 
                x=x-1 
                valorAnterior = auxCliente.valor
            else:
                x = -1     
        encFin = 0
        while encFin ==0:
            if len(listaClientes)>0:
                auxCliente = listaClientes.pop()
                if auxCliente.valor == valorAnterior:
                    listaResultado.append(auxCliente)
                else:
                    encFin = 1
            else:
                encFin = 1
        return listaResultado, 0
    except OSError:
        return [], 2
    else: 
        return [], 1

def validarExisteUsuario(usuario):
#funcion que llama a la funcion correspondiente a la validación de Usuario
    valor,huboError = validarExisteUsuarioDatos(usuario)
    return valor, huboError

def grabarUsuario(registro):
#funcion que llama a a la función correspondiente que graba el usuario
    valor,huboError = grabarUsuarioDatos(registro)
    return valor, huboError

def buscarUsuario(nombreUsuario, password):
#funcion que llama a a la función correspondiente que busca un usuario
    valor,huboError = buscarUsuarioDatos(nombreUsuario, password)
    return valor, huboError

def generarArchivoCsv(titulo, cabecera, lista):
#funcion que genera un archivo .csv a partir de una lista que se le pasa por parámetro
    try:
        nombreArchivo = "Resultado_" + datetime.now().strftime("%Y%m%d_%H:%M:%S") + ".csv"
        nombreArchivoConPath = pathExportados + nombreArchivo
        with open(nombreArchivoConPath, 'w') as archivo:
            archivo_csv = csv.writer(archivo)
            archivo_csv.writerow(titulo)
            archivo_csv.writerow(cabecera)
            for venta in lista:
                registro = venta.retornarLinea()
                archivo_csv.writerow(registro) 
        return nombreArchivo, nombreArchivoConPath , 0

    except OSError:
        return "","", 8
    else: 
        return "","", 8    

def grabarPwdUsuario(registro):
#funcion que llama a a la función correspondiente que graba la contraseña del usuario
    valor,huboError = grabarPwdUsuarioDatos(registro)
    return valor, huboError
