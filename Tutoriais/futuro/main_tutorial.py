import sys
import numpy as np
import cv2
import time
import pygame
from pygame import mixer
from tutorial_config import tutorials

# Inicialização do pygame
pygame.init()

# Configurações gerais
largura, altura = 1920, 1080
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Funções reutilizáveis
def init_camera():
    """Inicializa a câmera."""
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
    if not camera.isOpened():
        raise IOError("Erro ao abrir a câmera")
    return camera

def carregar_instrumentos(img_paths, sizes):
    """Carrega as imagens dos instrumentos."""
    instrumentos = []
    for img, size in zip(img_paths, sizes):
        image = cv2.imread(f'./src/Images/{img}', cv2.IMREAD_UNCHANGED)
        if image is None:
            print(f"Erro ao carregar imagem: {img}")
        else:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            image = cv2.flip(image, 1)
            instrumentos.append(cv2.resize(image, (size[1], size[0]), interpolation=cv2.INTER_CUBIC))
    return instrumentos

def desenhar_batidas(current_time, times, center, frame):
    """Desenha os círculos de batida sincronizados."""
    for beat_time in times:
        if abs(current_time - beat_time) < 0.1:
            radius = int(50 + 50 * (1 - abs(current_time - beat_time) / 0.1))
            cv2.circle(frame, center, radius, (255, 0, 255), -1)

def executar_tutorial(screen, tutorial_data):
    """Executa o tutorial com base nos dados fornecidos."""
    music = tutorial_data["music"]
    Bumbo_times = tutorial_data["Bumbo_times"]
    Caixa_times = tutorial_data["Caixa_times"]
    Chimbal_times = tutorial_data["Chimbal_times"]

    # Inicializar música
    mixer.init()
    mixer.music.load(music)
    mixer.music.play(-1)

    # Inicializar câmera
    camera = init_camera()

    # Carregar instrumentos
    img_paths = ['Chimbal.png', 'Caixa.png', 'Bumbo.png', 'Crash.png', 'Caixa2.png']
    sizes = [(150, 200), (150, 200), (200, 200), (150, 200), (150, 200)]
    instrument_images = carregar_instrumentos(img_paths, sizes)

    centers = [
        (int(altura * 0.4), int(largura * 0.1)),  # Chimbal
        (int(altura * 0.6), int(largura * 0.6)),  # Caixa
        (int(altura * 0.7), int(largura * 0.4)),  # Bumbo
    ]

    start_time = time.time()
    running = True

    try:
        while running:
            ret, frame = camera.read()
            if not ret:
                continue

            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.resize(frame, (altura, largura))
            current_time = time.time() - start_time

            # Sincronizar batidas
            desenhar_batidas(current_time, Bumbo_times, centers[2], frame)
            desenhar_batidas(current_time, Caixa_times, centers[1], frame)
            desenhar_batidas(current_time, Chimbal_times, centers[0], frame)

            # Mostrar frame na tela do pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame)
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

    finally:
        camera.release()
        mixer.music.stop()
        pygame.quit()
        cv2.destroyAllWindows()

# Código principal
if __name__ == "__main__":
    # Escolha do tutorial
    screen = pygame.display.set_mode((largura, altura))
    tutorial_choice = "avancado"  # Modifique para escolher o tutorial
    tutorial_data = tutorials[tutorial_choice]
    executar_tutorial(screen, tutorial_data)
