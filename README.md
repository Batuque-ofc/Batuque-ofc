## 🌐 [English Version of README](README_EN.md)

# Projeto Batuque

O Projeto Batuque é uma aplicação interativa que combina detecção de cores e reprodução de sons de bateria. Utilizando a captura de vídeo em tempo real, o projeto toca diferentes sons de bateria baseados na presença de cores específicas detectadas pela câmera.

## 🔨 Funcionalidades do Projeto

- **Detecção de Cores**: Identifica cores específicas e toca sons correspondentes.
- **Reprodução de Sons em Tempo Real**: Sons de bateria são reproduzidos instantaneamente ao detectar as cores certas.
- **Interface Gráfica**: Tela inicial, opções de configuração e menu para iniciar o jogo.
- **Sincronização com Música**: Sons e efeitos visuais sincronizados com o ritmo da música.
- **Configuração Personalizada**: Permite ajustar a resolução da tela e o volume dos sons através de um menu de configurações.
- **Feedback Visual**: Sobreposição de imagens e efeitos visuais para indicar a detecção de cores e a reprodução de sons.
- **Tela de Login e Registro**: Funcionalidades para criar uma conta e acessar a aplicação com diferentes perfis de usuário.
- **Tutorial Interativo**: Áudios e instruções para guiar o usuário no uso do sistema.
- **Modo de Teste**: Scripts dedicados para testar a detecção de cores e a troca de áudios.

### Exemplo Visual do Projeto

![Screenshot 2024-08-11 211550](https://github.com/user-attachments/assets/a8d3dca2-70ed-4246-8350-34b1ec0b187b)
![Screenshot 2024-08-11 225320](https://github.com/user-attachments/assets/e3ebd3e8-0319-49c8-b83f-d77ef9b7bf95)
![image](https://github.com/user-attachments/assets/c1a1b929-dbf9-4468-a144-8868e009d5ed)

## ✔️ Técnicas e Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação principal.
- **OpenCV**: Biblioteca para processamento de imagem e captura de vídeo.
- **Pygame**: Biblioteca para criação da interface gráfica e manipulação de áudio.
- **NumPy**: Biblioteca para operações matemáticas e processamento de arrays.

## 📁 Estrutura do Projeto

- **batuque.py**: Implementa o funcionamento principal do projeto, incluindo a reprodução de sons.
- **batuque-teste (troca de audios).py**: Script para teste e troca de áudios.
- **interface.py**: Gerencia a interface gráfica com o usuário usando Pygame.
- **rodar_batuque.py**: Script para iniciar o projeto Batuque.
- **teste_cor_alvo_instrumentos.py**: Testa a detecção de cores para diferentes instrumentos.
- **LICENSE**: Arquivo de licença do projeto.
- **README.md**: Documento de descrição e instruções do projeto.
- **requirements.txt**: Lista de dependências do projeto.
- **screens/**: Diretório com arquivos relacionados às telas e menus do projeto.
    - `menu_resolucao.py`: Configurações de resolução de tela.
    - `menu_volume.py`: Configurações de volume.
    - `telaLogin.py`: Tela de login.
    - `telaRegistro.py`: Tela de registro.
- **src/Images/**: Diretório contendo imagens usadas no projeto.
    - `Bumbo.png`, `Bumbou.png`, `Caixa.png`, `Caixa2.png`, `Chimbal.png`, `Crash.png`: Imagens dos instrumentos.
    - `tela inicial/`: Imagens para a tela inicial, incluindo ícones e fundo.
- **src/sounds/**: Diretório contendo arquivos de áudio usados no projeto.
    - `Bumbo/`, `Caixa/`, `Caixa2/`, `Chimbal/`, `Crash/`: Pastas com sons para cada instrumento.
    - `Tutorial 1.wav`, `Tutorial 2.wav`: Áudios de tutorial.

## 🛠️ Abrir e Rodar o Projeto

Para iniciar o projeto localmente, siga os passos abaixo:

1. **Certifique-se de que o Python 3.x está instalado**:
    - Verifique se o Python está instalado com o comando:

      ```bash
      python --version
      ```

    - Se não estiver instalado, baixe e instale a versão recomendada do [Python](https://www.python.org/).

2. **Instale as Dependências**:
    - Certifique-se de que o arquivo `requirements.txt` está presente na raiz do projeto e instale as dependências com:

      ```bash
      pip install -r requirements.txt
      ```

3. **Clone o Repositório**:
    - Copie a URL do repositório e execute o comando abaixo no terminal:

      ```bash
      git clone <URL_DO_REPOSITORIO>
      ```

4. **Execute o Projeto**:
    - Navegue até o diretório do projeto e execute o script principal:

      ```bash
      python interface.py
      ```

## 🌐 Deploy

Para informações sobre como fazer o deploy do projeto, consulte o arquivo `DEPLOY.md` (se disponível) ou entre em contato com os mantenedores do projeto para orientações adicionais.
