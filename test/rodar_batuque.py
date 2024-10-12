import sys
import pygame
from batuque import run_batuque

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 1920, 1080
screen = pygame.display.set_mode((largura, altura))
    
# Roda run_batuque
if __name__ == "__main__":
    try:
        run_batuque(screen)
    except Exception as e:
        print(f"Erro ao executar 'run_batuque': {e}")
        sys.exit(1)
