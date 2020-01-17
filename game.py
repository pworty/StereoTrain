import pygame
import os
import math
import webbrowser

from pointers.player_pointer import PlayerPointer
from pointers.sound_source import SoundSource
from menu.button import Button
from menu.main_menu import MainMenu


class Game:
    def __init__(self, restart):
        self.width = 1600
        self.height = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window_rect = self.window.get_rect()
        self.bg = pygame.Color("black")

        self.animation_count = 0
        self.sound_delay = 0

        # Load images for animation
        self.player_images = [
            pygame.image.load(
                os.path.join("game_assets/player/idle", "survivor-idle_rifle_" + str(x) + ".png"))
            for x in range(0, 20)]

        self.img = self.player_images[0]
        self.player_rect = self.img.get_rect()
        self.player_rect.center = self.window_rect.center
        self.rotation = False
        self.angle = 0
        # Precision needed to find sound source (it's proximity)
        self.precision = 10

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
        self.show_pointers_btn = Button(self.idle_color, 10, 800, 190, 90, 'Show',
                                        self.text_idle_color)
        self.help_btn = Button(self.idle_color, 1500, 10, 90, 90, '?', self.text_idle_color)
        self.buttons = [self.start_guess_btn, self.reset_btn, self.show_pointers_btn, self.help_btn]

        self.restart = restart
        self.game_over = False

    def run(self):
        # Start with main menu only on first launch
        if not self.restart:
            main_menu_btn = MainMenu(self.idle_color, 672, 390, 256, 120, 'StereoTrain',
                                     self.text_idle_color)
            main_menu_btn.main_menu(self.window)
        run = True
        clock = pygame.time.Clock()
        fps = 60
        pos = (0, 0)
        pressed = False
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    # If you click on button and hold, it doesn't click on it every time you move
                    # your mouse
                    if pressed is False:
                        if self.start_guess_btn.is_over(pos):
                            if self.start_guess_btn.text == 'Start':
                                # It's either the start or the end of the game
                                if self.game_over:
                                    run = False
                                    return True
                                else:
                                    self.start_guess_btn.text = 'Guess'
                            elif self.start_guess_btn.text == 'Guess':
                                # Check if player pointer is in close proximity to sound source
                                proximity = self.angle - self.sound_source.angle
                                if abs(proximity) <= self.precision or abs(
                                        proximity + 360) <= self.precision:
                                    self.start_guess_btn.text = 'Start'
                                    self.show_hint = True
                                    self.game_over = True
                        elif self.show_pointers_btn.is_over(pos):
                            # Switch show/hide pointers
                            if self.show_hint is True:
                                self.show_hint = False
                            else:
                                self.show_hint = True
                        elif self.reset_btn.is_over(pos):
                            # Quit game cycle and restart from run.py
                            run = False
                            return True
                        elif self.help_btn.is_over(pos):
                            # Open game presentation (Russian only)
                            webbrowser.open(
                                "https://docs.google.com/presentation/"
                                "d/104w1E_uxu9TKOo_dz8Pt4-TWiG84I_zt_pW4fhC-p2U/edit?usp=sharing")
                        else:
                            self.rotation = True
                        pressed = True
                else:
                    self.rotation = False
                    pressed = False

            self.draw(pos)
            # If button says "Start", i.e. player hadn't started yet or just ended the game,
            # the sound won't play
            if self.start_guess_btn.text == 'Guess':
                self.play_sound()

        pygame.quit()

    def draw(self, pos):
        """
        Animate the player, rotate the player, display the buttons
        :param pos: tuple
        :return: None
        """
        self.window.fill(self.bg)

        self.animate_player()
        self.rotate_player(pos)
        self.display_buttons(pos)
        self.window.blit(self.img, self.player_rect)
        pygame.display.update()

    def animate_player(self):
        """
        Animate the player
        :return: None
        """
        if int(self.animation_count) >= len(self.player_images):
            self.animation_count = 0
        self.img = self.player_images[int(self.animation_count)]
        self.animation_count += 0.5

    def rotate_player(self, pos):
        """
        Calculate rotation angle and rotate player towards mouse cursor
        :param pos: tuple
        :return: None
        """
        # Calculate the angle of player relative to mouse position
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

    def display_buttons(self, pos):
        """
        Display the buttons
        :return: None
        """
        for btn in self.buttons:
            btn.draw(self.window, self.outline_color)
            if btn.is_over(pos):
                btn.color = self.active_color
                btn.text_color = self.text_active_color
            else:
                btn.color = self.idle_color
                btn.text_color = self.text_idle_color

    def play_sound(self):
        """
        Make gaps between sounds played (in ticks)
        :return:
        """
        if self.sound_delay == 120:
            self.sound_source.play_hint(self.angle)
            self.sound_delay = 0

        self.sound_delay += 1
