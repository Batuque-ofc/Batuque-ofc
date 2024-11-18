import sys
import numpy as np
import cv2
import time
from pygame import mixer
import pygame
import math
from screens import configuracoes

pygame.init()

# Definir as dimensões da tela
def criar_tela():
    largura = pygame.display.Info().current_w
    altura = pygame.display.Info().current_h
    tela = pygame.display.set_mode((largura, altura), pygame.SCALED)
    return tela, largura, altura

tela, largura, altura = criar_tela()

# Carregar sons
drum_sounds = [
    mixer.Sound('src/sounds/Chimbal/Chimbal.mp3'),
    mixer.Sound('src/sounds/Caixa/Caixa.mp3'),
    mixer.Sound('src/sounds/Bumbo/Bumbo.wav'),
    mixer.Sound('src/sounds/Crash/Crash.mp3'),
    mixer.Sound('src/sounds/Caixa2/Caixa2.mp3')
]

# Definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (0, 0, 255)

def draw_pulsating_effect(frame, roi, border_color, center_color=(128, 128, 128), intensity=1.0, time_left=1.0, duration=10, thickness=5):
    top_x, top_y, bottom_x, bottom_y = roi
    center = (int((top_x + bottom_x) / 2), int((top_y + bottom_y) / 2))
    radius = int(min(bottom_x - top_x, bottom_y - top_y) / 2)

    # Pulsação baseada no tempo restante
    pulse = 0.5 + 0.5 * math.sin((1 - time_left / duration) * 2 * math.pi * 3)
    adjusted_intensity = intensity * pulse

    # Criar uma camada sobreposta
    overlay = frame.copy()

    # Desenhar o círculo interno preenchido com a cor cinza
    cv2.circle(
        overlay,
        center,
        radius - thickness,
        center_color,
        -1  # Círculo preenchido
    )

    # Desenhar o círculo externo (apenas borda)
    cv2.circle(
        overlay,
        center,
        radius,
        border_color,
        thickness  # Espessura da borda
    )

    # Mesclar o efeito com o quadro original
    cv2.addWeighted(overlay, adjusted_intensity, frame, 1 - adjusted_intensity, 0, frame)

def calc_mask(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower, upper)

def find_pink_centers(mask, min_area=100):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []

    for contour in contours:
        if cv2.contourArea(contour) > min_area:  # Ignorar áreas pequenas
            M = cv2.moments(contour)
            if M["m00"] > 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                centers.append((center_x, center_y))

    return centers

# Função para desenhar o efeito de tocha (rastros que diminuem de tamanho)
def draw_torch_effect(frame, baqueta_position, centers, effect_color=(0, 0, 255), max_length=100, alpha=0.5, max_radius=7):
    overlay = frame.copy()

    # Limitar a quantidade de pontos para o rastro
    max_points = max_length
    if len(centers) > max_points:
        centers = centers[-max_points:]

    # Desenhar círculos de rastro com efeito de tocha
    for i, center in enumerate(centers):
        # Calcular a distância da baqueta à esfera
        distance = math.sqrt((center[0] - baqueta_position[0])**2 + (center[1] - baqueta_position[1])**2)

        # Ajustar a fórmula para controlar o tamanho dos círculos
        radius = max(7, max_radius - int(distance / 15))  # O raio diminui com a distância, ajustado para uma transição mais suave
        alpha_value = alpha * (i / len(centers))  # Graduação de transparência

        # Desenhar o círculo diminuindo de tamanho
        cv2.circle(overlay, center, radius, effect_color, -1)

    # Mesclar o rastro com o frame
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

