import pygame
import os
import math

from player_pointer import PlayerPointer
from sound_source import SoundSource
from menu.button import Button


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

        self.show_hint = False
        self.sound_source = SoundSource(self.player_rect)
        self.player_pointer = PlayerPointer(self.player_rect)

        self.idle_color = (0, 0, 0)
        self.active_color = (255, 255, 255)
        self.outline_color = (255, 255, 255)
        self.text_idle_color = (255, 255, 255)
        self.text_active_color = (0, 0, 0)
        self.start_guess_btn = Button(self.idle_color, 1400, 800, 190, 90, 'Start',
                                      self.text_idle_color)
        self.reset_btn = Button(self.idle_color, 10, 10, 190, 90, 'Reset', self.text_idle_color)
        self.show_pointers_btn = Button(self.idle_color, 1400, 10, 190, 90, 'Show',
                                        self.text_idle_color)
        self.buttons = [self.start_guess_btn, self.reset_btn, self.show_pointers_btn]

        self.game_over = False

    def run(self):
        run = True
        clock = pygame.time.Clock()
        fps = 60
        pos = None
        pressed = False
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    if pressed is False:
                        if self.start_guess_btn.is_over(pos):
                            if self.start_guess_btn.text == 'Start':
                                if self.game_over:
                                    run = False
                                    return True
                                else:
                                    self.start_guess_btn.text = 'Guess'
                            elif self.start_guess_btn.text == 'Guess':
                                if abs(self.angle - self.sound_source.angle) <= 10 or abs(
                                        self.angle + 360 - self.sound_source.angle) <= 10:
                                    self.start_guess_btn.text = 'Start'
                                    self.show_hint = True
                                    self.game_over = True
                        elif self.show_pointers_btn.is_over(pos):
                            if self.show_hint is True:
                                self.show_hint = False
                            else:
                                self.show_hint = True
                        elif self.reset_btn.is_over(pos):
                            run = False
                            return True
                        else:
                            self.rotation = True
                        pressed = True
                else:
                    self.rotation = False
                    pressed = False

            self.draw(pos)
            if self.start_guess_btn.text == 'Guess':
                self.play_sound()

        pygame.quit()

    def draw(self, pos):
        self.window.fill((0, 0, 0))
        if int(self.animation_count) >= len(self.player_images):
            self.animation_count = 0
        self.img = self.player_images[int(self.animation_count)]
        self.rotate_player(pos)
        self.window.blit(self.img, self.player_rect)
        for btn in self.buttons:
            btn.draw(self.window, self.outline_color)
            if btn.is_over(pos):
                btn.color = self.active_color
                btn.text_color = self.text_active_color
            else:
                btn.color = self.idle_color
                btn.text_color = self.text_idle_color
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
        if self.show_hint is True:
            self.sound_source.place_source_pointer(self.window)
            self.player_pointer.rotate_pointer(self.window, self.angle)

    def play_sound(self):
        if self.sound_delay == 120:
            self.sound_source.play_hint(self.angle)
            self.sound_delay = 0
        self.sound_delay += 1


def main(restart):
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    g = Game()
    if restart:
        g.start_guess_btn.text = 'Guess'
    if g.run():
        main(True)


main(False)
pygame.quit()
