import cv2  # pip install opencv-contrib-python
import os
import numpy as np 
import pygetwindow as gw  # pip install pygetwindow Pillow
from PIL import ImageGrab
import pygame  # pip install pygame
import time
import win32gui
import win32con

# Set desired location for pygame frame (the counter)
window_width = 200
window_height = 100
x_pos = 1920 - window_width  # Adjust for your screen resolution
y_pos = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1200, 0)  # To adjust change (x, y)

# Load the reference image
reference_image = cv2.imread('deathscreen3.png', 0)

# Initialize the SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT in the reference image
kp1, des1 = sift.detectAndCompute(reference_image, None)
print(f"Reference image: {len(kp1)} keypoints found")

# Initialize the BFMatcher with default parameters
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

# compares screenshot provided with existing reference image and determines if they are similar
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
    if len(good_matches) > 9:  # You can adjust this threshold, using 1-3 as it seems the best
        return True
    return False

# Captures a screenshot of application screen
def capture_screen(window_title):
    game_window = gw.getWindowsWithTitle(window_title)[0]
    bbox = (game_window.left, game_window.top, game_window.right, game_window.bottom)
    screen = ImageGrab.grab(bbox)
    screen_np = np.array(screen)
    return screen_np

# Captures a screenshot of whole screen
def capture_whole_screen():
    screen = ImageGrab.grab()
    screen_np = np.array(screen)
    return screen_np

# Save # of deaths
def save_death_counter(counter, filename="death_count.txt"):
    with open(filename, 'w') as file:
        file.write(str(counter)) #write counter into file
        
# Load # of deaths
def load_death_counter(filename="death_count.txt"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            content = file.read().strip()
            if content.isdigit():
                return int(content) #read counter from file
            else:
                return 0
    else:
        return 0
    
# Initialize Pygame
pygame.init()

# Create the overlay window
overlay_screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)

# Set transparency
overlay_screen.set_colorkey((0, 0, 0))

# Font for the counter
font = pygame.font.Font(None, 36)

counter = load_death_counter() #loads the death counter from last time program was closed

def update_overlay():
    global counter
    overlay_screen.fill((0, 0, 0, 0))  # Clear the screen with transparency
    text = font.render(f'Deaths: {counter}', True, (255, 255, 255))
    overlay_screen.blit(text, (50, 50))
    pygame.display.flip()

# Get the window handle
hwnd = pygame.display.get_wm_info()['window']

# Keep window of pygame on top of all other applications
def set_window_on_top(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
set_window_on_top(hwnd)

# Main loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen_frame = capture_screen('ELDEN RING')  # Enter the name of the application; for Elden Ring it's: "ELDEN RING"
    ##screen_frame = capture_screen('Firefox')
    screen_frame = capture_whole_screen()
    if detect_image(screen_frame):
        counter += 1
        print(f"counter: {counter}")
        save_death_counter(counter)
        #add delay for when it finds it so it doesnt count twice
        time.sleep(1.5)
    update_overlay()
    pygame.time.delay(1000)  # Delay to reduce CPU usage

save_death_counter(counter)
pygame.quit()
