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

# Redireciona erros para o lixo
sys.stderr = open(os.devnull, 'w')

# Inicialização do Pygame
pygame.init()

# Variável de controle para o login
usuario_logado = None  # Armazena o nome do usuário logado ou None se não houver login

def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()

# Carregar imagens e sons
background_image = pygame.image.load("src/Images/tela inicial/imagem_de_fundo.png")
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")
button_play_image = pygame.image.load("src/Images/tela inicial/tocar_button.svg")
button_settings_image = pygame.image.load("src/Images/tela inicial/configuracoes_button.svg")
button_exit_image = pygame.image.load("src/Images/tela inicial/sair_button.svg")
button_login_image = pygame.image.load("src/Images/tela inicial/login_button.svg")
button_register_image = pygame.image.load("src/Images/tela inicial/register_button.svg")
button_tutorial_image = pygame.image.load("src/Images/tela inicial/tutorial_button.png")
avatar_image = pygame.image.load("src/Images/tela inicial   /avatar_padrao.svg")
avatar_image = pygame.transform.scale(avatar_image, (50, 50))  # Redimensiona o avatar

# Música de fundo
pygame.mixer.music.load("src/Images/tela inicial/drum_no_copyright.mp3")
pygame.mixer.music.set_volume(0.5)

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
button_text_color = (255, 255, 255)
button_hover_color = (255, 255, 255)

fonte_titulo = pygame.font.Font(None, 120)
mensagem_boas_vindas = fonte_titulo.render("Sinta o som do batuque!", True, BRANCO)

def draw_button(screen, image, position, hover_color, mouse_pos):
    rect = image.get_rect(center=position)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect.inflate(10, 10), border_radius=8)
    screen.blit(image, rect.topleft)
    return rect

def plot_tela_inicial():
    tela.blit(background_image, (0, 0))
    tela.blit(mensagem_boas_vindas, (largura // 2 - mensagem_boas_vindas.get_width() // 2, altura // 8))
    mouse_pos = pygame.mouse.get_pos()

    global button_play_rect, button_settings_rect, button_exit_rect, button_login_rect, button_register_rect, button_tutorial_rect, button_logout_rect
    button_play_rect = draw_button(tela, button_play_image, (largura // 2, altura - 525), button_hover_color, mouse_pos)
    button_settings_rect = draw_button(tela, button_settings_image, (largura // 2, altura - 225), button_hover_color, mouse_pos)
    button_exit_rect = draw_button(tela, button_exit_image, (largura // 2, altura - 150), button_hover_color, mouse_pos)
    button_login_rect = draw_button(tela, button_login_image, (largura // 2, altura - 450), button_hover_color, mouse_pos)
    button_register_rect = draw_button(tela, button_register_image, (largura // 2, altura - 375), button_hover_color, mouse_pos)
    button_tutorial_rect = draw_button(tela, button_tutorial_image, (largura // 2, altura - 300), button_hover_color, mouse_pos)

    # Exibir avatar e nome do usuário logado, se houver login
    if usuario_logado:
        tela.blit(avatar_image, (largura - 70, 10))  # Exibir avatar no canto superior direito
        fonte_usuario = pygame.font.Font(None, 40)
        nome_usuario = fonte_usuario.render(usuario_logado, True, BRANCO)
        tela.blit(nome_usuario, (largura - 140, 20))

        # Criar botão de logout
        button_logout_rect = pygame.Rect(largura - 140, 70, 100, 30)
        pygame.draw.rect(tela, (200, 0, 0), button_logout_rect, border_radius=5)
        logout_text = fonte_usuario.render("Logout", True, BRANCO)
        tela.blit(logout_text, (largura - 130, 75))

    pygame.display.flip()

def loading_screen(loading_progress):
    tela.fill(PRETO)
    tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))
    pygame.draw.rect(tela, BRANCO, (100, altura - 50, loading_progress * (largura - 200), 20))
    pygame.display.flip()

def tocar(screen, largura, altura):
    pygame.mixer.music.stop()  # Para a música de fundo antes de iniciar o batuque
    tempo_carregamento = 4
    tempo_inicial = time.time()

    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        loading_progress = min(tempo_decorrido / tempo_carregamento, 1)
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
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                menu_aberto = not menu_aberto
                if menu_aberto:
                    configuracoes(screen)
                else:
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

    camera.release()
    main()

def sair():
    pygame.quit()
    sys.exit()

def main():
    global usuario_logado
    plot_tela_inicial()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_play_rect.collidepoint(event.pos):
                    tocar(tela, largura, altura)
                elif button_settings_rect.collidepoint(event.pos):
                    if not configuracoes(tela):
                        plot_tela_inicial()
                elif button_login_rect.collidepoint(event.pos) and not usuario_logado:
                    usuario_logado = telaLogin.login(tela, altura, largura)
                    plot_tela_inicial()
                elif button_register_rect.collidepoint(event.pos):
                    telaRegistro.registrar(tela, altura, largura)
                    plot_tela_inicial()
                elif button_exit_rect.collidepoint(event.pos):
                    sair()
                elif button_tutorial_rect.collidepoint(event.pos):
                    modulos_tutoriais(tela, altura, largura)
                    plot_tela_inicial()
                elif usuario_logado and button_logout_rect.collidepoint(event.pos):
                    usuario_logado = None  # Realiza o logout
                    plot_tela_inicial()

        plot_tela_inicial()

if __name__ == "__main__":
    main()

pygame.quit()
