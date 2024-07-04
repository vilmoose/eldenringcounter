import cv2  #pip install opencv-python
import numpy as np 
import pygetwindow as gw #pip install pygetwindow Pillow
from PIL import ImageGrab
import pygame #pip install pygame

# Load the reference image
reference_image = cv2.imread('deathscreen.png', 0)
w, h = reference_image.shape[::-1]

def detect_image(screen_frame):
    # Convert the screen frame to grayscale
    gray_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2GRAY)
    # Apply template matching
    result = cv2.matchTemplate(gray_frame, reference_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        return True
    return False

def capture_screen(window_title):
    game_window = gw.getWindowsWithTitle(window_title)[0]
    bbox = (game_window.left, game_window.top, game_window.right, game_window.bottom)
    screen = ImageGrab.grab(bbox)
    screen_np = np.array(screen)
    return screen_np

def capture_whole_screen():
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    return screen_np

# Initialize Pygame
pygame.init()

# Create the overlay window
overlay_screen = pygame.display.set_mode((200, 200), pygame.NOFRAME)

# Set transparency
overlay_screen.set_colorkey((0, 0, 0))

# Font for the counter
font = pygame.font.Font(None, 36)

counter = 0

def update_overlay():
    global counter
    overlay_screen.fill((0, 0, 0, 0))  # Clear the screen with transparency
    text = font.render(f'Count: {counter}', True, (255, 255, 255))
    overlay_screen.blit(text, (50, 50))
    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen_frame = capture_screen('Photos')
    #screen_frame = capture_whole_screen()
    if detect_image(screen_frame):
        counter += 1

    update_overlay()
    pygame.time.delay(1000)  # Delay to reduce CPU usage

pygame.quit()
