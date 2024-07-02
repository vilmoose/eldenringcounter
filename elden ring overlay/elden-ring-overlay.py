import pyautogui #done by "pip install pyautogui"
import pygame #done by "pip install pygame"

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
SCREEN_HEIGHT, SCREEN_WIDTH = 200, 400
text_font = pygame.font.SysFont("Arial", 30, bold = True) #text font
running = True #variable to control while loop
#screenWidth, screenHeight = pyautogui.size() #get dimensions

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
deathCounter = 0
while running:
    #for loop to check when screen displays you died
    for txt in pyautogui.locateOnScreen('deathscreen.png', region=(750,510,300,100)):
        deathCounter += 1
        draw_text("Death Counter" + deathCounter, text_font, (0,0,0), )

    