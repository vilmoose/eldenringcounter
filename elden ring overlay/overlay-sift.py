import cv2  # pip install opencv-contrib-python
import os
import numpy as np 
import pygetwindow as gw  # pip install pygetwindow Pillow
from PIL import ImageGrab
import pygame  # pip install pygame

# Set desired location for pygame frame (the counter)
window_width = 200
window_height = 100
x_pos = 1920 - window_width  # Adjust for your screen resolution
y_pos = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_width, window_height)  # To adjust change (x, y)

# Load the reference image
reference_image = cv2.imread('deathscreen.png', 0)

# Initialize the SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT in the reference image
kp1, des1 = sift.detectAndCompute(reference_image, None)
print(f"Reference image: {len(kp1)} keypoints found")

# Initialize the BFMatcher with default parameters
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

def detect_image(screen_frame):
    # Convert the screen frame to grayscale
    gray_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGR2GRAY)
    # Find the keypoints and descriptors with SIFT in the screen frame
    kp2, des2 = sift.detectAndCompute(gray_frame, None)
    if des2 is None:
        print("No descriptors found in frame")
        return False  # No descriptors found in the frame

    print(f"Screen frame: {len(kp2)} kepypoints found")
    # Use BFMatcher to find matches
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Apply ratio test
    good_matches = []
    for m_n in matches:  # changed m,n to m_n because of ValueError (from BFMatcher knnMatch returning less than two matches)
        if len(m_n) == 2:
            m, n = m_n
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)
    
    print(f"{len(good_matches)} good matches found")
    # If there are enough good matches, consider it a detection
    if len(good_matches) > 2:  # You can adjust this threshold
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
overlay_screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)

# Set transparency
overlay_screen.set_colorkey((0, 0, 0))

# Font for the counter
font = pygame.font.Font(None, 36)

counter = 0

def update_overlay():
    global counter
    overlay_screen.fill((0, 0, 0, 0))  # Clear the screen with transparency
    text = font.render(f'Deaths: {counter}', True, (255, 255, 255))
    overlay_screen.blit(text, (50, 50))
    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen_frame = capture_screen('Firefox')  # Enter the name of the application; for Elden Ring it's: "ELDEN RING"
    #screen_frame = capture_whole_screen()
    if detect_image(screen_frame):
        counter += 1
        print(f"counter: {counter}")
        
    update_overlay()
    pygame.time.delay(1000)  # Delay to reduce CPU usage

pygame.quit()
