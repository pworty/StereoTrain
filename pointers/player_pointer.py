import pygame
import os

from pointers.pointer import Pointer


class PlayerPointer(Pointer):
    def __init__(self, player_rect):
        super().__init__(player_rect)
        self.pointer_img = None
        self.player_pointer = pygame.image.load(os.path.join("game_assets/pointers/Star_red.png"))
        self.pointer_rect = self.player_pointer.get_rect()

    def rotate_pointer(self, window, angle):
        """
        Allows to rotate player
        :param window: surface
        :param angle: int
        :return: None
        """
        self.pointer_img = pygame.transform.rotozoom(self.player_pointer, int(angle), 1)
        offset_rotated = self.offset.rotate(-angle)
        self.pointer_rect = self.pointer_img.get_rect(center=self.pos + offset_rotated)
        window.blit(self.pointer_img, self.pointer_rect)
