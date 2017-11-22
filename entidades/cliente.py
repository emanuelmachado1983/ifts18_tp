class Cliente:
    nombre = ""
    valor = 0
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def retornarLinea(self):
        return [self.nombre, self.valor]
