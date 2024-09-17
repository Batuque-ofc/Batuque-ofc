import sys
import pygame

bg_color = (0,0,0)
txt_color = (255,255,255)

def config_resolucoes(tela):
    # Definir fonte para o título
    fonte_titulo = pygame.font.Font(None, 48)

    # Definir fonte para as opções
    fonte_opcoes = pygame.font.Font(None, 36)

    # Título da tela de resoluções
    titulo = fonte_titulo.render("Escolha a Resolução", True, txt_color)

    # Opções disponíveis de resolução
    opcoes_resolucao = [
        {"texto": "800x600", "resolucao": (800, 600)},
        {"texto": "1024x768", "resolucao": (1024, 768)},
        {"texto": "1280x720", "resolucao": (1280, 720)},
        {"texto": "1440x900", "resolucao": (1440, 900)},
        {"texto": "1920x1080", "resolucao": (1920, 1080)},
        {"texto": "Voltar", "acao": "voltar"}
    ]

    # Espaço entre as opções
    espaco = 20

    # Loop principal da tela de resoluções
    selecionando_resolucao = True
    while selecionando_resolucao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar se o clique foi em uma opção de resolução
                for opcao in opcoes_resolucao:
                    if opcao.get("resolucao"):
                        y_pos = (opcoes_resolucao.index(opcao) + 1) * (60 + espaco) + 100
                        if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > y_pos and mouse_pos[1] < y_pos + 50:
                            selecionando_resolucao = False
                            return opcao["resolucao"]
                # Verificar se o clique foi no botão de voltar
                if mouse_pos[0] > 100 and mouse_pos[0] < 400 and mouse_pos[1] > 650 and mouse_pos[1] < 700:
                    return False

        tela.fill(bg_color)
        tela.blit(titulo, (100, 50))

        # Exibir opções de resolução
        for opcao in opcoes_resolucao:
            if opcao.get("resolucao"):
                y_pos = (opcoes_resolucao.index(opcao) + 1) * (60 + espaco) + 100
                pygame.draw.rect(tela, txt_color, pygame.Rect(100, y_pos, 300, 50))
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, bg_color)
                tela.blit(texto_renderizado, (150, y_pos + 10))

        # Exibir botão de voltar
        pygame.draw.rect(tela, txt_color, pygame.Rect(100, 650, 300, 50))
        texto_voltar = fonte_opcoes.render("Voltar", True, bg_color)
        tela.blit(texto_voltar, (200, 660))

        pygame.display.flip()
