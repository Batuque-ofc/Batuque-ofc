import sys
import numpy as np
import cv2
import time
import pygame
from pygame import mixer
from screens.configuracoes import configuracoes
from Tutoriais.tutorial_config import TUTORIAIS

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
    pulse = 0.5 + 0.5 * np.sin((1 - time_left / duration) * 2 * np.pi * 3)
    adjusted_intensity = intensity * pulse

    # Criar uma camada sobreposta
    overlay = frame.copy()

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

def executar_tutorial(screen, tutorial_name):
    if tutorial_name not in TUTORIAIS:
        print(f"Tutorial {tutorial_name} não encontrado.")
        return

    tutorial_data = TUTORIAIS[tutorial_name]
    music = tutorial_data["music"]
    Bumbo_times = tutorial_data["Bumbo_times"]
    Caixa_times = tutorial_data["Caixa_times"]
    Chimbal_times = tutorial_data["Chimbal_times"]

    mixer.init()
    mixer.music.load(music)
    mixer.music.play()

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
    return_to_menu = False

    scaling_factors = [1.0] * len(instrument_images)
    scaling_speed = 0.1
    impact_scale = 0.7

    def apply_animation_effect(index):
        scaling_factors[index] = impact_scale

    effect_timers = [0] * len(ROIs)
    score = 0
    font = pygame.font.Font(None, 60)
    floating_texts = []

    restart_button_rect = pygame.Rect(largura - 200, 50, 150, 50)

    while running:
        ret, frame = camera.read()
        if not ret:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if configuracoes(screen):
                    return_to_menu = True
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    score = 0
                    floating_texts.clear()

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, (altura, largura))

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            mask = calc_mask(roi, (146, 116, 123), (172, 255, 255))

            if np.sum(mask) > 30:
                effect_timers[i] = 7
                apply_animation_effect(i)
                score += 1
                floating_texts.append({"text": "+1", "pos": (top_x, top_y), "time": time.time()})

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            center_x, center_y = centers[i]
            size_x, size_y = sizes[i]

            scaling_factors[i] = min(1.0, scaling_factors[i] + scaling_speed)

            new_width = int(size_x * scaling_factors[i])
            new_height = int(size_y * scaling_factors[i])

            new_width = max(1, new_width)
            new_height = max(1, new_height)

            scaled_overlay = cv2.resize(instrument_images[i], (new_width, new_height), interpolation=cv2.INTER_CUBIC)

            new_top_x = max(0, center_x - new_width // 2)
            new_top_y = max(0, center_y - new_height // 2)
            new_bottom_x = min(frame.shape[1], center_x + new_width // 2)
            new_bottom_y = min(frame.shape[0], center_y + new_height // 2)

            roi_height = new_bottom_y - new_top_y
            roi_width = new_bottom_x - new_top_x

            if scaled_overlay.shape[2] == 4:
                b, g, r, a = cv2.split(scaled_overlay)
                overlay_rgb = cv2.merge((b, g, r))
                alpha_mask = a / 255.0 * 0.5

                overlay_rgb = cv2.resize(overlay_rgb, (roi_width, roi_height))
                alpha_mask = cv2.resize(alpha_mask, (roi_width, roi_height))

                for c in range(3):
                    frame[new_top_y:new_bottom_y, new_top_x:new_bottom_x, c] = (
                            overlay_rgb[:, :, c] * alpha_mask +
                            frame[new_top_y:new_bottom_y, new_top_x:new_bottom_x, c] * (1 - alpha_mask)
                    )
            else:
                frame[new_top_y:new_bottom_y, new_top_x:new_bottom_x] = cv2.addWeighted(
                    scaled_overlay, 0.5, frame[new_top_y:new_bottom_y, new_top_x:new_bottom_x], 0.5, 0
                )

        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            if np.sum(calc_mask(roi, (146, 116, 123), (172, 255, 255))) > 30:
                effect_timers[i] = 7
            else:
                effect_timers[i] = max(0, effect_timers[i] - 1)

            if effect_timers[i] > 0:
                draw_pulsating_effect(
                    frame,
                    (top_x, top_y, bottom_x, bottom_y),
                    border_color=(255, 0, 255),
                    intensity=1.0,
                    time_left=effect_timers[i],
                    duration=7
                )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        screen.blit(frame_surface, (0, 0))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (50, 50))

        current_time = time.time()
        for text in floating_texts[:]:
            if current_time - text["time"] > 1.0:
                floating_texts.remove(text)
            else:
                rendered_text = font.render(text["text"], True, (0, 255, 0))
                text_pos = (text["pos"][0] - 20, text["pos"][1] - int(50 * (current_time - text["time"])))
                screen.blit(rendered_text, text_pos)

        pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
        restart_text = font.render("Reiniciar", True, (255, 255, 255))
        screen.blit(restart_text, (largura - 185, 60))

        pygame.display.flip()

    camera.release()
    return return_to_menu

if __name__ == "__main__":
    screen = pygame.display.set_mode((largura, altura))
    executar_tutorial(screen, "iniciante")
