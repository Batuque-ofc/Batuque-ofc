import pygame
from models.database import conectar_banco_de_dados, inserir_usuario, verifica_nome_usuario
from models.model import Usuario

bg_color = (240, 248, 255)
txt_color = (0, 0, 0)

return_image = pygame.image.load("src/Images/tela inicial/return_button.png")

def draw_rounded_rect(screen, color, rect, radius, width=0):
    """Desenha um retângulo com bordas arredondadas e uma espessura de borda opcional."""
    pygame.draw.rect(screen, color, rect, border_radius=radius, width=width)

def registrar(tela, altura, largura):
    # Redimensionar a fonte com base na largura da tela
    fonte_titulo = pygame.font.Font(None, int(largura * 0.08))  # 8% da largura da tela
    fonte_opcoes = pygame.font.Font(None, int(largura * 0.03))  # 3% da largura da tela

    input_box1 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 225, 400, 50)
    input_box2 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 125, 400, 50)
    input_box3 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 25, 400, 50)  # Caixa de confirmação de senha
    button_rect = pygame.Rect(largura // 2 - 200, altura // 1.5 + 75, 400, 50)
    
    # Botão de voltar representado pela imagem
    button_back_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    
    color1 = color_inactive
    color2 = color_inactive
    color3 = color_inactive  # Cor para a caixa de confirmação de senha
    
    active1 = False
    active2 = False
    active3 = False  # Ativo para a caixa de confirmação de senha
    
    text1 = ''
    text2 = ''
    text3 = ''  # Texto para a caixa de confirmação de senha
    
    fonte_input = pygame.font.Font(None, int(largura * 0.027))  # 4% da largura da tela
    registrar = True
    while registrar:
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
                if input_box3.collidepoint(event.pos):  # Verificação para a caixa de confirmação de senha
                    active3 = not active3
                else:
                    active3 = False
                if button_rect.collidepoint(event.pos):
                    if text1 and text2 and text3:
                        if text2 == text3:
                            usuario = Usuario(text1, text2)
                            cnx = conectar_banco_de_dados()
                            if verifica_nome_usuario(cnx, text1):
                                print("Nome de usuário não disponível!")
                                continue
                            else:
                                inserir_usuario(cnx, usuario)
                                print("Usuário registrado com sucesso!")
                                registrar = False
                        else:
                            print("Senha e confirmação de senha não são iguais!")
                    else:
                        print("Preencha todos os campos!")
                
                # Verificar se o botão de voltar foi clicado
                if button_back_rect.collidepoint(event.pos):
                    print("Voltando para a tela anterior...")
                    registrar = False  # Ou chamar uma função que volte para a tela anterior

                # Atualização da cor
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
                color3 = color_active if active3 else color_inactive

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
                if active3:  # Manipulação de entrada para a caixa de confirmação de senha
                    if event.key == pygame.K_RETURN:
                        active3 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text3 = text3[:-1]
                    else:
                        text3 += event.unicode
        
        tela.fill(bg_color)
        
        # Renderizar o texto digitado nas caixas de entrada
        txt_surface1 = fonte_input.render(text1, True, txt_color)
        txt_surface2 = fonte_input.render('*' * len(text2), True, txt_color)  # Exibe asteriscos
        txt_surface3 = fonte_input.render('*' * len(text3), True, txt_color)  # Exibe asteriscos para a confirmação de senha
        
        # Ajustando o tamanho da caixa de texto para não sobrepor o texto
        width1 = max(400, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(400, txt_surface2.get_width() + 10)
        input_box2.w = width2
        width3 = max(400, txt_surface3.get_width() + 10)  # Largura da caixa de confirmação de senha
        
        input_box3.w = width3
        tela.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 10))
        tela.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 15))
        tela.blit(txt_surface3, (input_box3.x + 5, input_box3.y + 15))  # Blit para a confirmação de senha
        
        # Desenhar as caixas de entrada com bordas arredondadas finas
        draw_rounded_rect(tela, color1, input_box1, 10, 5)
        draw_rounded_rect(tela, color2, input_box2, 10, 5)
        draw_rounded_rect(tela, color3, input_box3, 10, 5)  # Desenha a caixa de confirmação de senha

        # Desenhar o botão de login com bordas arredondadas finas
        draw_rounded_rect(tela, color_inactive, button_rect, 10, 5)
        
        # Desenhar o botão de voltar com a imagem
        tela.blit(return_image, button_back_rect)
        
        titulo = fonte_titulo.render("Registrar", True, txt_color)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 8))
        
        texto_usuario = fonte_opcoes.render("Usuário:", True, txt_color)
        tela.blit(texto_usuario, (input_box1.x, input_box1.y - 40))
        texto_senha = fonte_opcoes.render("Senha:", True, txt_color)
        tela.blit(texto_senha, (input_box2.x, input_box2.y - 40))
        texto_confirmar_senha = fonte_opcoes.render("Confirmar Senha:", True, txt_color)
        tela.blit(texto_confirmar_senha, (input_box3.x, input_box3.y - 40))
        tela.blit(fonte_opcoes.render("Cadastrar", True, txt_color), (button_rect.x + 125, button_rect.y + 10))

        pygame.display.flip()
