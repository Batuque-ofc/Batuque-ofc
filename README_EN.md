## 🌐 [Versão em Português do README](README.md)

# Batuque Project

The Batuque Project is an interactive application that combines color detection with drum sound playback. Using real-time video capture, the project plays different drum sounds based on the presence of specific colors detected by the camera.

## 🔨 Project Features

- **Color Detection**: Identifies specific colors and plays corresponding sounds.
- **Real-Time Sound Playback**: Drum sounds are played instantly upon detecting the correct colors.
- **Graphical User Interface**: Includes a start screen, configuration options, and a menu to start the game.
- **Music Synchronization**: Sounds and visual effects are synchronized with the rhythm of the music.
- **Custom Configuration**: Allows users to adjust screen resolution and sound volume through a settings menu.
- **Visual Feedback**: Overlays images and visual effects to indicate color detection and sound playback.
- **Login and Registration Screen**: Features for creating an account and accessing the application with different user profiles.
- **Interactive Tutorial**: Audio and instructions to guide users in using the system.
- **Test Mode**: Dedicated scripts for testing color detection and audio switching.

### Visual Example of the Project

![Screenshot 2024-08-11 211550](https://github.com/user-attachments/assets/a8d3dca2-70ed-4246-8350-34b1ec0b187b)
![Screenshot 2024-08-11 225320](https://github.com/user-attachments/assets/e3ebd3e8-0319-49c8-b83f-d77ef9b7bf95)
![image](https://github.com/user-attachments/assets/c1a1b929-dbf9-4468-a144-8868e009d5ed)

## ✔️ Techniques and Technologies Used

- **Python 3.x**: Main programming language.
- **OpenCV**: Library for image processing and video capture.
- **Pygame**: Library for creating the graphical interface and handling audio.
- **NumPy**: Library for mathematical operations and array processing.

## 📁 Project Structure

- **batuque.py**: Implements the main functionality of the project, including sound playback.
- **batuque-teste (troca de audios).py**: Script for testing and swapping audio.
- **interface.py**: Manages the graphical user interface using Pygame.
- **rodar_batuque.py**: Script to start the Batuque project.
- **teste_cor_alvo_instrumentos.py**: Tests color detection for different instruments.
- **LICENSE**: Project license file.
- **README.md**: Description and instructions document for the project.
- **requirements.txt**: List of project dependencies.
- **screens/**: Directory with files related to project screens and menus.
    - `menu_resolucao.py`: Screen resolution settings.
    - `menu_volume.py`: Volume settings.
    - `telaLogin.py`: Login screen.
    - `telaRegistro.py`: Registration screen.
- **src/Images/**: Directory containing images used in the project.
    - `Bumbo.png`, `Bumbou.png`, `Caixa.png`, `Caixa2.png`, `Chimbal.png`, `Crash.png`: Images of the instruments.
    - `tela inicial/`: Images for the start screen, including icons and background.
- **src/sounds/**: Directory containing audio files used in the project.
    - `Bumbo/`, `Caixa/`, `Caixa2/`, `Chimbal/`, `Crash/`: Folders with sounds for each instrument.
    - `Tutorial 1.wav`, `Tutorial 2.wav`: Tutorial audio files.

## 🛠️ Running the Project

To start the project locally, follow these steps:

1. **Ensure Python 3.x is Installed**:
    - Check if Python is installed with the command:

      ```bash
      python --version
      ```

    - If not installed, download and install the recommended version of [Python](https://www.python.org/).

2. **Install Dependencies**:
    - Ensure that the `requirements.txt` file is present in the project root and install dependencies with:

      ```bash
      pip install -r requirements.txt
      ```

3. **Clone the Repository**:
    - Copy the repository URL and run the following command in the terminal:

      ```bash
      git clone <REPOSITORY_URL>
      ```

4. **Run the Project**:
    - Navigate to the project directory and execute the main script:

      ```bash
      python interface.py
      ```

## 🌐 Deployment

For information on how to deploy the project, refer to the `DEPLOY.md` file (if available) or contact the project maintainers for further guidance.
