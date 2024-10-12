import sys
import pygame
from screens import menu_volume
from screens import menu_resolucao

bg_color = (0, 0, 0)
txt_color = (255, 255, 255)

def draw_rounded_rect(screen, color, rect, radius):
    """Desenha um retângulo com bordas arredondadas."""
    pygame.draw.rect(screen, color, rect, border_radius=radius)

def configuracoes(screen):
    """Abre o menu de configurações com adaptação à resolução."""
    largura_tela, altura_tela = screen.get_size()  # Obter dimensões da tela

    # Ajustar dinamicamente o tamanho da fonte
    fonte_titulo = pygame.font.Font(None, int(largura_tela * 0.06))  # 6% da largura da tela
    fonte_opcoes = pygame.font.Font(None, int(largura_tela * 0.025))  # 2% da largura da tela

    # Inicializar volume_atual com o volume atual da música
    volume_atual = pygame.mixer.music.get_volume()

    # Texto do título
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
                # Verificar clique em "Mudar Resolução"
                if largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and altura_tela * 0.25 <= mouse_pos[1] <= altura_tela * 0.30:
                    resolucao = menu_resolucao.config_resolucoes(screen)
                    if resolucao is None:  # Verifica se o usuário clicou em "Voltar"
                        return False
                        continue  # Volta para o menu anterior sem alterar nada
                    if isinstance(resolucao, tuple) and len(resolucao) == 2:  # Verifica se a resolução é uma tupla válida
                        pygame.display.set_mode(resolucao)
                # Verificar clique em "Ajustar Volume"
                elif largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and altura_tela * 0.4 <= mouse_pos[1] <= altura_tela * 0.45:
                    # Passar o volume_atual como argumento
                    volume_atual = menu_volume.config_volume(screen, volume_atual)
                    if volume_atual is not None:
                        pygame.mixer.music.set_volume(volume_atual)
                # Verificar clique em "Voltar"
                elif largura_tela * 0.2 <= mouse_pos[0] <= largura_tela * 0.8 and altura_tela * 0.55 <= mouse_pos[1] <= altura_tela * 0.60:
                    return False  # Fecha o menu de configurações e volta

        # Preencher o fundo
        screen.fill((0, 0, 0))  # Cor de fundo preta
        screen.blit(titulo, (largura_tela * 0.3, altura_tela * 0.05))  # Posição dinâmica do título

        # Desenhar botão "Mudar Resolução" com bordas arredondadas
        draw_rounded_rect(screen, (255, 255, 255), pygame.Rect(largura_tela * 0.25, altura_tela * 0.25, largura_tela * 0.35, altura_tela * 0.05), 10)
        texto_resolucao = fonte_opcoes.render("Mudar Resolução", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_resolucao, (largura_tela * 0.35, altura_tela * 0.26))  # Posição dinâmica

        # Desenhar botão "Ajustar Volume" com bordas arredondadas
        draw_rounded_rect(screen, (255, 255, 255), pygame.Rect(largura_tela * 0.25, altura_tela * 0.4, largura_tela * 0.35, altura_tela * 0.05), 10)
        texto_volume = fonte_opcoes.render("Ajustar Volume", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_volume, (largura_tela * 0.36, altura_tela * 0.41))  # Posição dinâmica

        # Desenhar botão "Voltar" com bordas arredondadas
        draw_rounded_rect(screen, (255, 255, 255), pygame.Rect(largura_tela * 0.25, altura_tela * 0.55, largura_tela * 0.35, altura_tela * 0.05), 10)
        texto_voltar = fonte_opcoes.render("Voltar", True, (0, 0, 0))  # Texto preto
        screen.blit(texto_voltar, (largura_tela * 0.4, altura_tela * 0.56))  # Posição dinâmica

        pygame.display.flip()

    return True  # Retorna verdadeiro após sair da configuração
