import pygame


class Pointer:
    def __init__(self, player_rect):
        self.player_rect = player_rect
        self.pivot = self.player_rect.center
        self.pos = pygame.math.Vector2(self.player_rect.center)
        self.offset = pygame.math.Vector2(400, 0)
