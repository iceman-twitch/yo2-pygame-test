import pygame
import sys
from pygame.transform import scale, rotate

class MenuBackground:
    def __init__(self, screen_width, screen_height, screen ):
        """Initialize the background animation system"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_size = screen.get_size()
        # Load and scale images
        self.background = scale(pygame.image.load(r"export\data\menu\abmake_bg_01.png").convert(), self.screen_size)
        self.animation = scale(pygame.image.load(r"export\data\menu\abmake_bg_02.png").convert_alpha(), self.screen_size)
        self.animation2 = scale(pygame.image.load(r"export\data\menu\menu_bg_01.png").convert_alpha(), self.screen_size)
        
        # Animation control
        self.scroll_offset = 0
        self.scroll_speed = 1
        self.running = False
    
    def _load_image(self, path, convert=False, convert_alpha=False):
        """Helper method to load and scale images"""
        try:
            img = pygame.image.load(path)
            if convert:
                img = img.convert()
            if convert_alpha:
                img = img.convert_alpha()
            return pygame.transform.scale(img, (self.screen_width, self.screen_height))
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Create fallback surface
            surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            surface.fill((50, 50, 100))  # Dark blue fallback
            return surface
    
    def update(self):
        """Update animation position"""
        self.scroll_offset += self.scroll_speed
        if self.scroll_offset >= self.screen_height:
            self.scroll_offset = 0
    
    def draw(self, screen):
        """Draw the background elements"""
        # Static background
        screen.blit(self.background, (0, 0))
        
        # Animated layer (two copies for seamless looping)
        screen.blit(self.animation, (0, self.scroll_offset - self.screen_height))
        screen.blit(self.animation, (0, self.scroll_offset))
        # screen.blit(self.animation2, (0, self.scroll_offset - self.screen_height))
        # screen.blit(self.animation2, (0, self.scroll_offset))
    
def run_test():
    """Test method to run the animation standalone"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Background Animation Test")
    clock = pygame.time.Clock()
    bg = MenuBackground(800, 600, screen)
    bg.running = True
    while bg.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bg.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bg.running = False
        
        bg.update()
        screen.fill((0, 0, 0))  # Clear screen
        bg.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


# Example usage:
if __name__ == "__main__":
    run_test()