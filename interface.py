import os
import sys
import time
import pygame
import cv2
from itertools import cycle
from pygame.locals import *
from batuque import run_batuque
import screens.telaLogin as telaLogin
import screens.telaRegistro as telaRegistro
from screens.configuracoes import configuracoes
from screens.modulos_aprendizado import modulos_tutoriais

sys.stderr = open(os.devnull, 'w')

pygame.init()


def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()


background_image = pygame.image.load("src/Images/tela inicial/imagem_de_fundo.png")
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")
button_play_image = pygame.image.load("src/Images/tela inicial/tocar_button.svg")
button_settings_image = pygame.image.load("src/Images/tela inicial/configuracoes_button.svg")
button_exit_image = pygame.image.load("src/Images/tela inicial/sair_button.svg")
button_login_image = pygame.image.load("src/Images/tela inicial/login_button.svg")
button_registrar_image = pygame.image.load("src/Images/tela inicial/register_button.svg")
button_tutorial_image = pygame.image.load("src/Images/tela inicial/tutorial_button.png")


pygame.mixer.music.load("src/Images/tela inicial/drum_no_copyright.mp3")
pygame.mixer.music.set_volume(0.2)


PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)


fonte = pygame.font.Font(None, 145)
mensagem_boas_vindas = fonte.render("Sinta o som do batuque!", True, BRANCO)

def plot_tela_inicial():
    """Desenha a tela inicial do jogo."""
    tela.blit(background_image, (0, 0))
    tela.blit(button_play_image, (largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
    tela.blit(button_settings_image, (largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
    tela.blit(button_exit_image, (largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
    tela.blit(mensagem_boas_vindas, (largura // 2 - mensagem_boas_vindas.get_width() // 2, altura // 8))
    tela.blit(button_login_image, (largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 450))
    tela.blit(button_registrar_image, (largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 375))
    tela.blit(button_tutorial_image, (largura // 2 - button_tutorial_image.get_width() // 2, altura - button_tutorial_image.get_height() - 300))
    pygame.display.flip()

def loading_screen(loading_progress):
    """Desenha a tela de carregamento com a barra de progresso."""
    tela.fill(PRETO)
    tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))
    pygame.draw.rect(tela, BRANCO, (100, altura - 50, loading_progress * (largura - 200), 20))
    pygame.display.flip()

def tocar(screen, largura, altura):
    tempo_carregamento = 4
    tempo_inicial = time.time()
    

    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        loading_progress = min(tempo_decorrido / tempo_carregamento, 1)  # Garantir que o progresso não exceda 1
        loading_screen(loading_progress)
        if tempo_decorrido >= tempo_carregamento:
            break


    camera = cv2.VideoCapture(0)
    
    clock = pygame.time.Clock()
    frame = cycle(run_batuque(screen))
    menu_aberto = False
    voltar_ao_menu_principal = False

    while not voltar_ao_menu_principal:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu_aberto = not menu_aberto
                    if menu_aberto:
                        configuracoes(screen)
                    else:
                        voltar_ao_menu_principal = True
            elif event.type == MOUSEBUTTONDOWN and menu_aberto:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 400 and 400 <= mouse_pos[1] <= 450:
                    menu_aberto = False
                    voltar_ao_menu_principal = True

        if not menu_aberto:
            ret, frame = camera.read()
            if not ret:
                break


            resized_frame = cv2.resize(frame, (1080, 1920))

            screen.fill(PRETO)
            frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()
            clock.tick(30)

        if menu_aberto and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_aberto = False

    camera.release()
    main()

def sair():
    pygame.quit()
    sys.exit()

def main():

    plot_tela_inicial()
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_play_rect = button_play_image.get_rect(topleft=(largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
                button_settings_rect = button_settings_image.get_rect(topleft=(largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
                button_exit_rect = button_exit_image.get_rect(topleft=(largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
                button_login_rect = button_login_image.get_rect(topleft=(largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 450))
                button_registrar_rect = button_registrar_image.get_rect(topleft=(largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 375))
                button_tutorial_rect = button_tutorial_image.get_rect(topleft=(largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))
                
                if button_play_rect.collidepoint(event.pos):
                    tocar(tela, largura, altura)
                elif button_settings_rect.collidepoint(event.pos):
                    if not configuracoes(tela):
                        plot_tela_inicial()
                elif button_login_rect.collidepoint(event.pos):
                    logado = telaLogin.login(tela, altura, largura)
                    if logado:
                        tocar(tela, largura, altura)
                    main()
                elif button_registrar_rect.collidepoint(event.pos):
                    telaRegistro.registrar(tela, altura, largura)
                    main()
                elif button_exit_rect.collidepoint(event.pos):
                    sair()
                elif button_tutorial_rect.collidepoint(event.pos):
                    modulos_tutoriais(tela, altura, largura)
                    main()
                

        pygame.display.flip()


if __name__ == "__main__":
    main()

pygame.quit()