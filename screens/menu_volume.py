import sys
import pygame

bg_color = (30, 30, 30)
hover_color = (100, 100, 100)
slider_color = (0, 255, 0)
knob_color = (255, 255, 255)
hover_knob_color = (200, 200, 255)
text_color = (255, 255, 255)

def draw_rounded_rect(screen, color, rect, radius):
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def config_volume(tela, volume_atual):
    largura_tela, altura_tela = tela.get_size()

    fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.05))
    fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.03))

    titulo = fonte_titulo.render("Ajustar Volume", True, text_color)

    opcoes_volume = [
        {"texto": "20% de Volume", "volume": 0.2},
        {"texto": "40% de Volume", "volume": 0.4},
        {"texto": "60% de Volume", "volume": 0.6},
        {"texto": "80% de Volume", "volume": 0.8},
        {"texto": "100% de Volume", "volume": 1.0},
        {"texto": "Voltar", "acao": "voltar"}
    ]

    slider_rect = pygame.Rect(largura_tela * 0.25, altura_tela * 0.3, largura_tela * 0.5, altura_tela * 0.05)
    slider_knob_rect = pygame.Rect(slider_rect.x + int(slider_rect.width * volume_atual) - 10, slider_rect.y - 5, 20, slider_rect.height + 10)

    ajustando_volume = True
    while ajustando_volume:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(mouse_pos):
                    volume_atual = (mouse_pos[0] - slider_rect.x) / slider_rect.width
                    volume_atual = max(0.0, min(1.0, volume_atual))
                    pygame.mixer.music.set_volume(volume_atual)
                for opcao in opcoes_volume:
                    if opcao.get("volume") is not None:
                        y_pos = int((opcoes_volume.index(opcao) + 1) * (altura_tela * 0.07) + slider_rect.bottom + 40)
                        if largura_tela * 0.35 <= mouse_pos[0] <= largura_tela * 0.65 and y_pos <= mouse_pos[1] <= y_pos + int(altura_tela * 0.06):
                            volume_atual = opcao["volume"]
                            ajustando_volume = False
                            return volume_atual
                if largura_tela * 0.35 <= mouse_pos[0] <= largura_tela * 0.65 and altura_tela * 0.85 <= mouse_pos[1] <= altura_tela * 0.95:
                    ajustando_volume = False
                    return volume_atual

            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if slider_rect.collidepoint(mouse_pos):
                    volume_atual = (mouse_pos[0] - slider_rect.x) / slider_rect.width
                    volume_atual = max(0.0, min(1.0, volume_atual))
                    pygame.mixer.music.set_volume(volume_atual)

        slider_knob_rect.x = slider_rect.x + int(slider_rect.width * volume_atual) - 10

        tela.fill(bg_color)
        tela.blit(titulo, (largura_tela * 0.35, altura_tela * 0.1))

        pygame.draw.rect(tela, slider_color, slider_rect, border_radius=10)
        knob_current_color = hover_knob_color if slider_knob_rect.collidepoint(mouse_pos) else knob_color
        pygame.draw.ellipse(tela, knob_current_color, slider_knob_rect)

        for opcao in opcoes_volume:
            y_pos = int((opcoes_volume.index(opcao) + 1) * (altura_tela * 0.07) + slider_rect.bottom + 40)
            if opcao.get("volume") is not None:
                if largura_tela * 0.35 <= mouse_pos[0] <= largura_tela * 0.65 and y_pos <= mouse_pos[1] <= y_pos + int(altura_tela * 0.06):
                    draw_rounded_rect(tela, hover_color, pygame.Rect(largura_tela * 0.35, y_pos, largura_tela * 0.3, altura_tela * 0.05), 10)
                else:
                    draw_rounded_rect(tela, text_color, pygame.Rect(largura_tela * 0.35, y_pos, largura_tela * 0.3, altura_tela * 0.05), 10)
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, bg_color)
                tela.blit(texto_renderizado, (largura_tela * 0.42, y_pos + 5))

        if largura_tela * 0.35 <= mouse_pos[0] <= largura_tela * 0.65 and altura_tela * 0.85 <= mouse_pos[1] <= altura_tela * 0.95:
            draw_rounded_rect(tela, hover_color, pygame.Rect(largura_tela * 0.35, altura_tela * 0.85, largura_tela * 0.3, altura_tela * 0.05), 10)
        else:
            draw_rounded_rect(tela, text_color, pygame.Rect(largura_tela * 0.35, altura_tela * 0.85, largura_tela * 0.3, altura_tela * 0.05), 10)
        texto_voltar = fonte_opcoes.render("Voltar", True, bg_color)
        tela.blit(texto_voltar, (largura_tela * 0.45, altura_tela * 0.86))

        pygame.display.flip()

    return volume_atual
