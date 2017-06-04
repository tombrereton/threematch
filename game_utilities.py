import os

import pygame
from pygame.compat import geterror
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'resources')


# ============================================
# load functions
# ============================================

def load_background(name: str, width: int, height: int):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.smoothscale(image, (width, height))
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(geterror())

    # convert alpha makes the images transparent
    image = image.convert_alpha()
    return image


def load_image(name: str, size: int, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.smoothscale(image, (size, size))
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(geterror())

    # convert alpha makes the images transparent
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name: str):
    class NoneSound:
        def play(self): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


def load_explosions(size: int):
    explosions = []

    for i in range(9):
        name = "explosions/Explosion/explosion0{}.png".format(i)
        fullname = os.path.join(data_dir, name)
        try:
            image = pygame.image.load(fullname)
            image = pygame.transform.smoothscale(image, (size, size))
        except pygame.error:
            print('Cannot load image:', fullname)
            raise SystemExit(geterror())

        # convert alpha makes the images transparent
        image = image.convert_alpha()
        explosions.append(image)

    return explosions
