class Produto:
    def __init__(self, id, nome, descricao, preco, categoria, estoque):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__preco = preco
        self.__categoria = categoria
        self.__estoque = estoque

    # Getters
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_descricao(self):
        return self.__descricao

    def get_preco(self):
        return self.__preco

    def get_categoria(self):
        return self.__categoria

    def get_estoque(self):
        return self.__estoque

    # Setters
    def set_nome(self, nome):
        self.__nome = nome

    def set_preco(self, preco):
        self.__preco = preco

    def set_estoque(self, estoque):
        self.__estoque = estoque

    def atualizar_estoque(self, quantidade):
        self.__estoque += quantidade

    def tem_estoque(self):
        return self.__estoque > 0

    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "descricao": self.__descricao,
            "preco": self.__preco,
            "categoria": self.__categoria,
            "estoque": self.__estoque
        }

    def __repr__(self):
        return f"Produto(nome={self.__nome}, preco={self.__preco})"