import sys
import pygame

bg_color = (0, 0, 0)
txt_color = (255, 255, 255)

def draw_rounded_rect(screen, color, rect, radius):
    """Desenha um retângulo com bordas arredondadas."""
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def config_resolucoes(tela):
    # Obter largura e altura da tela atual
    largura_tela, altura_tela = tela.get_size()

    # Definir fonte para o título (dinamicamente ajustada)
    fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.04))

    # Definir fonte para as opções (dinamicamente ajustada)
    fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.025))

    # Título da tela de resoluções
    titulo = fonte_titulo.render("Escolha a Resolução", True, txt_color)

    # Opções disponíveis de resolução
    opcoes_resolucao = [
        {"texto": "800x600", "resolucao": (800, 600)},
        {"texto": "1024x768", "resolucao": (1024, 768)},
        {"texto": "1280x720", "resolucao": (1280, 720)},
        {"texto": "1360x768", "resolucao": (1360, 768)},
        {"texto": "1440x900", "resolucao": (1440, 900)},
        {"texto": "1920x1080", "resolucao": (1920, 1080)},
        {"texto": "Voltar", "acao": "voltar"}
    ]

    # Espaço entre as opções (ajustado dinamicamente)
    espaco = int(altura_tela * 0.03)

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
                        y_pos = int((opcoes_resolucao.index(opcao) + 1) * (altura_tela * 0.1) + 100)  # Ajuste dinâmico do Y
                        if largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and \
                           mouse_pos[1] > y_pos and mouse_pos[1] < y_pos + int(altura_tela * 0.1):
                            selecionando_resolucao = False
                            return opcao["resolucao"]
                # Verificar se o clique foi no botão de voltar
                if mouse_pos[0] > largura_tela * 0.2 and mouse_pos[0] < largura_tela * 0.8 and \
                   mouse_pos[1] > altura_tela * 0.85 and mouse_pos[1] < altura_tela * 0.95:
                    selecionando_resolucao = False  # Não altera a resolução e volta para a tela anterior
                    return "voltar"  # Retorna a ação de voltar

        tela.fill(bg_color)
        tela.blit(titulo, (largura_tela * 0.3, altura_tela * 0.1))  # Ajuste dinâmico do título

        # Exibir opções de resolução com bordas arredondadas
        for opcao in opcoes_resolucao:
            if opcao.get("resolucao"):
                y_pos = int((opcoes_resolucao.index(opcao) + 1) * (altura_tela * 0.1) + 100)
                draw_rounded_rect(tela, txt_color, pygame.Rect(largura_tela * 0.25, y_pos, largura_tela * 0.35, altura_tela * 0.05), 10)
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, bg_color)
                tela.blit(texto_renderizado, (largura_tela * 0.38, y_pos + 10))

        # Exibir botão de voltar com bordas arredondadas
        draw_rounded_rect(tela, txt_color, pygame.Rect(largura_tela * 0.25, altura_tela * 0.85, largura_tela * 0.35, altura_tela * 0.05), 10)
        texto_voltar = fonte_opcoes.render("Voltar", True, bg_color)
        tela.blit(texto_voltar, (largura_tela * 0.40, altura_tela * 0.86))

        pygame.display.flip()

    return "voltar"  # Retorna "voltar" se o botão de voltar for clicado
