import pygame


def draw_basic_text(surface, text, font_name, size, x, y, color):
    """
    The class used to draw text on the screen. May be primarily used for the start screen

    Args:

        surface: The Screen in which this text will be rendered
        text: The string of the words to be tisplayed on the surface
        font_name: The name of the font used to display the text
        size: The size of the text
        x: X value for the rect of the text
        y: Y value for the rect of the text
        color: The color of the Text

    Returns:
        Blits the text to the provided screen.

    """
    pygame.init()
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
