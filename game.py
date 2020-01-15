import pygame
import os
import math

from player_pointer import PlayerPointer
from sound_source import SoundSource

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game:
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window_rect = self.window.get_rect()
        self.bg = pygame.Color("black")

        self.animation_count = 0
        self.sound_delay = 0
        self.player_images = [
            pygame.image.load(
                os.path.join("game_assets/player/idle", "survivor-idle_rifle_" + str(x) + ".png"))
            for x in range(0, 20)]
        self.img = self.player_images[0]
        self.player_rect = self.img.get_rect()
        self.player_rect.center = self.window_rect.center
        self.rotation = False
        self.angle = 0

        self.pointer_img = None
        self.pointer_rect = None

        self.show = True
        self.sound_source = SoundSource(self.player_rect)
        self.player_pointer = PlayerPointer(self.player_rect)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        fps = 60
        pos = None
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    self.rotation = True
                else:
                    self.rotation = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass

            self.draw(pos)
            self.play_sound()

        pygame.quit()

    def draw(self, pos):
        self.window.fill((0, 0, 0))
        if int(self.animation_count) >= len(self.player_images):
            self.animation_count = 0
        self.img = self.player_images[int(self.animation_count)]
        self.rotate_player(pos)
        self.window.blit(self.img, self.player_rect)
        pygame.display.update()
        self.animation_count += 0.5

    def rotate_player(self, pos):
        mouse_x, mouse_y = pos
        rel_x, rel_y = mouse_x - self.width / 2, mouse_y - self.height / 2
        if self.rotation:
            self.angle = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
        self.img = pygame.transform.rotozoom(self.img, self.angle, 1)
        x, y = self.player_rect.center
        self.player_rect = self.img.get_rect()
        self.player_rect.center = (x, y)
        if self.show is True:
            self.sound_source.place_source_pointer(self.window)
            self.player_pointer.rotate_pointer(self.window, self.angle)

    def play_sound(self):
        if self.sound_delay == 120:
            self.sound_source.play_hint(self.angle)
            self.sound_delay = 0
        self.sound_delay += 1

    def guess(self):
        pass

    def show_hint(self):
        if self.show is True:
            self.show = False
        else:
            self.show = True

    def reset(self):
        pass


g = Game()
g.run()
