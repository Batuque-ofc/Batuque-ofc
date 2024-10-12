import sys
import pygame

bg_color = (0, 0, 0)
txt_color = (255, 255, 255)


def draw_rounded_rect(screen, color, rect, radius):
    """Desenha um retângulo com bordas arredondadas."""
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def config_volume(tela, volume_atual):
    # Obter dimensões da tela atual
    largura_tela, altura_tela = tela.get_size()

    # Definir fontes de forma dinâmica
    fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.05))  # 6% da largura da tela
    fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.025))  # 3% da largura da tela

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

    # Espaço entre as opções (ajustado dinamicamente)
    espaco = int(altura_tela * 0.03)

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
                        y_pos = int((opcoes_volume.index(opcao) + 1) * (altura_tela * 0.1) + 100)  # Ajuste dinâmico do Y
                        if largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and y_pos <= mouse_pos[1] <= y_pos + int(altura_tela * 0.08):
                            volume_atual = opcao["volume"]  # Atualiza o volume atual
                            ajustando_volume = False
                            return volume_atual
                # Verificar se o clique foi no botão de voltar
                if largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and altura_tela * 0.85 <= mouse_pos[1] <= altura_tela * 0.95:
                    ajustando_volume = False  # Não altera o volume e volta
                    return volume_atual  # Retorna o volume atual sem alterar

        # Preencher o fundo
        tela.fill(bg_color)
        tela.blit(titulo, (largura_tela * 0.3, altura_tela * 0.05))  # Ajustar a posição do título

        # Exibir opções de volume com bordas arredondadas
        for opcao in opcoes_volume:
            if opcao.get("volume"):
                y_pos = int((opcoes_volume.index(opcao) + 1) * (altura_tela * 0.1) + 100)  # Ajuste dinâmico
                draw_rounded_rect(tela, txt_color, pygame.Rect(largura_tela * 0.25, y_pos, largura_tela * 0.35, altura_tela * 0.05), 10)
                texto_renderizado = fonte_opcoes.render(opcao["texto"], True, bg_color)
                tela.blit(texto_renderizado, (largura_tela * 0.35, y_pos + 10))

        # Exibir botão de voltar com bordas arredondas
        draw_rounded_rect(tela, txt_color, pygame.Rect(largura_tela * 0.25, altura_tela * 0.85, largura_tela * 0.35, altura_tela * 0.05), 10)
        texto_voltar = fonte_opcoes.render("Voltar", True, bg_color)
        tela.blit(texto_voltar, (largura_tela * 0.4, altura_tela * 0.86))

        pygame.display.flip()

    return volume_atual  # Retorna o volume atual se "Voltar" for clicado
