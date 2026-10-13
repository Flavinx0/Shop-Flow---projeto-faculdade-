from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome, email, senha):
        self.__nome = nome
        self.__email = email
        self.__senha = senha

    # Getters
    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_senha(self):
        return self.__senha

    # Setters
    def set_nome(self, nome):
        self.__nome = nome

    def set_email(self, email):
        self.__email = email

    def set_senha(self, senha):
        self.__senha = senha

    # Método abstrato — obriga Admin e Cliente a implementarem
    @abstractmethod
    def exibir_menu(self):
        pass

    def __repr__(self):
        return f"Usuario(nome={self.__nome}, email={self.__email})"