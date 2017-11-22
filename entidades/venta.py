class Venta:
    cliente=""
    codigo=""
    producto=""
    cantidad=0
    precio=0
    def __init__(self, cliente, codigo, producto, cantidad, precio):
        self.cliente = cliente
        self.codigo = codigo
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio

    def retornarLinea(self):
        return [self.cliente, self.codigo, self.producto, self.cantidad, self.precio]
