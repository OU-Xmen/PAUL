import pygame
import sys
from importlib.machinery import SourceFileLoader

pygame.init()

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 24
SPEED = 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Credits")
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 30)
main_menu = SourceFileLoader('main', 'main.py').load_module()

credits_list = [
    "P.A.U.L.",
    "Team Leader: Valerie Nielson",
    "Developers: Eli Sepulveda, Logan Pizzurro",
    "Matthew Robertson, Eshan Rajam",
    "Music: Eli Sepulveda, Matthew Robertson",
    "Testing Engineer: Freddie Warren",
    "[Other stuff to credit here]",
    "",
    "Resources Used:",
    "link",
    "link",
]

def scroll_credits():
                
    text_height = len(credits_list) * (FONT_SIZE + 10)
    scroll_y = SCREEN_HEIGHT

    while scroll_y > -text_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.main(False)
                    quit()
        screen.fill(BACKGROUND_COLOR)

        for i, line in enumerate(credits_list):
            rendered_text = font.render(line, True, FONT_COLOR)
            text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, scroll_y + i * (FONT_SIZE + 10)))
            screen.blit(rendered_text, text_rect)

        scroll_y -= SPEED
        pygame.display.flip()
        clock.tick(60)

    return False  # Return False when the credits are no longer visible


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not scroll_credits():  # Break the loop and quit when the credits are done
            break

    main_menu.main(False)

if __name__ == "__main__":
    main()
