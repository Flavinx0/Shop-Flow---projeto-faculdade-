from models.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, nome, email, senha, cpf, endereco):
        super().__init__(nome, email, senha)
        self.__cpf = cpf
        self.__endereco = endereco

    # Getters
    def get_cpf(self):
        return self.__cpf

    def get_endereco(self):
        return self.__endereco

    # Setters
    def set_endereco(self, endereco):
        self.__endereco = endereco

    # Polimorfismo — mesma assinatura, comportamento diferente do Admin
    def exibir_menu(self):
        return [
            "1. Ver Produtos",
            "2. Meu Carrinho",
            "3. Meus Pedidos",
            "4. Meu Perfil",
            "5. Sair"
        ]

    def __repr__(self):
        return f"Cliente(nome={self.get_nome()}, email={self.get_email()})"