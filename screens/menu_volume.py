import sys
import pygame

bg_color = (0,0,0)
txt_color = (255,255,255)

def config_volume(tela):
    # Definir fonte para o título
    fonte_titulo = pygame.font.Font(None, 48)

    # Definir fonte para as opções
    fonte_opcoes = pygame.font.Font(None, 36)

    # Título da tela de volume
    titulo = fonte_titulo.render("Ajustar Volume", True, txt_color)

    # Opções disponíveis de volume
    opcoes_volume = [
        {"texto": "20% de Volume", "volume": 0.2},
        {"texto": "40% de Volume", "volume": 0.4},
        {"texto": "60% de Volume", "volume": 0.6},
        {"texto": "80% de Volume", "volume": 0.8},
        {"texto": "100% de Volume", "volume": 1.0},
        {"texto": "Voltar", "acao": "voltar"}
    ]

    # Espaço entre as opções
    espaco = 20

    # Loop principal da tela de volume
    ajustando_volume = True
    while ajustando_volume:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Ajustar volume de acordo com a opção selecionada
                for opcao in opcoes_volume:
                    if opcao.get("volume"):
                        y_pos = (opcoes_volume.index(opcao) + 1) * (60 + espaco) + 100
                        if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > y_pos and mouse_pos[1] < y_pos + 50:
                            ajustando_volume = False
                            return opcao["volume"]
                # Verificar se o clique foi no botão de voltar
                if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > 650 and mouse_pos[1] < 700:
                    return False

        tela.fill(bg_color)
        tela.blit(titulo, (100, 50))

        # Exibir opções de volume
        for opcao in opcoes_volume:
            if opcao.get("volume"):
                y_pos = (opcoes_volume.index(opcao) + 1) * (60 + espaco) + 100
                pygame.draw.rect(tela, txt_color, pygame.Rect(100, y_pos, 300, 50))
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, bg_color)
                tela.blit(texto_renderizado, (150, y_pos + 10))

        # Exibir botão de voltar
        pygame.draw.rect(tela, txt_color, pygame.Rect(100, 650, 300, 50))
        texto_voltar = fonte_opcoes.render("Voltar", True, bg_color)
        tela.blit(texto_voltar, (200, 660))

        pygame.display.flip()