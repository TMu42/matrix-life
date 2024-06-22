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
    
    print(f"w: {args.resolution_width}; b: {args.resolution_breadth}")
    
    surface = pygame.display.set_mode((args.resolution_width,
                                       args.resolution_breadth))
    
    return surface


def paint_board(surface, mat):
    life_grid = pygame.surfarray.make_surface(-mat.T)
    
    surface.blit(pygame.transform.scale(life_grid, surface.get_rect()[2:]),
                                                                        (0, 0))
    
    pygame.display.flip()
