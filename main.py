import pygame
import sys
from mouse import Mouse
from intro import Intro

# Add at the top
class GameState:
    INTRO = 0
    MAIN_MENU = 1
    LOGIN = 2
    CHARACTERSELECT = 3
    CHARACTERCREATION = 4
    FREEROAM = 5
    JANKEN = 6
    DUEL = 7
    LOOT = 8
    SHOP = 9
    TRADE = 10
    DECKEDIT = 11
    SIDEDECK = 12
    REPLAY = 13

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Yu-Gi-Oh! ONLINE 2")
    
    # Set icon (replace 'icon.ico' with your actual file)
    try:
        icon = pygame.image.load('yo2.ico')
        pygame.display.set_icon(icon)
    except:
        pass  # Skip if icon fails to load
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    # Hide default cursor
    pygame.mouse.set_visible(False)
    mouse = Mouse(screen)
    intro = Intro(screen, 800, 600)
    current_state = GameState.INTRO
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Here needs to do some stuff
        screen.fill((0, 0, 0))  # Always black background
        if current_state == GameState.INTRO:
            if intro.current_state != 5:
                intro.update()
            elif intro.current_state == 5:
                current_state = GameState.MAIN_MENU
                intro = None  # Let garbage collector handle it
                print("Let garbage collector handle it (intro)")
        mouse.update()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()