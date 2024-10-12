import sys
import pygame
from models.database import conectar_banco_de_dados, consultar_usuario

bg_color = (240, 248, 255)
txt_color = (0, 0, 0)  # Preto para o texto

return_image = pygame.image.load("src/Images/tela inicial/return_button.png")

def draw_rounded_rect(screen, color, rect, radius, width=0):
    """Desenha um retângulo com bordas arredondadas e uma espessura de borda opcional."""
    pygame.draw.rect(screen, color, rect, border_radius=radius, width=width)

def login(tela, altura, largura):
    # Redimensionar a fonte com base na largura da tela
    fonte_titulo = pygame.font.Font(None, int(largura * 0.08))  # 8% da largura da tela
    fonte_opcoes = pygame.font.Font(None, int(largura * 0.03))  # 3% da largura da tela

    input_box1 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 225, 400, 50)
    input_box2 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 125, 400, 50)
    button_rect = pygame.Rect(largura // 2 - 200, altura // 1.5 - 25, 400, 50)

    # Botão de voltar representado pela imagem
    button_back_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    color1 = color_inactive
    color2 = color_inactive

    active1 = False
    active2 = False

    text1 = ''
    text2 = ''

    fonte_input = pygame.font.Font(None, int(largura * 0.027))  # 4% da largura da tela
    login = True

    error_message = ''  # Armazenará a mensagem de erro caso o login falhe

    while login:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                if button_rect.collidepoint(event.pos):
                    if text1 and text2:
                        cnx = conectar_banco_de_dados()
                        user_exists = consultar_usuario(cnx, text1, text2)
                        if user_exists:
                            print("Login bem-sucedido!")
                            return True
                        else:
                            error_message = "Usuário ou senha incorretos"
                    else:
                        error_message = "Por favor, preencha todos os campos!"
                
                # Verificar se o botão de voltar foi clicado
                if button_back_rect.collidepoint(event.pos):
                    login = False  # Ou chamar uma função que volte para a tela anterior

                # Atualização da cor
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive

            elif event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        tela.fill(bg_color)
        
        # Usando txt_color (preto) para o texto digitado
        txt_surface1 = fonte_input.render(text1, True, txt_color)
        txt_surface2 = fonte_input.render('*' * len(text2), True, txt_color)  # Exibe asteriscos para senha

        width1 = max(400, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(400, txt_surface2.get_width() + 10)
        input_box2.w = width2

        tela.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 10))
        tela.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 15))

        # Desenhar caixas de entrada com bordas arredondadas finas
        draw_rounded_rect(tela, color1, input_box1, 10, 5)
        draw_rounded_rect(tela, color2, input_box2, 10, 5)

        # Desenhar o botão de login com bordas arredondadas finas
        draw_rounded_rect(tela, color_inactive, button_rect, 10, 5)

        # Desenhar o botão de voltar com a imagem
        tela.blit(return_image, button_back_rect)
        
        titulo = fonte_titulo.render("Login", True, txt_color)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 8))

        texto_usuario = fonte_opcoes.render("Usuário:", True, txt_color)
        tela.blit(texto_usuario, (input_box1.x, input_box1.y - 40))
        texto_senha = fonte_opcoes.render("Senha:", True, txt_color)
        tela.blit(texto_senha, (input_box2.x, input_box2.y - 40))
        tela.blit(fonte_opcoes.render("Entrar", True, txt_color), (button_rect.x + 150, button_rect.y + 10))

        # Exibe a mensagem de erro, se houver
        if error_message:
            erro_surface = fonte_opcoes.render(error_message, True, (255, 0, 0))  # Exibe em vermelho
            tela.blit(erro_surface, (largura // 2 - erro_surface.get_width() // 2, altura // 1.5 + 50))

        pygame.display.flip()
