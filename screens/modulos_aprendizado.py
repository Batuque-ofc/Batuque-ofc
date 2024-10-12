import pygame
import sys
from Tutoriais.iniciante import run_batuque as run_batuque_iniciante  # Importa a função run_batuque do módulo iniciante
from Tutoriais.intermediario import run_batuque as run_batuque_intermediario  # Importa a função run_batuque do módulo intermediário
from Tutoriais.avançado import run_batuque as run_batuque_avancado  # Importa a função run_batuque do módulo avançado
import time

# Definir as cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
largura, altura = 1920, 1080

# Carregar imagens dos ícones (agora em formato PNG)
icon_iniciante = pygame.image.load("./src/Images/tutoriais/rainbow.png")
icon_intermediario = pygame.image.load("./src/Images/tutoriais/fire.png")
icon_avancado = pygame.image.load("./src/Images/tutoriais/skull.png")
background_image = pygame.image.load("./src/Images/tela inicial/imagem_de_fundo.png")
return_image = pygame.image.load("./src/Images/tutoriais/return.png")

# Carregar logo para a tela de carregamento
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")

# Redimensionar as imagens para caberem nos botões menores
icon_iniciante = pygame.transform.scale(icon_iniciante, (80, 80))
icon_intermediario = pygame.transform.scale(icon_intermediario, (80, 80))
icon_avancado = pygame.transform.scale(icon_avancado, (80, 80))

# Função para desenhar os botões dos tutoriais
def draw_button(icon, text, sub_text, position, tela):
    x, y = position
    width, height = 700, 150  # Tamanho reduzido dos botões
    
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 35)

    # Fundo do botão
    pygame.draw.rect(tela, BRANCO, (x, y, width, height), border_radius=15)
    
    # Desenhar ícone
    tela.blit(icon, (x + 20, y + 45))
    
    # Desenhar texto
    text_surface = font_text.render(text, True, PRETO)
    tela.blit(text_surface, (x + 120, y + 50))
    text_surface = font_sub_text.render(sub_text, True, PRETO)
    tela.blit(text_surface, (x + 120, y + 90))
    
    return pygame.Rect(x, y, width, height)  # Retornar a área do botão para interatividade

# Função para mostrar a tela de carregamento
def loading_screen(tela):
    tela.fill(PRETO)  # Preencher a tela com a cor preta
    tela.blit(logo_image, (largura // 3 - logo_image.get_width() // 3.5, altura // 3 - logo_image.get_height() // 3))
    pygame.display.flip()  

# Funções para os diferentes níveis de tutorial
def tutorial_iniciante(altura, largura, tela):
    loading_screen(tela)  # Exibe a tela de carregamento
    if run_batuque_iniciante(tela):  # Chama a função do módulo iniciante
        return True

def tutorial_intermediario(altura, largura, tela):
    loading_screen(tela)  # Exibe a tela de carregamento
    if run_batuque_intermediario(tela):  # Chama a função do módulo intermediário
        return True

def tutorial_avancado(altura, largura, tela):
    loading_screen(tela)  # Exibe a tela de carregamento
    if run_batuque_avancado(tela):  # Chama a função do módulo avançado
        return True

# Loop principal
def modulos_tutoriais(tela, altura, largura):
    posicao_height = (altura // 3)
    running = True

    # Definir fontes corretamente (usando uma fonte disponível no sistema)
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 40)

    button_return_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    while running:
        tela.blit(background_image, (0, 0))

        # Desenhar os botões dos tutoriais
        btn_iniciante = draw_button(icon_iniciante, "INICIANTE", "O básico da bateria.", (200, 200), tela)
        btn_intermediario = draw_button(icon_intermediario, "INTERMEDIÁRIO", "Aprendendo a sincronizar.", (200, 400), tela)
        btn_avancado = draw_button(icon_avancado, "AVANÇADO", "Para quem realmente sabe manter o ritmo!", (200, 600), tela)
        tela.blit(return_image, (50, altura - return_image.get_height() - 750))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar se o botão iniciante foi clicado
                if btn_iniciante.collidepoint(mouse_pos):
                    tutorial_iniciante(altura, largura, tela)  # Chama função do tutorial Iniciante

                # Verificar se o botão intermediário foi clicado
                if btn_intermediario.collidepoint(mouse_pos):
                    tutorial_intermediario(altura, largura, tela)  # Chama função do tutorial Intermediário

                # Verificar se o botão avançado foi clicado
                if btn_avancado.collidepoint(mouse_pos):
                    tutorial_avancado(altura, largura, tela)  # Chama função do tutorial Avançado

                if button_return_rect.collidepoint(event.pos):
                    return False

        pygame.display.flip()
