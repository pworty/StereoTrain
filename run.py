import pygame
import os

from game import Game


def main(restart):
    pygame.init()
    pygame.display.set_caption('Score: 0')
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    g = Game(restart)
    if restart:
        g.start_guess_btn.text = 'Guess'
    if g.run():
        main(True)
    pygame.quit()


if __name__ == "__main__":
    main(False)
