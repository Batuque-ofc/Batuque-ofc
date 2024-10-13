import pygame
import sys
from Tutoriais.iniciante import run_batuque as run_batuque_iniciante
from Tutoriais.intermediario import run_batuque as run_batuque_intermediario
from Tutoriais.avançado import run_batuque as run_batuque_avancado
import time

pygame.init()

def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()


logo_image = pygame.image.load("src/Images/tela inicial/logo.png")


PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)


icon_iniciante = pygame.image.load("./src/Images/tutoriais/rainbow.png")
icon_intermediario = pygame.image.load("./src/Images/tutoriais/fire.png")
icon_avancado = pygame.image.load("./src/Images/tutoriais/skull.png")
background_image = pygame.image.load("./src/Images/tela inicial/imagem_de_fundo.png")
return_image = pygame.image.load("./src/Images/tutoriais/return.png")
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")


icon_iniciante = pygame.transform.scale(icon_iniciante, (80, 80))
icon_intermediario = pygame.transform.scale(icon_intermediario, (80, 80))
icon_avancado = pygame.transform.scale(icon_avancado, (80, 80))


def draw_button(icon, text, sub_text, position, tela):
    x, y = position
    width, height = 700, 150
    
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 35)


    pygame.draw.rect(tela, BRANCO, (x, y, width, height), border_radius=15)
    

    tela.blit(icon, (x + 20, y + 45))
    

    text_surface = font_text.render(text, True, PRETO)
    tela.blit(text_surface, (x + 120, y + 50))
    text_surface = font_sub_text.render(sub_text, True, PRETO)
    tela.blit(text_surface, (x + 120, y + 90))
    
    return pygame.Rect(x, y, width, height) 

def loading_screen(tela):
    tela.fill(PRETO)
    tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))
    pygame.display.flip()


def tutorial_iniciante(altura, largura, tela):
    loading_screen(tela)
    if run_batuque_iniciante(tela): 
        return True

def tutorial_intermediario(altura, largura, tela):
    loading_screen(tela) 
    if run_batuque_intermediario(tela): 
        return True

def tutorial_avancado(altura, largura, tela):
    loading_screen(tela)
    if run_batuque_avancado(tela):
        return True

def modulos_tutoriais(tela, altura, largura):
    posicao_height = (altura // 3)
    running = True

  
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 40)

    button_return_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    while running:
        tela.blit(background_image, (0, 0))

  
        btn_iniciante = draw_button(icon_iniciante, "INICIANTE", "O básico da bateria.", (200, 200), tela)
        btn_intermediario = draw_button(icon_intermediario, "INTERMEDIÁRIO", "Aprendendo a sincronizar.", (200, 400), tela)
        btn_avancado = draw_button(icon_avancado, "AVANÇADO", "Para quem realmente sabe manter o ritmo!", (200, 600), tela)
        tela.blit(return_image, (50, altura - return_image.get_height() - 750))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

             
                if btn_iniciante.collidepoint(mouse_pos):
                    tutorial_iniciante(altura, largura, tela)

              
                if btn_intermediario.collidepoint(mouse_pos):
                    tutorial_intermediario(altura, largura, tela) 

              
                if btn_avancado.collidepoint(mouse_pos):
                    tutorial_avancado(altura, largura, tela) 

                if button_return_rect.collidepoint(event.pos):
                    return False

        pygame.display.flip()
