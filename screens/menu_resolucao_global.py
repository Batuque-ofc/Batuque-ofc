# Esse arquivo tem o proposito de globalizar as config do menu para aplicar em todo o app
import pygame

class MenuResolucaoGlobal:
    def __init__(self):
        self.largura_maxima, self.altura_maxima = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.modo_atual = "modo_janela"
        self.tela = None

    def aplicar_resolucao(self, largura, altura, modo):
        self.modo_atual = modo
        if modo == "modo_janela":
            self.tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        elif modo == "modo_sem_bordas":
            self.tela = pygame.display.set_mode((largura, altura), pygame.NOFRAME | pygame.RESIZABLE)
        elif modo == "tela_cheia":
            self.tela = pygame.display.set_mode((self.largura_maxima, self.altura_maxima), pygame.FULLSCREEN)

    def obter_tela(self):
        return self.tela

    def obter_dimensoes(self):
        return self.tela.get_size()

# Instancia a configuração global para ser utilizada em todo o aplicativo
menu_resolucao_global = MenuResolucaoGlobal()
