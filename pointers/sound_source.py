import pygame
import os
import random

from pointers.pointer import Pointer


class SoundSource(Pointer):
    def __init__(self, player_rect):
        super().__init__(player_rect)
        self.source_img = None
        self.source_pointer = pygame.image.load(os.path.join(
            "game_assets/pointers/Star_yellow.png"))
        self.source_rect = self.source_pointer.get_rect()
        self.angle = random.randint(0, 360)

        self.hint_sound = pygame.mixer.Sound("game_assets/sound_effects/hint.wav")
        self.channel = pygame.mixer.Channel(0)
        self.vol_left = 0
        self.vol_right = 0

    def place_source_pointer(self, window):
        """
        Places sound source star mark
        :param window: surface
        :return: None
        """
        self.source_img = pygame.transform.rotozoom(self.source_pointer, int(self.angle), 1)
        offset_rotated = self.offset.rotate(-self.angle)
        self.source_rect = self.source_img.get_rect(center=self.pos + offset_rotated)
        window.blit(self.source_img, self.source_rect)

    def play_hint(self, angle):
        """
        Plays sound with regard to mark position (adjusting left and right channel volume)
        :param angle: int
        :return: None
        """
        # Calculate the volume in each channel using angle player is looking at
        new_angle = (angle - self.angle) % 360
        if new_angle >= 180:
            self.vol_left = 1
            if new_angle <= 270:
                self.vol_right = (270 - new_angle) / 90
            elif new_angle > 270:
                self.vol_right = (new_angle - 180) / 90
        elif new_angle < 180:
            self.vol_right = 1
            if new_angle >= 90:
                self.vol_left = (new_angle - 90) / 90
            elif new_angle < 90:
                self.vol_left = (90 - new_angle) / 90
        self.channel.set_volume(self.vol_left, self.vol_right)
        self.hint_sound.play()
