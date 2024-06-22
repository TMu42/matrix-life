import os
import sys
import numpy


ZERO_RED   = 31
ZERO_GREEN =  1
ZERO_BLUE  = 46

ONE_RED   =  29
ONE_GREEN = 206
ONE_BLUE  = 166


with open(os.devnull, 'w') as devnull:
    sys.stdout = devnull
    
    import pygame
    
    sys.stdout = sys.__stdout__


def initialize(args):
    pygame.init()
    
    icon = pygame.image.load("icon.ico")
    
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption("Matrix Life")
    
    surface = pygame.display.set_mode((args.resolution_width,
                                       args.resolution_breadth))
    
    return surface


def paint_board(surface, mat):
    red_pixels   = (ONE_RED   - ZERO_RED  )*numpy.atleast_3d(mat.T) + ZERO_RED
    green_pixels = (ONE_GREEN - ZERO_GREEN)*numpy.atleast_3d(mat.T) + ZERO_GREEN
    blue_pixels  = (ONE_BLUE  - ZERO_BLUE )*numpy.atleast_3d(mat.T) + ZERO_BLUE
    
    life_pixels = numpy.append(
                        red_pixels, numpy.append(green_pixels,
                                                 blue_pixels, axis=2), axis=2)
    
    #print(f"life_pixels.shape: {life_pixels.shape}")
    
    life_surface = pygame.surfarray.make_surface(life_pixels)
    
    surface.blit(pygame.transform.scale(life_surface, surface.get_rect()[2:]),
                 (0, 0))
    
    pygame.display.flip()
