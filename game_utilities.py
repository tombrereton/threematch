import os

import pygame
from pygame.compat import geterror
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'resources')


# ============================================
# load functions
# ============================================

def load_background(back: str, fore: str, width: int, height: int):
    fullname_1 = os.path.join(data_dir, back)
    fullname_2 = os.path.join(data_dir, fore)
    try:
        fore = pygame.image.load(fullname_2)
        fore = pygame.transform.smoothscale(fore, (width, height))
        # fore = fore.convert_alpha()
        back = pygame.image.load(fullname_1)
        back = pygame.transform.smoothscale(back, (width, height))
        # back = back.convert_alpha()
        merged = back.copy()
        merged.blit(fore, (0, int(0)))
    except pygame.error:
        print('Cannot load image:', fullname_1)
        raise SystemExit(geterror())

    return merged


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


def load_explosion(foreground: str, background: str, size: int):
    fullname_1 = os.path.join(data_dir, foreground)
    fullname_2 = os.path.join(data_dir, background)
    try:
        fore = pygame.image.load(fullname_1)
        fore = pygame.transform.smoothscale(fore, (size, size))
        fore = fore.convert_alpha()
        back = pygame.image.load(fullname_2)
        back = pygame.transform.smoothscale(back, (size, size))
        back = back.convert_alpha()
        merged = back.copy()
        merged.blit(fore, (0, 0))
    except pygame.error:
        print('Cannot load image:', fullname_1)
        raise SystemExit(geterror())

    # convert alpha makes the images transparent
    return merged


def load_image_only(name: str, size: int, colorkey=None, rotate=0):
    fullname = os.path.join(data_dir, name)
    size = int(size)
    try:
        image = pygame.image.load(fullname)

        if rotate:
            image = pygame.transform.rotate(image, rotate)

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
    return image


def load_border(name: str, length: int, height: int, colorkey=None, rotate=0):
    fullname = os.path.join(data_dir, name)
    length = int(length)
    height = int(height)
    try:
        image = pygame.image.load(fullname)

        if rotate:
            image = pygame.transform.rotate(image, rotate)

        image = pygame.transform.smoothscale(image, (length, height))
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(geterror())

    # convert alpha makes the images transparent
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


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
