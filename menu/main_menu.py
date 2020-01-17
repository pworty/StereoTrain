import pygame

from menu.button import Button


class MainMenu(Button):
    def __init__(self, color, x, y, width, height, text='', text_color=(0, 0, 0)):
        super().__init__(color, x, y, width, height, text, text_color)
        self.bg = pygame.Color("black")
        self.idle_color = (0, 0, 0)
        self.active_color = (255, 255, 255)
        self.outline_color = (255, 255, 255)
        self.text_idle_color = (255, 255, 255)
        self.text_active_color = (0, 0, 0)
        self.main_menu_btn = Button(self.idle_color, 672, 390, 256, 120, 'StereoTrain',
                                    self.text_idle_color)

    def main_menu(self, window):
        run = True
        clock = pygame.time.Clock()
        fps = 60
        pos = (0, 0)
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    if self.main_menu_btn.is_over(pos):
                        run = False

            window.fill(self.bg)
            self.main_menu_btn.draw(window, self.outline_color)
            if self.main_menu_btn.is_over(pos):
                self.main_menu_btn.color = self.active_color
                self.main_menu_btn.text_color = self.text_active_color
            else:
                self.main_menu_btn.color = self.idle_color
                self.main_menu_btn.text_color = self.text_idle_color
            pygame.display.update()
