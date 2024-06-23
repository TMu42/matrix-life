import os
import sys
import numpy


ZERO_R =  31
ZERO_G =   1
ZERO_B =  46

ONE_R  =  29
ONE_G  = 206
ONE_B  = 166


with open(os.devnull, 'w') as devnull:
    sys.stdout = devnull
    
    import pygame
    
    sys.stdout = sys.__stdout__


def initialize(args):
    global running, paused
    
    pygame.init()
    
    icon = pygame.image.load("icon.ico")
    
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption("Matrix Life")
    
    if args.fullscreen:
        surface = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    else:
        surface = pygame.display.set_mode((args.resolution_width,
                                           args.resolution_breadth),
                                          pygame.RESIZABLE)
    
    running = True
    
    paused = False
    
    return surface


def paint_board(surface, mat):
    r_pixels = (ONE_R - ZERO_R)*numpy.atleast_3d(mat.T) + ZERO_R
    g_pixels = (ONE_G - ZERO_G)*numpy.atleast_3d(mat.T) + ZERO_G
    b_pixels = (ONE_B - ZERO_B)*numpy.atleast_3d(mat.T) + ZERO_B
    
    life_pixels = numpy.concatenate((r_pixels, g_pixels, b_pixels), axis=2)
    
    life_surface = pygame.surfarray.make_surface(life_pixels)
    
    life_surface = pygame.transform.scale(life_surface, surface.get_rect()[2:])
    
    surface.blit(life_surface, (0, 0))
    
    pygame.display.flip()


def events():
    global running, paused
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
