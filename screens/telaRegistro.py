import pygame
from models.database import conectar_banco_de_dados, inserir_usuario, verifica_nome_usuario
from models.model import Usuario

pygame.init()

bg_color = (255, 255, 255)
input_inactive_color = pygame.Color(192, 192, 192)
input_active_color = pygame.Color(0, 128, 0)
button_color = (60, 179, 113)
button_hover_color = (144, 238, 144)
error_color = (255, 69, 0)
error_background_color = (255, 240, 245)
text_color = (0, 0, 0)
button_text_color = (255, 255, 255)

return_image = pygame.image.load("src/Images/tela inicial/return_button.png")

def draw_rounded_rect(screen, color, rect, radius, width=0):
    pygame.draw.rect(screen, color, rect, border_radius=radius, width=width)

def draw_button(screen, text, rect, font, mouse_pos, default_color, hover_color):
    color = hover_color if rect.collidepoint(mouse_pos) else default_color
    draw_rounded_rect(screen, color, rect, 10, 0)
    text_surface = font.render(text, True, button_text_color)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

def draw_error_message(screen, message, font, largura, altura):
    erro_surface = font.render(message, True, error_color)
    erro_background = pygame.Surface((erro_surface.get_width() + 40, erro_surface.get_height() + 20))
    erro_background.fill(error_background_color)
    erro_background_rect = erro_background.get_rect(center=(largura // 2, altura - 100))
    draw_rounded_rect(screen, error_background_color, erro_background_rect, 15)
    screen.blit(erro_background, erro_background_rect.topleft)
    screen.blit(erro_surface, (erro_background_rect.x + 20, erro_background_rect.y + 10))

def registrar(tela, altura, largura):
    fonte_titulo = pygame.font.Font(None, int(largura * 0.08))
    fonte_opcoes = pygame.font.Font(None, int(largura * 0.035))
    fonte_input = pygame.font.Font(None, int(largura * 0.03))

    input_box1 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 225, 400, 50)
    input_box2 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 125, 400, 50)
    input_box3 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 25, 400, 50)
    button_rect = pygame.Rect(largura // 2 - 200, altura // 1.5 + 75, 400, 50)
    button_back_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    color1 = input_inactive_color
    color2 = input_inactive_color
    color3 = input_inactive_color
    active1 = False
    active2 = False
    active3 = False

    text1 = ''
    text2 = ''
    text3 = ''
    registrar_running = True
    error_message = ''

    while registrar_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                if input_box3.collidepoint(event.pos):
                    active3 = not active3
                else:
                    active3 = False
                if button_rect.collidepoint(event.pos):
                    if text1 and text2 and text3:
                        if text2 == text3:
                            usuario = Usuario(text1, text2)
                            cnx = conectar_banco_de_dados()
                            if verifica_nome_usuario(cnx, text1):
                                error_message = "Nome de usuário não disponível!"
                            else:
                                inserir_usuario(cnx, usuario)
                                registrar_running = False
                        else:
                            error_message = "Senha e confirmação de senha não são iguais!"
                    else:
                        error_message = "Preencha todos os campos!"
                if button_back_rect.collidepoint(event.pos):
                    registrar_running = False

                color1 = input_active_color if active1 else input_inactive_color
                color2 = input_active_color if active2 else input_inactive_color
                color3 = input_active_color if active3 else input_inactive_color

            elif event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode
                if active3:
                    if event.key == pygame.K_BACKSPACE:
                        text3 = text3[:-1]
                    else:
                        text3 += event.unicode

        tela.fill(bg_color)

        titulo = fonte_titulo.render("Registrar", True, text_color)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 8))

        txt_surface1 = fonte_input.render(text1, True, text_color)
        txt_surface2 = fonte_input.render('*' * len(text2), True, text_color)
        txt_surface3 = fonte_input.render('*' * len(text3), True, text_color)
        tela.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 10))
        tela.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 10))
        tela.blit(txt_surface3, (input_box3.x + 5, input_box3.y + 10))
        draw_rounded_rect(tela, color1, input_box1, 10, 5)
        draw_rounded_rect(tela, color2, input_box2, 10, 5)
        draw_rounded_rect(tela, color3, input_box3, 10, 5)

        draw_button(tela, "Cadastrar", button_rect, fonte_opcoes, mouse_pos, button_color, button_hover_color)
        tela.blit(return_image, button_back_rect)

        texto_usuario = fonte_opcoes.render("Usuário:", True, text_color)
        texto_senha = fonte_opcoes.render("Senha:", True, text_color)
        texto_confirmar_senha = fonte_opcoes.render("Confirmar Senha:", True, text_color)
        tela.blit(texto_usuario, (input_box1.x, input_box1.y - 40))
        tela.blit(texto_senha, (input_box2.x, input_box2.y - 40))
        tela.blit(texto_confirmar_senha, (input_box3.x, input_box3.y - 40))

        if error_message:
            draw_error_message(tela, error_message, fonte_opcoes, largura, altura)

        pygame.display.flip()

    return True
