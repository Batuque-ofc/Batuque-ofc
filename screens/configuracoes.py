import pygame
from screens import menu_volume
from screens import menu_resolucao

def configuracoes(screen):
    """Abre o menu de configurações."""
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_opcoes = pygame.font.Font(None, 36)
    titulo = fonte_titulo.render("Configurações", True, (255, 255, 255))  # Cor branca

    configurando = True
    while configurando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    configurando = False
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 400 and 200 <= mouse_pos[1] <= 250:
                    resolucao = menu_resolucao.config_resolucoes(screen)
                    if not resolucao:
                        return False
                    pygame.display.set_mode(resolucao)
                elif 100 <= mouse_pos[0] <= 400 and 300 <= mouse_pos[1] <= 350:
                    volume = menu_volume.config_volume(screen)
                    if not volume:
                        return False
                    pygame.mixer.music.set_volume(volume)
                elif 100 <= mouse_pos[0] <= 400 and 400 <= mouse_pos[1] <= 450:
                    return False

        screen.fill((0, 0, 0))  # Cor de fundo preta
        screen.blit(titulo, (100, 50))

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 200, 300, 50))
        texto_resolucao = fonte_opcoes.render("Mudar Resolução", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_resolucao, (150, 210))

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 300, 300, 50))
        texto_volume = fonte_opcoes.render("Ajustar Volume", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_volume, (180, 310))

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 400, 300, 50))
        texto_voltar = fonte_opcoes.render("Menu Principal", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_voltar, (200, 410))

        pygame.display.flip()

    return True
