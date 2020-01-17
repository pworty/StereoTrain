import pygame
import os
import random


class SoundSource:
    def __init__(self, player_rect):
        self.player_rect = player_rect
        self.pivot = self.player_rect.center
        self.pos = pygame.math.Vector2(self.player_rect.center)
        self.offset = pygame.math.Vector2(400, 0)
        self.source_img = None
        self.source_pointer = pygame.image.load(os.path.join("game_assets/pointers/Star_yellow.png"))
        self.source_rect = self.source_pointer.get_rect()
        self.angle = random.randint(0, 360)

        self.hint_sound = pygame.mixer.Sound("game_assets/sound_effects/hint.wav")
        self.channel = pygame.mixer.Channel(0)
        self.vol_left = 0
        self.vol_right = 0

    def place_source_pointer(self, window):
        self.source_img = pygame.transform.rotozoom(self.source_pointer, int(self.angle), 1)
        offset_rotated = self.offset.rotate(-self.angle)
        self.source_rect = self.source_img.get_rect(center=self.pos + offset_rotated)
        window.blit(self.source_img, self.source_rect)

    def play_hint(self, angle):
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
