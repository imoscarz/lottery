import pygame
import sys
import os
from pygame.locals import *
from config import *


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.normpath(os.path.join(base_path,relative_path))


class Text:
    def __init__(self, text: str, font_name, color, font_size):
        """
        text: Text to render
        font_name: Filename of font (in assests directory)
        color: Color of the text
        font_size: Scale of the text
        """
        self.text = text
        self.color = color
        self.font_type = get_path(f'assets/fonts/{font_name}')
        self.font_size = font_size
        font = pygame.font.Font(self.font_type, self.font_size)
        self.text_image = font.render(
            self.text, True, self.color).convert_alpha()
        self.text_width = self.text_image.get_width()
        self.text_height = self.text_image.get_height()

    def draw(self, canvas: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.text_width / 2
        upperleft_y = center_y - self.text_height / 2
        canvas.blit(self.text_image, (upperleft_x, upperleft_y))


class Image:
    def __init__(self, img_name, ratio=GLOBAL_RATIO):
        self.img_name = img_name
        self.ratio = ratio
        self.image_original = pygame.image.load(
            get_path(f'assets/images/{self.img_name}')).convert_alpha()
        self.image_width = self.image_original.get_width()
        self.image_height = self.image_original.get_height()

        self.size_scaled = (self.image_width * self.ratio,
                            self.image_height * self.ratio)
        self.image_scaled = pygame.transform.smoothscale(
            self.image_original, self.size_scaled)
        self.img_width_scaled = self.image_scaled.get_width()
        self.img_height_scaled = self.image_scaled.get_height()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.img_width_scaled / 2
        upperleft_y = center_y - self.img_height_scaled / 2
        surface.blit(self.image_scaled, (upperleft_x, upperleft_y))


class ImageFixed:
    def __init__(self, img_name, width: int, height: int):
        self.img_name = img_name
        self.image_original = pygame.image.load(
            get_path(f'assets/images/{self.img_name}')).convert_alpha()
        self.image_width = self.image_original.get_width()
        self.image_height = self.image_original.get_height()
        self.ratio = max(width / self.image_width, height / self.image_height)

        self.size_scaled = (self.image_width * self.ratio,
                            self.image_height * self.ratio)
        self.image_scaled = pygame.transform.smoothscale(
            self.image_original, self.size_scaled).subsurface(0,0,width,height)
        self.img_width_scaled = self.image_scaled.get_width()
        self.img_height_scaled = self.image_scaled.get_height()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.img_width_scaled / 2
        upperleft_y = center_y - self.img_height_scaled / 2
        surface.blit(self.image_scaled, (upperleft_x, upperleft_y))


class ColorSurface:
    def __init__(self, color, width, height, alpha):
        self.color = color
        self.width = width
        self.height = height
        self.alpha = alpha
        self.color_image = pygame.Surface(
            (self.width, self.height)).convert_alpha()
        self.color_image.fill(self.color)
        self.color_image.set_alpha(alpha)

    def draw(self, surface: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.width / 2
        upperleft_y = center_y - self.height / 2
        surface.blit(self.color_image, (upperleft_x, upperleft_y))


class ButtonText(Text):
    def __init__(self, text: str, text_color, font_type: str, font_size: int):
        super().__init__(text, text_color, font_type, font_size)
        self.rect = self.text_image.get_rect()

    def draw(self, canvas: pygame.Surface, center_x, center_y):
        super().draw(canvas, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command, *argv):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command(*argv)


class ButtonImage(Image):
    def __init__(self, img_name: str, ratio=0.4):
        super().__init__(img_name, ratio)
        self.rect = self.image_scaled.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command, *args):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command(*args)


class ButtonColorSurface(ColorSurface):
    def __init__(self, color, width, height, alpha):
        super().__init__(color, width, height, alpha)
        self.rect = self.color_image.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, command, *args):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.hovered:
            command(*args)
