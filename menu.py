import pygame
import os
from enum import Enum
# In your imports at the top (add this if not already there)
from background import MenuBackground  # Assuming you have this in a separate file
class MenuState(Enum):
    START = 0
    TITLE = 1
    ONLINE = 2
    OPTIONS = 3
    WEBSITE = 4
    DELETE = 5
    QUIT = 6
    SIGNIN = 7
    CHARACTER = 8
    CHARACTERCREATION_CLICK = 9
    LOADGAME = 10

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.current_state = MenuState.TITLE
        
        # Initialize background
        self.bg = MenuBackground(800, 600, screen)
        self.bg.running = True
        
         # Initialize audio
        self._init_audio()
        
        # Load and scale all assets
        self._load_and_scale_assets()
        self._setup_positions()
        
    def _load_and_scale_assets(self):
        """Load and properly scale all title screen assets"""
        try:
            # Scale factors for different elements
            button_scale = 0.65  # Buttons will be 70% of original size
            logo_scale = 0.75    # Main logo scale
            char_scale = 0.75    # Character scale (larger to go off-screen)
            small_logo_scale = 0.6  # Konami logo scale
            
            # Load and scale buttons (5 buttons)
            self.buttons = [
                self._load_scaled(r"export\data\title\title_botton_01_01_e.png", button_scale),
                self._load_scaled(r"export\data\title\title_botton_02_01_e.png", button_scale),
                self._load_scaled(r"export\data\title\title_botton_03_01_e.png", button_scale),
                self._load_scaled(r"export\data\title\title_botton_04_01_e.png", button_scale),
                self._load_scaled(r"export\data\title\title_botton_05_01_e.png", button_scale)
            ]
            
            # Center logo (scaled down)
            self.title_logo = self._load_scaled(r"export\data\title\title_title_01_e.png", logo_scale)
            
            # Konami small logo (scaled down more)
            self.konami_logo = self._load_scaled(r"export\data\title\title_konami_01.png", small_logo_scale)
            
            # Character images (scaled up to go off-screen)
            self.yugi = self._load_scaled(r"export\data\title\title_kyara_01.png", char_scale)
            self.yuki = self._load_scaled(r"export\data\title\title_kyara_02.png", char_scale)
            
            # Bottom copyright text
            self.copyright = self._load_scaled(r"export\data\title\title_copy_01_e.png", 0.7)
            
        except Exception as e:
            print(f"Error loading menu assets: {e}")
            self._create_fallback_assets()
    
    def _init_audio(self):
        """Initialize background music"""
        try:
            pygame.mixer.init()
            self.bg_music = pygame.mixer.Sound(r"export\sound\bgm\y_gx_01.wav")
            self.bg_music.set_volume(0.8)  # 50% volume
            self.bg_music.play(loops=-1)  # Loop indefinitely
        except Exception as e:
            print(f"Error loading background music: {e}")
            # Create silent fallback
            self.bg_music = pygame.mixer.Sound(buffer=bytearray(44))

    # ... [rest of your existing Menu class methods] ...

    def cleanup(self):
        """Clean up resources"""
        self.bg_music.stop()  # Stop music when menu closes
    
    def _load_scaled(self, path, scale_factor):
        """Load an image and scale it by the given factor"""
        img = pygame.image.load(path).convert_alpha()
        original_size = img.get_size()
        new_size = (int(original_size[0] * scale_factor), 
                    int(original_size[1] * scale_factor))
        return pygame.transform.smoothscale(img, new_size)
    
    def _create_fallback_assets(self):
        """Create placeholder assets if loading fails"""
        # Create a simple button
        button = pygame.Surface((150, 40), pygame.SRCALPHA)
        pygame.draw.rect(button, (100, 100, 255), (0, 0, 150, 40), border_radius=5)
        
        self.buttons = [button.copy() for _ in range(5)]
        self.title_logo = pygame.Surface((300, 80), pygame.SRCALPHA)
        self.konami_logo = pygame.Surface((80, 25), pygame.SRCALPHA)
        self.yugi = pygame.Surface((200, 400), pygame.SRCALPHA)  # Larger for off-screen effect
        self.yuki = pygame.Surface((200, 400), pygame.SRCALPHA)  # Larger for off-screen effect
        self.copyright = pygame.Surface((200, 15), pygame.SRCALPHA)
    
    def _setup_positions(self):
        """Calculate all screen positions for the elements"""
        # Title logo - top center (drawn above everything else)
        self.logo_pos = (
            (self.screen_width - self.title_logo.get_width()) // 2,
            30  # 30px from top
        )
        
        # Konami logo - top left
        self.konami_pos = (10, 10)
        
        # Characters - partially off-screen at bottom
        # Yugi (left side) - 30% off left edge
        self.yugi_pos = (
            -int(self.yugi.get_width() * 0.2),  # 30% off left side
            self.screen_height - self.yugi.get_height() + 0  # Slightly above bottom
        )
        
        # Yuki (right side) - 30% off right edge
        self.yuki_pos = (
            self.screen_width - int(self.yuki.get_width() * 0.65),  # 30% off right side
            self.screen_height - self.yuki.get_height() + 0  # Slightly above bottom
        )
        
        # Buttons - stacked vertically with no spacing
        self.button_positions = []
        total_buttons_height = sum(btn.get_height() for btn in self.buttons)
        start_y = self.screen_height - total_buttons_height - 85  # 50px from bottom
        
        current_y = start_y
        for button in self.buttons:
            x = (self.screen_width - button.get_width()) // 2
            self.button_positions.append((x, current_y))
            current_y += button.get_height()  # No extra spacing
        
        # Copyright text - bottom center (below buttons)
        self.copyright_pos = (
            (self.screen_width - self.copyright.get_width()) // 2,
            self.screen_height - self.copyright.get_height() - 10  # 10px from bottom
        )
    
    def draw_title_screen(self):
        """Draw all title screen elements in correct order"""
        # Dark blue background
        self.screen.fill((20, 20, 50))  
        
        # Draw background first
        self.bg.draw(self.screen)
        
        # Draw characters first (bottom layer)
        self.screen.blit(self.yugi, self.yugi_pos)
        self.screen.blit(self.yuki, self.yuki_pos)
        
        # Draw buttons next (middle layer)
        for button, pos in zip(self.buttons, self.button_positions):
            self.screen.blit(button, pos)
        
        # Draw title logo last (top layer - above everything)
        self.screen.blit(self.title_logo, self.logo_pos)
        
        # Draw Konami logo (top left)
        self.screen.blit(self.konami_logo, self.konami_pos)
        
        # Draw copyright (very bottom)
        self.screen.blit(self.copyright, self.copyright_pos)
    
    def update(self):
        """Update menu state"""
        self.bg.update()  # Update background animation
        
        if self.current_state == MenuState.TITLE:
            self.draw_title_screen()
    
    def handle_event(self, event):
        """Handle user input"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            for i, (button, pos) in enumerate(zip(self.buttons, self.button_positions)):
                button_rect = pygame.Rect(pos, button.get_size())
                if button_rect.collidepoint(mouse_pos):
                    return self._handle_button_click(i)
        return None
    
    def _handle_button_click(self, button_index):
        """Handle button click actions"""
        button_actions = [
            MenuState.ONLINE,       # Button 1 - Start Game
            MenuState.OPTIONS,      # Button 2 - Online
            MenuState.WEBSITE,     # Button 3 - Options
            MenuState.DELETE,   # Button 4 - Character
            MenuState.QUIT         # Button 5 - Quit
        ]
        return button_actions[button_index] if button_index < len(button_actions) else None


# Test function
def test_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Yu-Gi-Oh! Menu Test")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            result = menu.handle_event(event)
            if result == MenuState.QUIT:
                running = False
            elif result is not None:
                print(f"Transitioning to: {result}")
        screen.fill((0, 0, 0))  # Always black background
        menu.update()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_menu()