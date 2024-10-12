import pygame

# Definir as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Carregar imagens dos ícones (agora em formato PNG)
icon_iniciante = pygame.image.load("./src/Images/tutoriais/rainbow.png")
icon_intermediario = pygame.image.load("./src/Images/tutoriais/fire.png")
icon_avancado = pygame.image.load("./src/Images/tutoriais/skull.png")
background_image = pygame.image.load("./src/Images/tela inicial/imagem_de_fundo.png")
return_image = pygame.image.load("./src/Images/tutoriais/return.png")

# Redimensionar as imagens para caberem nos botões menores
icon_iniciante = pygame.transform.scale(icon_iniciante, (80, 80))
icon_intermediario = pygame.transform.scale(icon_intermediario, (80, 80))
icon_avancado = pygame.transform.scale(icon_avancado, (80, 80))


# Função para desenhar os botões dos tutoriais
def draw_button(icon, text, sub_text, position, tela):
    x, y = position
    width, height = 700, 150  # Tamanho reduzido dos botões
    
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 40)

    # Fundo do botão
    pygame.draw.rect(tela, WHITE, (x, y, width, height), border_radius=15)
    
    # Desenhar ícone
    tela.blit(icon, (x + 20, y + 45))
    
    # Desenhar texto
    text_surface = font_text.render(text, True, BLACK)
    tela.blit(text_surface, (x + 120, y + 50))
    text_surface = font_sub_text.render(sub_text, True, BLACK)
    tela.blit(text_surface, (x + 120, y + 80))
    
    return pygame.Rect(x, y, width, height)  # Retornar a área do botão para interatividade


# Funções para os diferentes níveis de tutorial
def tutorial_iniciante(altura, largura, tela):
        
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 40)
    print("Entrou no tutorial iniciante!")
    running = True
    while running:
        tela.fill((50, 50, 50))
        text = font_text.render("Tutorial Iniciante", True, WHITE)
        tela.blit(text, (largura // 2 - text.get_width() // 2, altura // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()


# Loop principal
def modulos_tutoriais(tela, altura, largura):
    posicao_height = (altura // 3)
    running = True

    # Definir fontes corretamente (usando uma fonte disponível no sistema)
    font_text = pygame.font.Font(None, 50)
    font_sub_text = pygame.font.Font(None, 40)


    button_return_rect = return_image.get_rect(topleft=(50, altura - return_image.get_height() - 750))

    while running:

        tela.blit(background_image, (0, 0))

        # Desenhar os botões dos tutoriais
        btn_iniciante = draw_button(icon_iniciante, "Iniciante", "O básico da bateria.", (200, 200), tela)
        btn_intermediario = draw_button(icon_intermediario, "Intermediário", "Aprendendo a sincronizar.", (200, 400), tela)
        btn_avancado = draw_button(icon_avancado, "Avançado", "Para quem realmente sabe manter o ritmo!", (200, 600), tela)
        tela.blit(return_image, (50, altura - return_image.get_height() - 750))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar se o botão iniciante foi clicado
                if btn_iniciante.collidepoint(mouse_pos):
                    tutorial_iniciante(altura, largura, tela)  # Chamar função do tutorial Iniciante

                if button_return_rect.collidepoint(event.pos):
                    return False

        pygame.display.flip()
