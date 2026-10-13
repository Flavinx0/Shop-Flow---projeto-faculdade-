class Carrinho:
    def __init__(self, cliente):
        self.__cliente = cliente
        self.__itens = {}

    def adicionar_item(self, produto, quantidade=1):
        if not produto.tem_estoque():
            return False, "Produto sem estoque!"
        id_produto = produto.get_id()
        if id_produto in self.__itens:
            self.__itens[id_produto]["quantidade"] += quantidade
        else:
            self.__itens[id_produto] = {
                "produto": produto,
                "quantidade": quantidade
            }
        return True, "Produto adicionado ao carrinho!"

    def remover_item(self, id_produto):
        if id_produto in self.__itens:
            del self.__itens[id_produto]
            return True
        return False

    def get_itens(self):
        return self.__itens

    def calcular_total(self):
        total = 0
        for item in self.__itens.values():
            total += item["produto"].get_preco() * item["quantidade"]
        return total

    def limpar(self):
        self.__itens = {}

    def esta_vazio(self):
        return len(self.__itens) == 0

    def to_dict(self):
        itens = []
        for item in self.__itens.values():
            itens.append({
                "id": item["produto"].get_id(),
                "nome": item["produto"].get_nome(),
                "preco": item["produto"].get_preco(),
                "quantidade": item["quantidade"],
                "subtotal": item["produto"].get_preco() * item["quantidade"]
            })
        return {
            "itens": itens,
            "total": self.calcular_total()
        }