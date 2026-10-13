from datetime import datetime

class ItemPedido:
    def __init__(self, produto, quantidade):
        self.__produto = produto
        self.__quantidade = quantidade
        self.__preco_unitario = produto.get_preco()

    def get_produto(self):
        return self.__produto

    def get_quantidade(self):
        return self.__quantidade

    def get_preco_unitario(self):
        return self.__preco_unitario

    def get_subtotal(self):
        return self.__preco_unitario * self.__quantidade

    def to_dict(self):
        return {
            "produto": self.__produto.get_nome(),
            "quantidade": self.__quantidade,
            "preco_unitario": self.__preco_unitario,
            "subtotal": self.get_subtotal()
        }


class Pedido:
    _contador = 1

    def __init__(self, cliente):
        self.__id = Pedido._contador
        Pedido._contador += 1
        self.__cliente = cliente
        self.__itens = []
        self.__status = "Pendente"
        self.__data = datetime.now().strftime("%d/%m/%Y %H:%M")

    def get_id(self):
        return self.__id

    def get_status(self):
        return self.__status

    def get_data(self):
        return self.__data

    def get_itens(self):
        return self.__itens

    def get_cliente(self):
        return self.__cliente

    def adicionar_item(self, produto, quantidade):
        item = ItemPedido(produto, quantidade)
        self.__itens.append(item)

    def calcular_total(self):
        return sum(item.get_subtotal() for item in self.__itens)

    def atualizar_status(self, novo_status):
        status_validos = ["Pendente", "Confirmado", "Enviado", "Entregue", "Cancelado"]
        if novo_status in status_validos:
            self.__status = novo_status
            return True
        return False

    def to_dict(self):
        return {
            "id": self.__id,
            "cliente": self.__cliente.get_nome(),
            "itens": [item.to_dict() for item in self.__itens],
            "total": self.calcular_total(),
            "status": self.__status,
            "data": self.__data
        }

    def __repr__(self):
        return f"Pedido(id={self.__id}, status={self.__status})"