import sys
import pygame

bg_color = (0, 0, 0)
txt_color = (255, 255, 255)
hover_color = (100, 100, 100)
def draw_rounded_rect(screen, color, rect, radius):
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def desenhar_opcoes(tela, fonte, opcoes, largura_tela, altura_tela, opcao_hover):
    margem_topo = altura_tela * 0.15
    espaco_entre_opcoes = altura_tela * 0.06

    for idx, opcao in enumerate(opcoes):
        y_pos = margem_topo + idx * espaco_entre_opcoes
        cor = hover_color if idx == opcao_hover else txt_color

        largura_botao = largura_tela * 0.4
        altura_botao = altura_tela * 0.05
        x_pos = (largura_tela - largura_botao) / 2

        draw_rounded_rect(tela, cor, pygame.Rect(x_pos, y_pos, largura_botao, altura_botao), 10)
        texto_renderizado = fonte.render(opcao["texto"], True, bg_color)
        tela.blit(texto_renderizado, (x_pos + largura_botao * 0.1, y_pos + altura_botao * 0.2))

def verificar_hover(mouse_pos, opcoes, largura_tela, altura_tela):
    margem_topo = altura_tela * 0.15
    espaco_entre_opcoes = altura_tela * 0.06

    for idx, opcao in enumerate(opcoes):
        y_pos = margem_topo + idx * espaco_entre_opcoes
        largura_botao = largura_tela * 0.4
        altura_botao = altura_tela * 0.05
        x_pos = (largura_tela - largura_botao) / 2
        if x_pos <= mouse_pos[0] <= x_pos + largura_botao and y_pos <= mouse_pos[1] <= y_pos + altura_botao:
            return idx
    return None

def config_resolucoes(tela):
    modo_atual = "tela_cheia"
    selecionando_resolucao = True

    # Obtendo a resolução máxima suportada pelo monitor
    largura_maxima, altura_maxima = pygame.display.Info().current_w, pygame.display.Info().current_h

    def obter_opcoes_resolucao():
        # Detectar resoluções comuns que se ajustem à tela do usuário
        resolucoes_comuns = [
            (800, 600), (1024, 768), (1280, 720), (1366, 768),
            (1440, 900), (1600, 900), (1920, 1080), (2560, 1440), (3840, 2160)
        ]

        # Filtrar resoluções que se ajustem à tela do usuário e adicionar algumas proporcionais
        opcoes_res = [{"texto": f"{res[0]}x{res[1]}", "resolucao": res}
                      for res in resolucoes_comuns if res[0] <= largura_maxima and res[1] <= altura_maxima]

        resolucoes_proporcionais = [
            (int(largura_maxima * 0.5), int(altura_maxima * 0.5)),
            (int(largura_maxima * 0.75), int(altura_maxima * 0.75)),
            (int(largura_maxima * 0.9), int(altura_maxima * 0.9)),
            (largura_maxima, altura_maxima)
        ]

        for res in resolucoes_proporcionais:
            if res not in [op["resolucao"] for op in opcoes_res]:
                opcoes_res.append({"texto": f"{res[0]}x{res[1]}", "resolucao": res})

        return opcoes_res

    while selecionando_resolucao:
        largura_tela, altura_tela = tela.get_size()
        fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.05))
        fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.025))

        titulo = fonte_titulo.render("Escolha a Resolução", True, txt_color)

        opcoes_resolucao = obter_opcoes_resolucao()

        opcoes_resolucao.extend([
            {"texto": "Modo Janela", "acao": "modo_janela"},
            {"texto": "Modo Sem Bordas", "acao": "modo_sem_bordas"},
            {"texto": "Tela Cheia", "acao": "tela_cheia"},
            {"texto": "Voltar", "acao": "voltar"}
        ])

        mouse_pos = pygame.mouse.get_pos()
        opcao_hover = verificar_hover(mouse_pos, opcoes_resolucao, largura_tela, altura_tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and opcao_hover is not None:
                opcao_selecionada = opcoes_resolucao[opcao_hover]
                if "resolucao" in opcao_selecionada:
                    largura_selecionada, altura_selecionada = opcao_selecionada["resolucao"]
                    if modo_atual == "modo_janela":
                        tela = pygame.display.set_mode((largura_selecionada, altura_selecionada), pygame.RESIZABLE)
                    elif modo_atual == "modo_sem_bordas":
                        tela = pygame.display.set_mode((largura_selecionada, altura_selecionada), pygame.NOFRAME | pygame.RESIZABLE)
                    elif modo_atual == "tela_cheia":
                        tela = pygame.display.set_mode((largura_selecionada, altura_selecionada), pygame.FULLSCREEN)
                elif opcao_selecionada.get("acao") == "modo_janela":
                    modo_atual = "modo_janela"
                    tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.RESIZABLE)
                elif opcao_selecionada.get("acao") == "modo_sem_bordas":
                    modo_atual = "modo_sem_bordas"
                    tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.NOFRAME | pygame.RESIZABLE)
                elif opcao_selecionada.get("acao") == "tela_cheia":
                    modo_atual = "tela_cheia"
                    tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.FULLSCREEN)
                elif opcao_selecionada.get("acao") == "voltar":
                    return "voltar"

        tela.fill(bg_color)
        tela.blit(titulo, (largura_tela * 0.25, altura_tela * 0.05))
        desenhar_opcoes(tela, fonte_opcoes, opcoes_resolucao, largura_tela, altura_tela, opcao_hover)
        pygame.display.flip()

    return "voltar"
