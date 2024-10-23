import pygame

class MenuResolucaoGlobal:
    def __init__(self):
        self.largura_maxima, self.altura_maxima = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.modo_atual = "modo_janela"  # Modo inicial
        self.tela = None

    def iniciar_tela(self, largura=800, altura=600, modo="modo_janela"):
        """Inicializa a tela com uma resolução e modo padrão."""
        self.aplicar_resolucao(largura, altura, modo)

    def aplicar_resolucao(self, largura, altura, modo):
        """Aplica a resolução e o modo de tela."""
        self.modo_atual = modo
        if modo == "modo_janela":
            self.tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        elif modo == "modo_sem_bordas":
            self.tela = pygame.display.set_mode((largura, altura), pygame.NOFRAME | pygame.RESIZABLE)
        elif modo == "tela_cheia":
            self.tela = pygame.display.set_mode((self.largura_maxima, self.altura_maxima), pygame.FULLSCREEN)

    def obter_tela(self):
        """Retorna o objeto da tela atual."""
        return self.tela

    def obter_dimensoes(self):
        """Retorna as dimensões atuais da tela."""
        if self.tela:
            return self.tela.get_size()
        return self.largura_maxima, self.altura_maxima

# Instancia a configuração global para ser utilizada em todo o aplicativo
menu_resolucao_global = MenuResolucaoGlobal()
