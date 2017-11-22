class Producto:
    codigo = ""
    producto = ""
    cantidad = 0
    precio = 0
    def __init__(self, codigo, producto, cantidad, precio):
        self.codigo = codigo
        self.producto = producto
        self.cantidad = cantidad
        self.precio  = precio

    def retornarLinea(self):
        return [self.codigo, self.producto, self.cantidad]
