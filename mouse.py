import pygame
import os
import math

class Mouse:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.mouse_buttons = []
        self.click_animations = [] # Stores active animations
        self.is_clicking = False
        # Load cursor images (normal/clicked states)
        self.cursor_normal = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n01_c01.png")).convert_alpha()
        self.cursor_clicked = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n02_c01.png")).convert_alpha()
        self.cursor_normal_shadow = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n01_s.png")).convert_alpha()
        self.cursor_clicked_shadow = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n02_s.png")).convert_alpha()
    
    def load_assets(self):
        # Load cursor images (normal/clicked states)
        self.cursor_normal = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n01_c01.png")).convert_alpha()
        self.cursor_clicked = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n02_c01.png")).convert_alpha()
        self.cursor_normal_shadow = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n01_s.png")).convert_alpha()
        self.cursor_clicked_shadow = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_n02_s.png")).convert_alpha()
    
    def draw(self):
        self.screen.blit(self.current_cursor_shadow,(self.x - self.cursor_normal_shadow.get_width() // 2,self.y - self.cursor_normal_shadow.get_height() // 2))
        self.screen.blit(self.current_cursor,(self.x - self.cursor_normal.get_width() // 2,self.y - self.cursor_normal.get_height() // 2))
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        if self.mouse_buttons[0]:
            # Start a new animation at click position
            if self.is_clicking == False:
                self.click_animations.append(ClickAnimation(self.x,self.y))
                self.is_clicking = True
        else:
            self.is_clicking = False
        # Update and draw active click animations
        for anim in self.click_animations[:]:  # Iterate over a copy to allow removal
            if anim.update():
                anim.draw(self.screen)
            else:
                self.click_animations.remove(anim)
        # Draw current cursor (normal or clicked state)
        self.current_cursor = self.cursor_clicked if self.is_clicking else self.cursor_normal
        self.current_cursor_shadow = self.cursor_clicked_shadow if self.is_clicking else self.cursor_normal_shadow
        self.draw()

class ClickAnimation:
    def __init__(self, x, y):
        self.x = x - 16
        self.y = y - 16
        self.start_time = pygame.time.get_ticks()
        # Load click animation frames (assuming mausuk_e01_c01.png is the base frame)
        self.base_img = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_e01_c01.png")).convert_alpha() 
        self.animation_duration = 750 # 1 second (in ms)
        self.initial_scale = 0.1 # Starts at 50% size
        self.final_scale = 2.0 # Grows to 200% size
        
    def load_assets(self):
        # Load click animation frames (assuming mausuk_e01_c01.png is the base frame)
        self.click_animation_img = pygame.image.load(os.path.join("export", "data", "common", "m_cursor", "mausuk_e01_c01.png")).convert_alpha()

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.animation_duration, 1.0)  # 0.0 to 1.0
        
        # Scale from INITIAL_SCALE to FINAL_SCALE
        self.current_scale = self.initial_scale + (self.final_scale - self.initial_scale) * progress
        
        # Alpha from 255 to 0
        self.alpha = int(255 * (1.0 - progress))
        
        return progress < 1.0  # True = still active
    
    def draw(self, surface):
        # Create scaled surface
        width = int(self.base_img.get_width() * self.current_scale)
        height = int(self.base_img.get_height() * self.current_scale)
        scaled_img = pygame.transform.scale(self.base_img, (width, height))
        
        # Apply alpha
        if self.alpha < 255:  # Only needed if alpha changed
            scaled_img.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Draw centered at position
        surface.blit(scaled_img, (self.x - width//2, self.y - height//2))
        