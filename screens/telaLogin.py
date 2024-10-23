import sys
import pygame
from models.database import conectar_banco_de_dados, consultar_usuario
from screens.telaRegistro import registrar

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
show_password_image = pygame.image.load("src/Images/tela login/eye-password-show.svg")
hide_password_image = pygame.image.load("src/Images/tela login/eye-password-not-show.svg")
register_button_rect = pygame.Rect(50, 50, 150, 50)

show_password = False

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

def login(tela, altura, largura):
    fonte_titulo = pygame.font.Font(None, int(largura * 0.08))
    fonte_opcoes = pygame.font.Font(None, int(largura * 0.035))
    fonte_input = pygame.font.Font(None, int(largura * 0.03))

    input_box1 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 225, 400, 50)
    input_box2 = pygame.Rect(largura // 2 - 200, altura // 1.5 - 125, 400, 50)
    button_rect = pygame.Rect(largura // 2 - 200, altura // 1.5 - 25, 400, 50)
    button_back_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))
    show_password_rect = show_password_image.get_rect(topleft=(input_box2.right + 10, input_box2.y + 10))
    register_button_rect = pygame.Rect(largura // 2 - 200, altura // 1.5 + 75, 400, 50)

    color1 = input_inactive_color
    color2 = input_inactive_color
    active1 = False
    active2 = False

    text1 = ''
    text2 = ''
    login_running = True
    error_message = ''

    global show_password

    while login_running:
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
                if button_rect.collidepoint(event.pos):
                    if text1 and text2:
                        cnx = conectar_banco_de_dados()
                        user_exists = consultar_usuario(cnx, text1, text2)
                        if user_exists:
                            return True
                        else:
                            error_message = "Usuário ou senha incorretos"
                    else:
                        error_message = "Por favor, preencha todos os campos!"
                if button_back_rect.collidepoint(event.pos):
                    return False
                if show_password_rect.collidepoint(event.pos):
                    show_password = not show_password
                if register_button_rect.collidepoint(event.pos):
                    registrar(tela, altura, largura)
                    return False

                color1 = input_active_color if active1 else input_inactive_color
                color2 = input_active_color if active2 else input_inactive_color

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

        tela.fill(bg_color)

        titulo = fonte_titulo.render("Login", True, text_color)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, altura // 8))

        txt_surface1 = fonte_input.render(text1, True, text_color)
        txt_surface2 = fonte_input.render(text2 if show_password else '*' * len(text2), True, text_color)
        tela.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 10))
        tela.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 10))
        draw_rounded_rect(tela, color1, input_box1, 10, 5)
        draw_rounded_rect(tela, color2, input_box2, 10, 5)

        draw_button(tela, "Entrar", button_rect, fonte_opcoes, mouse_pos, button_color, button_hover_color)
        draw_button(tela, "Registrar-se", register_button_rect, fonte_opcoes, mouse_pos, button_color, button_hover_color)

        tela.blit(return_image, button_back_rect)
        if show_password:
            tela.blit(hide_password_image, show_password_rect)
        else:
            tela.blit(show_password_image, show_password_rect)

        texto_usuario = fonte_opcoes.render("Usuário:", True, text_color)
        texto_senha = fonte_opcoes.render("Senha:", True, text_color)
        tela.blit(texto_usuario, (input_box1.x, input_box1.y - 40))
        tela.blit(texto_senha, (input_box2.x, input_box2.y - 40))

        if error_message:
            draw_error_message(tela, error_message, fonte_opcoes, largura, altura)

        pygame.display.flip()

    return True
