import sys
import pygame
from screens import menu_volume, menu_resolucao

bg_color = (0, 0, 0)
txt_color = (255, 255, 255)
hover_color = (100, 100, 100)

def draw_rounded_rect(screen, color, rect, radius):
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def draw_button(screen, text, rect, font, mouse_pos, hover_color, default_color):
    color = hover_color if rect.collidepoint(mouse_pos) else default_color
    draw_rounded_rect(screen, color, rect, 10)
    text_rendered = font.render(text, True, bg_color)
    screen.blit(text_rendered, (rect.x + (rect.width - text_rendered.get_width()) // 2, rect.y + (rect.height - text_rendered.get_height()) // 2))

def configuracoes(screen):
    largura_tela, altura_tela = screen.get_size()
    fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.06))
    fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.025))

    volume_atual = pygame.mixer.music.get_volume()
    titulo = fonte_titulo.render("Configurações", True, txt_color)

    configurando = True
    voltar_ao_menu_inicial = False

    while configurando:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                configurando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mudar_resolucao_rect.collidepoint(mouse_pos):
                    resolucao = menu_resolucao.config_resolucoes(screen)
                    if isinstance(resolucao, tuple) and len(resolucao) == 2:
                        pygame.display.set_mode(resolucao)
                elif ajustar_volume_rect.collidepoint(mouse_pos):
                    volume_atual = menu_volume.config_volume(screen, volume_atual)
                    if volume_atual is not None:
                        pygame.mixer.music.set_volume(volume_atual)
                elif voltar_rect.collidepoint(mouse_pos):
                    configurando = False
                elif voltar_menu_inicial_rect.collidepoint(mouse_pos):
                    configurando = False
                    voltar_ao_menu_inicial = True

        screen.fill(bg_color)
        titulo_rect = titulo.get_rect(center=(largura_tela / 2, altura_tela * 0.1))
        screen.blit(titulo, titulo_rect)

        # Definir retângulos dos botões centralizados
        mudar_resolucao_rect = pygame.Rect((largura_tela - largura_tela * 0.35) / 2, altura_tela * 0.25, largura_tela * 0.35, altura_tela * 0.05)
        ajustar_volume_rect = pygame.Rect((largura_tela - largura_tela * 0.35) / 2, altura_tela * 0.4, largura_tela * 0.35, altura_tela * 0.05)
        voltar_rect = pygame.Rect((largura_tela - largura_tela * 0.35) / 2, altura_tela * 0.55, largura_tela * 0.35, altura_tela * 0.05)
        voltar_menu_inicial_rect = pygame.Rect((largura_tela - largura_tela * 0.35) / 2, altura_tela * 0.7, largura_tela * 0.35, altura_tela * 0.05)

        draw_button(screen, "Mudar Resolução", mudar_resolucao_rect, fonte_opcoes, mouse_pos, hover_color, txt_color)
        draw_button(screen, "Ajustar Volume", ajustar_volume_rect, fonte_opcoes, mouse_pos, hover_color, txt_color)
        draw_button(screen, "Voltar", voltar_rect, fonte_opcoes, mouse_pos, hover_color, txt_color)
        draw_button(screen, "Voltar ao Menu Inicial", voltar_menu_inicial_rect, fonte_opcoes, mouse_pos, hover_color, txt_color)

        pygame.display.flip()

    return voltar_ao_menu_inicial
