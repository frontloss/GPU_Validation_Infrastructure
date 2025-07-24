########################################################################################################################
# @file         launch_frame.py
# @brief        Test for XPST kei scenarios
# @author       Tulika
########################################################################################################################
import argparse
import os
import pygame
from ctypes import windll

windll.user32.SetProcessDPIAware()

parser = argparse.ArgumentParser(description='Process the Command line Arguments.')
parser.add_argument('-WIDTH', default=1920, type=str, help='Width of panel')
parser.add_argument('-HEIGHT', default=1080, type=str, help='Height of panel')
args = parser.parse_args()

width = int(args.WIDTH)
height = int(args.HEIGHT)

pygame.init()

screen = pygame.display.set_mode((width, height))
path = os.path.join(os.getcwd().split("\\dist")[0], "Logs\\DpstKeiImages")
image_files = [f for f in os.listdir(path) if f.endswith(".png")]
images = [pygame.image.load(os.path.join(path, f)) for f in image_files]
current_image = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                current_image = (current_image - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                current_image = (current_image + 1) % len(images)

    # Display the current image
    screen.blit(images[current_image], (0, 0))
    pygame.display.flip()

pygame.quit()
