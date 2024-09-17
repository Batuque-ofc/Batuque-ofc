import sys
from batuque import run_batuque

# Roda run_batuque
if __name__ == "__main__":
    try:
        run_batuque()
    except Exception as e:
        print(f"Erro ao executar 'run_batuque': {e}")
        sys.exit(1)
