import pygame
import sys
import time
from Tutoriais.main_tutorial import executar_tutorial  # Função principal para executar qualquer tutorial
from Tutoriais.tutorial_config import TUTORIAIS  # Importa a lista de tutoriais

# Inicializa o pygame
pygame.init()

# Definições de cores e configuração da tela
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
HOVER_COLOR = (200, 200, 200)

def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()

# Carregar imagens
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")
icon_iniciante = pygame.image.load("./src/Images/tutoriais/rainbow.png")
icon_intermediario = pygame.image.load("./src/Images/tutoriais/fire.png")
icon_avancado = pygame.image.load("./src/Images/tutoriais/skull.png")
background_image = pygame.image.load("./src/Images/tela inicial/imagem_de_fundo.png")
return_image = pygame.image.load("./src/Images/tutoriais/return.png")

# Escalar ícones
icon_iniciante = pygame.transform.scale(icon_iniciante, (80, 80))
icon_intermediario = pygame.transform.scale(icon_intermediario, (80, 80))
icon_avancado = pygame.transform.scale(icon_avancado, (80, 80))

# Função para desenhar botões com ícones
def draw_button(icon, text, sub_text, position, tela, mouse_pos):
    x, y = position
    width, height = 700, 150
    color = HOVER_COLOR if pygame.Rect(x, y, width, height).collidepoint(mouse_pos) else BRANCO

    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 35)

    # Desenha o retângulo do botão
    pygame.draw.rect(tela, color, (x, y, width, height), border_radius=15)
    # Desenha o ícone
    tela.blit(icon, (x + 20, y + 45))
    # Renderiza o texto principal
    text_surface = font_text.render(text, True, PRETO)
    tela.blit(text_surface, (x + 120, y + 50))
    # Renderiza o subtexto
    sub_text_surface = font_sub_text.render(sub_text, True, PRETO)
    tela.blit(sub_text_surface, (x + 120, y + 90))

    return pygame.Rect(x, y, width, height)

# Tela de carregamento com animação
def loading_screen(tela):
    for _ in range(3):
        tela.fill(PRETO)
        tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))
        pygame.display.flip()
        time.sleep(0.5)

# Função para executar um tutorial
def iniciar_tutorial(tela, tutorial_name):
    if tutorial_name in TUTORIAIS:
        loading_screen(tela)
        executar_tutorial(tela, tutorial_name)
    else:
        print(f"Erro: Tutorial '{tutorial_name}' não encontrado!")

# Função principal dos módulos de aprendizado
def modulos_tutoriais(tela, altura, largura):
    running = True
    button_return_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    while running:
        tela.blit(background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Desenhar botões dos tutoriais
        btn_iniciante = draw_button(icon_iniciante, "INICIANTE", "O básico da bateria.", (largura // 2 - 350, 200), tela, mouse_pos)
        btn_intermediario = draw_button(icon_intermediario, "INTERMEDIÁRIO", "Aprendendo a sincronizar.", (largura // 2 - 350, 400), tela, mouse_pos)
        btn_avancado = draw_button(icon_avancado, "AVANÇADO", "Para quem realmente sabe manter o ritmo!", (largura // 2 - 350, 600), tela, mouse_pos)

        # Desenhar botão de retorno
        if button_return_rect.collidepoint(mouse_pos):
            tela.blit(return_image, button_return_rect.topleft)
        else:
            tela.blit(return_image, button_return_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_iniciante.collidepoint(mouse_pos):
                    iniciar_tutorial(tela, "iniciante")
                elif btn_intermediario.collidepoint(mouse_pos):
                    iniciar_tutorial(tela, "intermediario")
                elif btn_avancado.collidepoint(mouse_pos):
                    iniciar_tutorial(tela, "avancado")
                elif button_return_rect.collidepoint(mouse_pos):
                    return False

        pygame.display.flip()

    return True
