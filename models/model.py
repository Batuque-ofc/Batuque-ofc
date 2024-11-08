class Usuario:
    def __init__(self, usuario, senha, email, premium=False):
        self.usuario = usuario
        self.senha = senha
        self.email = email
        self.premium = premium