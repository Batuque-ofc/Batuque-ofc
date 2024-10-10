import time
import pygame
import sys
from itertools import cycle
from pygame.locals import *
import cv2
from batuque import run_batuque
import screens.telaLogin as telaLogin
import screens.telaRegistro as telaRegistro
import screens.menu_volume as menu_volume
import screens.menu_resolucao as menu_resolucao
from screens.configuracoes import configuracoes

pygame.init()

# Definir as dimensões da janela
def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()

# Carregar imagens
background_image = pygame.image.load("src/Images/tela inicial/imagem_de_fundo.png")
logo_image = pygame.image.load("src/Images/tela inicial/logo.png")
button_play_image = pygame.image.load("src/Images/tela inicial/tocar_button.svg")
button_settings_image = pygame.image.load("src/Images/tela inicial/configuracoes_button.svg")
button_exit_image = pygame.image.load("src/Images/tela inicial/sair_button.svg")
button_login_image = pygame.image.load("src/Images/tela inicial/login_button.svg")
button_registrar_image = pygame.image.load("src/Images/tela inicial/register_button.svg")

# Carregar música
pygame.mixer.music.load("src/Images/tela inicial/drum_no_copyright.mp3")
pygame.mixer.music.set_volume(0.2)

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Definir fonte para a mensagem de boas-vindas
fonte = pygame.font.Font(None, 145)
mensagem_boas_vindas = fonte.render("Sinta o som do batuque!", True, BRANCO)

def plot_tela_inicial():
    """Desenha a tela inicial do jogo."""
    tela.blit(background_image, (0, 0))
    tela.blit(button_play_image, (largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
    tela.blit(button_settings_image, (largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
    tela.blit(button_exit_image, (largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
    tela.blit(mensagem_boas_vindas, (largura // 2 - mensagem_boas_vindas.get_width() // 2, altura // 8))
    tela.blit(button_login_image, (largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 375))
    tela.blit(button_registrar_image, (largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))
    pygame.display.flip()

def loading_screen(loading_progress):
    """Desenha a tela de carregamento com a barra de progresso."""
    tela.fill(PRETO)
    tela.blit(logo_image, (largura // 2 - logo_image.get_width() // 2, altura // 2 - logo_image.get_height() // 2))
    pygame.draw.rect(tela, BRANCO, (100, altura - 50, loading_progress * (largura - 200), 20))
    pygame.display.flip()

def tocar(screen, largura, altura):
    """Inicia a tela do jogo e exibe o vídeo com opções de menu."""
    pygame.mixer.music.stop()  # Parar a música antes de iniciar
    tempo_carregamento = 4
    tempo_inicial = time.time()

    # Tela de carregamento
    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        loading_progress = min(tempo_decorrido / tempo_carregamento, 1)  # Garantir que o progresso não exceda 1
        loading_screen(loading_progress)
        if tempo_decorrido >= tempo_carregamento:
            break

    pygame.time.wait(2000)

    # Inicializar a câmera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erro ao abrir a câmera")
        return

    clock = pygame.time.Clock()
    frames = cycle(run_batuque(screen))  # Aqui você passa a tela para run_batuque
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
                print("Erro ao capturar imagem da câmera")
                continue

            # Redimensionar para 1080x1920 (horizontal)
            resized_frame = cv2.resize(frame, (1080, 1920))

            screen.fill(PRETO)
            frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()
            clock.tick(30)

        if menu_aberto and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            menu_aberto = False

    camera.release()  # Liberar a câmera
    main()


def sair():
    """Encerra o Pygame e sai do programa."""
    pygame.quit()
    sys.exit()

def main():
    """Função principal que inicia a tela inicial e gerencia eventos do usuário."""
    plot_tela_inicial()
    pygame.mixer.music.play(-1)  # Loop infinito

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_play_rect = button_play_image.get_rect(topleft=(largura // 2 - button_play_image.get_width() // 2, altura - button_play_image.get_height() - 225))
                button_settings_rect = button_settings_image.get_rect(topleft=(largura // 2 - button_settings_image.get_width() // 2, altura - button_settings_image.get_height() - 150))
                button_exit_rect = button_exit_image.get_rect(topleft=(largura // 2 - button_exit_image.get_width() // 2, altura - button_exit_image.get_height() - 75))
                button_login_rect = button_login_image.get_rect(topleft=(largura // 2 - button_login_image.get_width() // 2, altura - button_login_image.get_height() - 375))
                button_registrar_rect = button_registrar_image.get_rect(topleft=(largura // 2 - button_registrar_image.get_width() // 2, altura - button_registrar_image.get_height() - 300))

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

        pygame.display.flip()

# Executar o programa
if __name__ == "__main__":
    main()

# Encerrar o Pygame
pygame.quit()

