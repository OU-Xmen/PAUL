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
font = pygame.font.SysFont('comicsansms', 24)
main_menu = SourceFileLoader('main', 'main.py').load_module()

credits_list = [
    "P.A.U.L.",
    "Team Leader: Valerie Nielson",
    "Developers: Eli Sepulveda, Logan Pizzurro",
    "Matthew Robertson, Eshan Rajam",
    "Music: Eli Sepulveda, Matthew Robertson",
    "Testing Engineer: Freddie Warren",
    "",
    "Resources Used:",
    "Asteroids Tutorial Using Pygame and Python: ","https://youtu.be/XKMjMGbdrpY","",
    "Chat.openai.com:", "https://chat.openai.com/","",
    "Connect Four Python Game Tutorial with Pygame:","https://www.youtube.com/watch?v=XpYz-q1lxu8","",
    "Creating Tetris:","https://youtu.be/uoR4ilCWwKA","",
    "Make Pong With Python!:","https://www.youtube.com/watch?v=vVGTZlnnX3U","",
    "Pygame Tutorial - Creating Tetris.","https://www.youtube.com/watch?v=uoR4ilCWwKA","",
    "Python Hangman Tutorial #1 - Learn to Make Games with Pygame:","https://youtu.be/UEO1B_llDnc","",
    "Python Pygame Tutorial - Creating a Snake Game:","https://youtu.be/8dfePlONtls","",
    "A Simple Game Loop for Testing Pygame Code:","https://gist.github.com/MarquisLP/b534c95e4a11efaf376e.","",
    "Textwrap - Wiki:","https://www.pygame.org/wiki/TextWrap. ","",
]
#a work cited I guess sorry guys lol 

#“Asteroids Tutorial Using Pygame and Python.” YouTube, YouTube, https://youtube.com/playlist?list=PLxZI4CJBTZmBqhtbf2WioiBjUqSpGRlam. Accessed 15 Apr. 2023. 
# Chat.openai.com. https://chat.openai.com/. 
# “Connect Four Python Game Tutorial with Pygame.” YouTube, YouTube, 2 Nov. 2018, https://www.youtube.com/watch?v=XpYz-q1lxu8. Accessed 15 Apr. 2023. 
# “Creating Tetris.” YouTube, 23 Nov. 2018, https://youtu.be/uoR4ilCWwKA. Accessed 15 Apr. 2023. 
# “Make Pong With Python!” YouTube, YouTube, 15 Feb. 2022, https://www.youtube.com/watch?v=vVGTZlnnX3U. Accessed 15 Apr. 2023. 
# “Pygame Tutorial - Creating Tetris.” YouTube, YouTube, 23 Nov. 2018, https://www.youtube.com/watch?v=uoR4ilCWwKA. Accessed 15 Apr. 2023. 
# “Python Hangman Tutorial #1 - Learn to Make Games with Pygame.” YouTube, 21 June 2020, https://youtu.be/UEO1B_llDnc. Accessed 15 Apr. 2023. 
# “A Simple Game Loop for Testing Pygame Code.” Gist, https://gist.github.com/MarquisLP/b534c95e4a11efaf376e. 
# “Snake Game in Python | Snake Game Program Using Pygame | Edureka.” Edureka, 13 Dec. 2022, https://www.edureka.co/blog/snake-game-with-pygame/. Accessed 15 Apr. 2023. 
# “Textwrap - Wiki.” TextWrap - Pygame Wiki, https://www.pygame.org/wiki/TextWrap. 
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
