import cv2  #pip install opencv-python
import os
import numpy as np 
import pygetwindow as gw #pip install pygetwindow Pillow
from PIL import ImageGrab
import pygame #pip install pygame

# #code for using tesseract
# #tesseract used to read text from screen but not using it
# import pytesseract #pip install pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\vilmo\anaconda3\Scripts\pytesseract.exe'

# def detect_text(screen_frame, text_to_find):
#     #convert the screen frame to grayscale
#     gray_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2GRAY)
#     #perform optical character recogintion
#     detected_text = pytesseract.image_to_string(gray_frame)
#     if text_to_find in detected_text:
#         return True
#     return False

#set desired location for pygame frame (thes window to display the counter)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1250, 0) #to adjust change (x,y)

#load the reference image
reference_image = cv2.imread('deathscreen.png', 0)
w, h = reference_image.shape[::-1] 

def detect_image(screen_frame):
    #convert the screen frame to grayscale
    gray_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2GRAY)
    #apply template matching
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

#initialize Pygame
pygame.init()

#create the overlay window
overlay_screen = pygame.display.set_mode((200, 100), pygame.NOFRAME)

#set transparency
overlay_screen.set_colorkey((0, 0, 0))

#font for the counter
font = pygame.font.Font(None, 36)

counter = 0

def update_overlay():
    global counter
    overlay_screen.fill((0, 0, 0, 0))  #clear the screen with transparency
    text = font.render(f'Deaths: {counter}', True, (255, 255, 255))
    overlay_screen.blit(text, (50, 50))
    pygame.display.flip()

#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen_frame = capture_screen('Firefox') #enter name of application; for elden ring its: "ELDEN RING"
    #screen_frame = capture_whole_screen()
    if detect_image(screen_frame):
        counter += 1

    #if using tesseract uncomment 
    # if detect_text(screen_frame, 'YOU DIED'):
    #     counter += 1
        
    update_overlay()
    pygame.time.delay(1000)  #delay to reduce CPU usage

pygame.quit()
