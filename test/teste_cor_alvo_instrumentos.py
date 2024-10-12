import cv2
import numpy as np
#from batuque import pinkLower as initial_pinkLower, pinkUpper as initial_pinkUpper

# Configurações de cor para detecção
h_low, h_high = 146, 172
s_low, s_high = 116, 255
v_low, v_high = 123, 255
initial_pinkLower = (h_low, s_low, v_low)
initial_pinkUpper = (h_high, s_high, v_high)
def nothing(x):
    pass

cv2.namedWindow('Trackbars and Pink Color', cv2.WINDOW_NORMAL)

# Cria trackbars para ajustar os valores HSV para rosa
cv2.createTrackbar('Pink Hue Low', 'Trackbars and Pink Color', initial_pinkLower[0], 179, nothing)
cv2.createTrackbar('Pink Hue High', 'Trackbars and Pink Color', initial_pinkUpper[0], 179, nothing)
cv2.createTrackbar('Pink Sat Low', 'Trackbars and Pink Color', initial_pinkLower[1], 255, nothing)
cv2.createTrackbar('Pink Sat High', 'Trackbars and Pink Color', initial_pinkUpper[1], 255, nothing)
cv2.createTrackbar('Pink Val Low', 'Trackbars and Pink Color', initial_pinkLower[2], 255, nothing)
cv2.createTrackbar('Pink Val High', 'Trackbars and Pink Color', initial_pinkUpper[2], 255, nothing)

# Função para obter os valores dos trackbars
def get_trackbar_values():
    pink_h_low = cv2.getTrackbarPos('Pink Hue Low', 'Trackbars and Pink Color')
    pink_h_high = cv2.getTrackbarPos('Pink Hue High', 'Trackbars and Pink Color')
    pink_s_low = cv2.getTrackbarPos('Pink Sat Low', 'Trackbars and Pink Color')
    pink_s_high = cv2.getTrackbarPos('Pink Sat High', 'Trackbars and Pink Color')
    pink_v_low = cv2.getTrackbarPos('Pink Val Low', 'Trackbars and Pink Color')
    pink_v_high = cv2.getTrackbarPos('Pink Val High', 'Trackbars and Pink Color')

    return (pink_h_low, pink_s_low, pink_v_low), (pink_h_high, pink_s_high, pink_v_high)

# Função para converter valores HSV para BGR
def hsv_to_bgr(hsv_color):
    hsv_color = np.uint8([[hsv_color]])
    bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return bgr_color

# Função para criar um patch de cor
def create_color_patch(color_lower, color_upper):
    color_patch = np.zeros((100, 300, 3), np.uint8)
    bgr_color_lower = hsv_to_bgr(color_lower)
    bgr_color_upper = hsv_to_bgr(color_upper)
    color_patch[:50] = bgr_color_lower
    color_patch[50:] = bgr_color_upper
    return color_patch

# Função para detectar a cor rosa no frame
def detect_color(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result, mask

camera = cv2.VideoCapture(0)

while True:
    # Captura um frame da câmera
    ret, frame = camera.read()
    if not ret:
        break

    # Atualiza os valores HSV com base nos trackbars
    pinkLower, pinkUpper = get_trackbar_values()

    # Detecta a cor que queremos
    detected_color, mask = detect_color(frame, pinkLower, pinkUpper)

    # Cria o patch da cor
    color_patch_pink = create_color_patch(pinkLower, pinkUpper)

    cv2.imshow('Original Frame', frame)
    cv2.imshow('Detected Pink Color', detected_color)
    cv2.imshow('Trackbars and Pink Color', color_patch_pink)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
camera.release()
cv2.destroyAllWindows()