def run_batuque(screen):
    h_low, h_high = 146, 172
    s_low, s_high = 116, 255
    v_low, v_high = 123, 255
    pinkLower = (h_low, s_low, v_low)
    pinkUpper = (h_high, s_high, v_high)

    last_played_time = [0, 0, 0, 0, 0]
    cooldown = 0.5  # Tempo em segundos entre toques
    sound_played = [False, False, False, False, False]

    def state_machine(sound_index):
        current_time = time.time()
        if current_time - last_played_time[sound_index] >= cooldown:
            drum_sounds[sound_index].play()
            last_played_time[sound_index] = current_time
            sound_played[sound_index] = True

    def calc_mask(frame, lower, upper):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, lower, upper)

    def ROI_analysis(roi, sound_index, lower, upper, min_value=30):
        mask = calc_mask(roi, lower, upper)
        summation = np.sum(mask)

        if summation >= min_value:
            if not sound_played[sound_index]:
                state_machine(sound_index)
        else:
            sound_played[sound_index] = False

        return mask

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

    if not camera.isOpened():
        print("Erro ao abrir a câmera")
        sys.exit()

    instruments = ['Chimbal.png', 'Caixa.png', 'Bumbo.png', 'Crash.png', 'Caixa2.png']
    instrument_images = []

    for img in instruments:
        image = cv2.imread(f'./src/Images/{img}', cv2.IMREAD_UNCHANGED)
        if image is None:
            print(f"Erro ao carregar imagem: {img}")
        else:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            image = cv2.flip(image, 1)
            instrument_images.append(cv2.resize(image, (200, 150), interpolation=cv2.INTER_CUBIC))

    H, W = 1080, 1920
    centers = [
        (int(H * 0.4), int(W * 0.1)),  # Chimbal
        (int(H * 0.6), int(W * 0.6)),  # Caixa
        (int(H * 0.7), int(W * 0.4)),  # Bumbo
        (int(H * 0.4), int(W * 0.7)),  # Crash
        (int(H * 0.6), int(W * 0.2))   # Caixa espelhada
    ]

    sizes = [(150, 200), (150, 200), (200, 200), (150, 200), (150, 200)]
    ROIs = [(center[0] - size[0] // 2, center[1] - size[1] // 2, center[0] + size[0] // 2, center[1] + size[1] // 2) for center, size in zip(centers, sizes)]

    running = True
    effect_timers = [0] * len(ROIs)
    trail_centers = []
    baqueta_position = (int(largura / 2), int(altura / 2))
    max_trail_length = 50

    while running:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, (altura, largura))

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
                roi = frame[top_y:bottom_y, top_x:bottom_x]
                mask = ROI_analysis(roi, i, pinkLower, pinkUpper)

        mask = calc_mask(frame, pinkLower, pinkUpper)

        pink_centers = find_pink_centers(mask)

        # Adicionar novas esferas à lista de rastro
        for center in pink_centers:
            if center not in trail_centers:
                trail_centers.append({'center': center, 'age': 0})  # 'age' controla quanto tempo a esfera fica na tela

        # Atualizar a idade das esferas e remover as mais antigas
        for entry in trail_centers[:]:
            entry['age'] += 1
            if entry['age'] > max_trail_length:  # Se uma esfera ficou tempo suficiente sem ser detectada, ela será removida
                trail_centers.remove(entry)

        # Desenhar o rastro com efeito de tocha
        trail_positions = [entry['center'] for entry in trail_centers]  # Pega só as posições
        draw_torch_effect(frame, baqueta_position, trail_positions, effect_color=VERMELHO)  # Efeito de tocha com rastro vermelho

        # Para cada baqueta, verificar se está sendo detectada
        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            if np.sum(calc_mask(roi, pinkLower, pinkUpper)) > 30:
                effect_timers[i] = 7
            else:
                effect_timers[i] = max(0, effect_timers[i] - 1)

            # Desenha o efeito pulsante (quando a baqueta está detectada)
            if effect_timers[i] > 0:
                draw_pulsating_effect(
                    frame,
                    (top_x, top_y, bottom_x, bottom_y),
                    border_color=(255, 0, 255),
                    intensity=1.0,
                    time_left=effect_timers[i],
                    duration=7
                )

            # Desenha as imagens dos instrumentos
            overlay = instrument_images[i]
            overlay_resized = cv2.resize(overlay, (bottom_x - top_x, bottom_y - top_y))

            if overlay_resized.shape[2] == 4:
                b, g, r, a = cv2.split(overlay_resized)
                overlay_rgb = cv2.merge((b, g, r))
                alpha = a / 255.0
                for c in range(0, 3):
                    frame[top_y:bottom_y, top_x:bottom_x, c] = (
                        alpha * overlay_rgb[:, :, c] +
                        (1 - alpha) * frame[top_y:bottom_y, top_x:bottom_x, c]
                    )

        # Converte para RGB e atualiza a tela com o efeito
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if in_settings:
                    in_settings = False
                else:
                    in_settings = configuracoes.configuracoes(screen)

        running = True
        in_settings = False
        while running:
            if not in_settings:
                ret, frame = camera.read()
                if not ret:
                    break

                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame = cv2.resize(frame, (altura, largura))

                for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
                    roi = frame[top_y:bottom_y, top_x:bottom_x]
                    mask = ROI_analysis(roi, i, pinkLower, pinkUpper)

                for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
                    roi = frame[top_y:bottom_y, top_x:bottom_x]
                    overlay = instrument_images[i]
                    overlay_resized = cv2.resize(overlay, (roi.shape[1], roi.shape[0]))

                    if overlay_resized.shape[2] == 4:
                        b, g, r, a = cv2.split(overlay_resized)
                        overlay_rgb = cv2.merge((b, g, r))
                        alpha_mask = a / 255.0 * 0.5
                        alpha_inv = 1.0 - alpha_mask

                        for c in range(0, 3):
                            frame[top_y:bottom_y, top_x:bottom_x, c] = (alpha_mask * overlay_rgb[:, :, c] +
                                                                        alpha_inv * frame[top_y:bottom_y, top_x:bottom_x, c])
                    else:
                        frame[top_y:bottom_y, top_x:bottom_x] = cv2.addWeighted(overlay_resized, 0.5, roi, 0.5, 0)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(frame)
                screen.blit(frame_surface, (0, 0))
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if in_settings:
                        in_settings = False
                    else:
                        in_settings = configuracoes.configuracoes(screen)

    camera.release()
    pygame.quit()
