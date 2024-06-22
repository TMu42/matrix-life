import os
import sys

with open(os.devnull, 'w') as devnull:
    sys.stdout = devnull
    
    import pygame
    
    sys.stdout = sys.__stdout__


def initialize(args):
    pygame.init()
    
    icon = pygame.image.load("icon.ico")
    
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption("Matrix Life")
    
    surface = pygame.display.set_mode((args.width, args.height))
    
    return surface


def paint_board(surface, mat):
    surface.blit(pygame.surfarray.make_surface(-mat.T), (0, 0))
    
    pygame.display.flip()
