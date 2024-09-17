import sys
import numpy as np
import cv2
import time
from pygame import mixer

# Configurações de cor para detecção
h_low, h_high = 146, 172
s_low, s_high = 116, 255
v_low, v_high = 123, 255
pinkLower = (h_low, s_low, v_low)
pinkUpper = (h_high, s_high, v_high)

# Configurações da música
mixer.init()
mixer.music.load('src/sounds/Tutorial 2.wav')

def init_mixer_and_play_music(music):
    mixer.init()
    mixer.music.load(music)
    mixer.music.play()
    print("Música iniciada:", music)

# Tutorial (iniciante) - Tempo das batidas (em segundos)

#Bumbo_times = [2.75, 3.10, 4.25, 4.55, 5.65, 6, 7.1, 7.5, 8.6, 9, 10.10, 10.47, 11.6, 12, 13.10, 13.45]
#Caixa_times = [3.45, 4.9, 6.35, 7.9, 9.37, 10.87, 12.30, 13.80]

# Tutorial (intermediario e avançado) - comente o bumbo para intermediario.

Bumbo_times = [2.6, 3, 4.1, 4.4, 5.6, 5.9, 7, 7.4, 8.5, 8.9, 10, 10.35, 11.4, 11.8, 12.7, 13.1, 14.3, 14.7, 15.8, 16.2, 17.3, 17.65, 18.75, 19.1, 20.2, 20.6, 21.7, 22.1, 23.1, 23.5, 24.55, 24.95, 26.05, 26.4, 27.45, 27.85, 28.95, 29.3, 30.35, 30.65, 31.87, 32.25, 33.35, 33.75, 34.85, 35.25]
Caixa_times = [3.35, 4.8, 6.3, 7.8, 9.2, 10.7, 12.1, 13.6, 15.1, 16.5, 18.05, 19.5, 20.95, 22.4, 23.8, 25.3, 26.7, 28.2, 29.65, 31.15, 32.65, 34.1, 35.55]
Chimbal_times = [2.7, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.8, 6.2, 6.6, 7.0, 7.4, 7.8, 8.2, 8.6, 9.0, 9.4, 9.8, 10.2, 10.6, 11.0, 11.4, 11.8, 12.2, 12.6, 13.0, 13.4, 13.8, 14.2, 14.6, 15.0, 15.4, 15.8, 16.2, 16.6, 17.0, 17.4, 17.8, 18.2, 18.6, 19.0, 19.4, 19.8, 20.2, 20.6, 21.0, 21.4, 21.8, 22.2, 22.6, 23.0, 23.4, 23.8, 24.2, 24.6, 25.0, 25.4, 25.8, 26.2, 26.6, 27.0, 27.4, 27.8, 28.2, 28.6, 29.0, 29.4, 29.8, 30.2, 30.6, 31.0, 31.4, 31.8, 32.2, 32.6, 33.0, 33.4, 33.8, 34.2, 34.6, 35.0]

def run_batuque():
    width = 1920
    height = 1080

    last_played_time = [0, 0, 0, 0, 0]
    cooldown = 0.5  # Tempo em segundos entre toques

    # Estado para verificar se o som já foi tocado
    sound_played = [False, False, False, False, False]

    drum_sounds = [
        mixer.Sound('src/sounds/Chimbal/Chimbal.mp3'),
        mixer.Sound('src/sounds/Caixa/Caixa.mp3'),
        mixer.Sound('src/sounds/Bumbo/Bumbo.wav'),
        mixer.Sound('src/sounds/Crash/Crash.mp3'),
        mixer.Sound('src/sounds/Caixa2/Caixa2.mp3')
    ]

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
        
        # Checar se o objeto está na hit box
        if summation >= min_value:
            if not sound_played[sound_index]:
                state_machine(sound_index)
        else:
            sound_played[sound_index] = False

        return mask

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not camera.isOpened():
        print("Erro ao abrir a câmera")
        sys.exit()

    # Adiciona as imagens dos instrumentos
    instruments = ['Chimbal.png', 'Caixa.png', 'Bumbo.png', 'Crash.png', 'Caixa2.png']
    instrument_images = [cv2.imread(f'./src/Images/{img}', cv2.IMREAD_UNCHANGED) for img in instruments]
    instrument_images[1] = cv2.resize(instrument_images[1], (200, 150), interpolation=cv2.INTER_CUBIC)  # Redimensionar Caixa
    instrument_images[4] = cv2.resize(instrument_images[4], (200, 150), interpolation=cv2.INTER_CUBIC)  # Redimensionar Caixa espelhada

    H, W = 720, 1280
    centers = [
        (W * 1 // 8, H * 4 // 8),  # Chimbal
        (W * 6 // 8, H * 6 // 8),  # Caixa
        (W * 4 // 8, H * 7 // 8),  # Bumbo
        (W * 7 // 8, H * 4 // 8),  # Crash
        (W * 2 // 8, H * 6 // 8)   # Caixa espelhada
    ]
    sizes = [(200, 200), (200, 150), (200, 200), (200, 200), (200, 150)]

    ROIs = [(center[0] - size[0] // 2, center[1] - size[1] // 2, center[0] + size[0] // 2, center[1] + size[1] // 2) for center, size in zip(centers, sizes)]

    # Inicia a música assim que a tela carrega
    init_mixer_and_play_music('src/sounds/Tutorial 2.wav')

    start_time = time.time()

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erro ao capturar imagem da câmera")
            break
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, 'Projeto: Batuque', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (20, 20, 20), 2)
        current_time = time.time() - start_time

        # Desenhar as imagens dos instrumentos nas ROIs
        for i, (top_x, top_y, bottom_x, bottom_y) in enumerate(ROIs):
            roi = frame[top_y:bottom_y, top_x:bottom_x]
            mask = ROI_analysis(roi, i, pinkLower, pinkUpper)

        # Desenhar as esferas roxas preenchidas que expandem com o ritmo da música
        for beat_time in Bumbo_times:
            if abs(current_time - beat_time) < 0.1:
                # Esfera para o Bumbo
                center_x, center_y = centers[2]  # Bumbo
                radius = int(50 + 50 * (1 - abs(current_time - beat_time) / 0.1))  # Esfera expande e contrai
                cv2.circle(frame, (center_x, center_y), radius, (255, 0, 255), -1)  # Esfera roxa preenchida

        for beat_time in Caixa_times:
            if abs(current_time - beat_time) < 0.1:
                # Esfera para a caixa
                center_x, center_y = centers[1]  # Caixa
                radius = int(50 + 50 * (1 - abs(current_time - beat_time) / 0.1))  # Esfera expande e contrai
                cv2.circle(frame, (center_x, center_y), radius, (255, 0, 255), -1)  # Esfera roxa preenchida

        for beat_time in Chimbal_times:
            if abs(current_time - beat_time) < 0.1:  # Corrigido de < 0.0 para < 0.1
                # Esfera para o chimbal
                center_x, center_y = centers[0]  # Chimbal
                radius = int(50 + 50 * (1 - abs(current_time - beat_time) / 0.1))  # Esfera expande e contrai
                cv2.circle(frame, (center_x, center_y), radius, (255, 0, 255), -1)  # Esfera roxa preenchida

        # Colocar as imagens dos instrumentos para sobrepor as esferas
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

        cv2.imshow('Batuque Project', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
   
