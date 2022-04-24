# import library here
import pygame
import time
import sys

# display init
display_width = 800
display_height = 600

# game initialization done
pygame.init()

# game display changed
gameDisplay = pygame.display.set_mode((display_width, display_height))

# init font object with font size 25 
font = pygame.font.SysFont(None, 25)

def message_to_display(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, (10, 10))

message_to_display("You Lose", (255,0,0))
pygame.display.update()  # VERY IMPORTANT! THIS IS WHAT YOU MISSED!
time.sleep(3)

pygame.quit()
# you can signoff now, everything looks good!
quit()