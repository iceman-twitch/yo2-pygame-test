import pygame
import sys

# State machine
class IntroState:
    START = 0
    FADE_IN = 1
    HOLD = 2
    FADE_OUT = 3
    PAUSE = 4
    END = 5

class Intro:
    def __init__(self, screen, width, height):
        self.screen = screen
        # Animation settings (all times in milliseconds)
        self.ANIMATION_TIMINGS = {
            "start": 3000,   # 1.5 seconds
            "fade_in": 1500,   # 1.5 seconds
            "hold": 2000,      # 2 seconds
            "fade_out": 1500,  # 1.5 seconds
            "pause": 5000      # 5 seconds black screen
        }
        self.original_logo = pygame.image.load(r"export\data\logo\konami_logo_0_j.png").convert_alpha()
        self.logo = pygame.transform.scale(self.original_logo, (width, height))  # Force fullscreen stretch
        self.current_state = IntroState.START
        self.state_start_time = 0
        self.alpha = 0  # Current opacity (0-255)
        
    def draw(self):
        if self.current_state != IntroState.PAUSE:
            # Apply current alpha to logo
            self.logo_copy = self.logo.copy()
            self.logo_copy.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(self.logo_copy, (0, 0))
    
    def update(self):
        self.current_time = pygame.time.get_ticks()
        
        # State management
        if self.current_state == IntroState.START:
            if self.state_start_time == 0:
                self.state_start_time = self.current_time
            
            progress = min(1.0, (self.current_time - self.state_start_time) / self.ANIMATION_TIMINGS["start"])
            
            if progress >= 1.0:
                self.current_state = IntroState.FADE_IN
                self.state_start_time = self.current_time
        if self.current_state == IntroState.FADE_IN:
            if self.state_start_time == 0:
                self.state_start_time = self.current_time
            
            progress = min(1.0, (self.current_time - self.state_start_time) / self.ANIMATION_TIMINGS["fade_in"])
            self.alpha = int(255 * progress)
            
            if progress >= 1.0:
                self.current_state = IntroState.HOLD
                self.state_start_time = self.current_time
        
        elif self.current_state == IntroState.HOLD:
            self.alpha = 255
            if self.current_time - self.state_start_time >= self.ANIMATION_TIMINGS["hold"]:
                self.current_state = IntroState.FADE_OUT
                self.state_start_time = self.current_time
        
        elif self.current_state == IntroState.FADE_OUT:
            progress = min(1.0, (self.current_time - self.state_start_time) / self.ANIMATION_TIMINGS["fade_out"])
            self.alpha = int(255 * (1 - progress))
            
            if progress >= 1.0:
                self.current_state = IntroState.PAUSE
                self.state_start_time = self.current_time
        
        elif self.current_state == IntroState.PAUSE:
            self.alpha = 0
            if self.current_time - self.state_start_time >= self.ANIMATION_TIMINGS["pause"]:
                self.current_state = IntroState.END # This will end it
                self.state_start_time = 0  # Reset for new cycle
        
        # Drawing
        self.draw()
"""
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Yu-Gi-Oh! Online 2 - Intro (Looped)")

# Load and stretch logo to 800x600
try:
    original_logo = pygame.image.load(r"export\data\logo\konami_logo_0_j.png").convert_alpha()
    logo = pygame.transform.scale(original_logo, (800, 600))  # Force fullscreen stretch
except Exception as e:
    print(f"Error loading logo: {e}")
    pygame.quit()
    sys.exit()

# Animation settings (all times in milliseconds)
ANIMATION_TIMINGS = {
    "fade_in": 1500,   # 1.5 seconds
    "hold": 2000,      # 2 seconds
    "fade_out": 1500,  # 1.5 seconds
    "pause": 5000      # 5 seconds black screen
}

current_state = IntroState.FADE_IN
state_start_time = 0
alpha = 0  # Current opacity (0-255)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # State management
    if current_state == IntroState.FADE_IN:
        if state_start_time == 0:
            state_start_time = current_time
        
        progress = min(1.0, (current_time - state_start_time) / ANIMATION_TIMINGS["fade_in"])
        alpha = int(255 * progress)
        
        if progress >= 1.0:
            current_state = IntroState.HOLD
            state_start_time = current_time
    
    elif current_state == IntroState.HOLD:
        alpha = 255
        if current_time - state_start_time >= ANIMATION_TIMINGS["hold"]:
            current_state = IntroState.FADE_OUT
            state_start_time = current_time
    
    elif current_state == IntroState.FADE_OUT:
        progress = min(1.0, (current_time - state_start_time) / ANIMATION_TIMINGS["fade_out"])
        alpha = int(255 * (1 - progress))
        
        if progress >= 1.0:
            current_state = IntroState.PAUSE
            state_start_time = current_time
    
    elif current_state == IntroState.PAUSE:
        alpha = 0
        if current_time - state_start_time >= ANIMATION_TIMINGS["pause"]:
            current_state = IntroState.FADE_IN
            state_start_time = 0  # Reset for new cycle
    
    # Drawing
    screen.fill((0, 0, 0))  # Always black background
    
    if current_state != IntroState.PAUSE:
        # Apply current alpha to logo
        logo_copy = logo.copy()
        logo_copy.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(logo_copy, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
"""