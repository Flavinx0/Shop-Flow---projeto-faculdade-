from models.usuario import Usuario

class Admin(Usuario):
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)
        self.__nivel = "admin"

    def get_nivel(self):
        return self.__nivel

    # Polimorfismo — implementação do método abstrato
    def exibir_menu(self):
        return [
            "1. Gerenciar Admins",
            "2. Gerenciar Produtos",
            "3. Gerenciar Estoque",
            "4. Gerenciar Pedidos",
            "5. Configurações da Loja",
            "6. Sair"
        ]

    def __repr__(self):
        return f"Admin(nome={self.get_nome()}, email={self.get_email()})"