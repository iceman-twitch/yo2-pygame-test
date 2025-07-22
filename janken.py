import pygame
import sys
import os
import random
from pygame.transform import scale, rotate


class Card:
    def __init__(self, x, y, image, is_player=False, position = 1):
        self.x = x
        self.y = y
        self.image = image
        self.is_player = is_player
        self.hovered = False
        self.speed = 10
        self.arrived = True
        self.rotation = 180 if not is_player else 0
        self.selected = False
        self.returning = False
        self.duel = False
        self.selecting = False
        self.hidden = True
        self.original_x = x
        self.original_y = y
        self.card_size_x = 120
        self.card_size_y = 180
        self.position = position # 1 - left, 2 - middle, 3 - right
        self.target_x = x # Will be set when card needs to move
        self.target_y = y # Will be set when card needs to move
        
    def draw(self):
        a = 0
        
    def select(self):
        a = 0
        
    def duel(self):
        a = 0
        
    def update(self):
        if (not self.arrived or self.selecting) and not self.hidden: # Only update if not arrived and not hidden
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance > self.speed: # Move towards target
                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed
            else: # Arrived at target
                self.x = self.target_x
                self.y = self.target_y
                self.arrived = True
        # Adjust position for hover effect
        if self.is_player and self.selecting:
            if self.hovered:
                self.y = self.target_y - 20 if self.hovered else self.target_y
            else:
                self.y = self.target_y  # Return to original position
            
    def check_hover(self, mouse_pos):
        # Check if the mouse is over the card
        card_rect = self.image.get_rect(topleft=(self.x, self.y))
        
        self.hovered = (
            self.x <= mouse_pos[0] <= self.x + self.card_size_x and
            self.y <= mouse_pos[1] <= self.y + self.card_size_y
        )
        
    def set_target(self, tx, ty):
        if self.arrived:
            self.target_x = tx
            self.target_y = ty
            self.arrived = False # Reset arrived flag when new target is set
            self.hidden = False # Make card visible when it starts moving
            
    def reset(self):
        # Resets card to its initial hidden state at center
        self.x = self.original_x
        self.y = self.original_y
        self.hidden = True
        self.arrived = False
        self.selected = False
        self.returning = False
        self.hovered = False
        
    def draw(self, surface):
        img = rotate(self.image, self.rotation) if self.rotation != 0 else self.image
        surface.blit(img, (self.x, self.y))
        

class Janken:
    def __init__(self, screen):
        self.screen = screen  
        self.screen_size = screen.get_size()
        self.mouse_buttons = []
        # Initialize fade properties
        self.fade_surface = pygame.Surface(screen.get_size())
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha = 255
        self.fade_speed = 5
        self.fade_direction = -1  # Start with fade-in    
        # Game state
        self.game_phase = "fadein"
        self.wait_time = 1000  # 1 second in milliseconds
        self.start_time = None
        self.waiting = False
        self.selected_card = None
        self.player_cards = []
        self.enemy_cards = []   
        # Background animation properties
        self.layer1_pos = 0
        self.layer1_speed = 1.5
        self.layer2_pos = 0
        self.layer2_speed = 2.5
        
    # Load assets
    def load_assets(self):
        self.assets = {
            'bg': None,
            'card_back': None,
            'card_rock': None,
            'card_paper': None,
            'card_scissors': None,
            'bg_music': None
        }
        
        try:
            bg = pygame.image.load(r"export\data\y\janken\jan_bg_01.png").convert()
            self.assets['bg'] = scale(bg, self.screen_size)
            bglayer1 = pygame.image.load(r"export\data\y\janken\jan_bg_02.png").convert_alpha()
            self.assets['bglayer1'] = scale(bglayer1, self.screen_size)
            bglayer2 = pygame.image.load(r"export\data\y\janken\jan_bg_03.png").convert_alpha()
            self.assets['bglayer2'] = scale(bglayer2, self.screen_size)
            card_back = pygame.image.load(r"export\data\y\janken\0000.png").convert_alpha()
            self.assets['card_back'] = scale(card_back, self.card_size)
            card_rock = pygame.image.load(r"export\data\y\janken\jan_card_01.png").convert_alpha()
            self.assets['card_rock'] = scale(card_rock, self.card_size)
            card_paper = pygame.image.load(r"export\data\y\janken\jan_card_03.png").convert_alpha()
            self.assets['card_paper'] = scale(card_paper, self.card_size)
            card_scissors = pygame.image.load(r"export\data\y\janken\jan_card_02.png").convert_alpha()
            self.assets['card_scissors'] = scale(card_scissors, self.card_size)            
            self.assets['bg_music'] = pygame.mixer.Sound(r"export\sound\bgm\y_gx_17.wav")
            
        except Exception as e:
            print(f"Asset loading error: {e}")
            self.assets['bg'] = pygame.Surface(self.screen_size)
            self.assets['bg'].fill((50, 50, 100))
            
            fallback_card = pygame.Surface(self.card_size, pygame.SRCALPHA)
            pygame.draw.rect(fallback_card, (200, 200, 200), fallback_card.get_rect(), 2)
            for card_type in ['card_back', 'card_rock', 'card_paper', 'card_scissors']:
                self.assets[card_type] = fallback_card.copy()
            
            self.assets['bg_music'] = pygame.mixer.Sound(buffer=bytearray(44))
        
        return self.assets
    
    def phase(self):
        a = 0
    
    def update_fade(self):
        if self.game_phase in ["fadein", "fadeout"]:
            self.fade_alpha += self.fade_speed * self.fade_direction
            
            if self.fade_alpha <= 0:  # Fade-in complete
                self.fade_alpha = 0
                if self.game_phase == "fadein":
                    self.game_phase = "waiting"
                    self.start_time = pygame.time.get_ticks()
                    
            elif self.fade_alpha >= 255:  # Fade-out complete
                self.fade_alpha = 255
                if self.game_phase == "fadeout":
                    # Transition to whatever comes after fadeout
                    self.game_phase = "loading"  
                    # Reset for potential future fades
                    self.fade_direction = -1  
    
    def draw_fade(self):
        if self.game_phase in ["fadein", "fadeout"]:
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))
    
    def start_fadeout(self):
        """Call this when you want to start fading to black"""
        self.game_phase = "fadeout"
        self.fade_direction = 1  # Fading out
        self.fade_alpha = 0  # Start from fully visible
    
    # Update moving layers
    def background_anim(self):
        self.layer1_pos += self.layer1_speed
        self.layer2_pos += self.layer2_speed
        if self.layer1_pos >= 600:
            self.layer1_pos = 0
        if self.layer2_pos >= 600:
            self.layer2_pos = 0
            
    def draw_background(self):
        self.screen.blit(self.assets['bg'], (0, 0))
        # Draw moving layers
        self.screen.blit(self.assets['bglayer1'], (0, self.layer1_pos))
        self.screen.blit(self.assets['bglayer1'], (0, self.layer1_pos - 600))
        self.screen.blit(self.assets['bglayer2'], (0, self.layer2_pos))
        self.screen.blit(self.assets['bglayer2'], (0, self.layer2_pos - 600))
    
    def create_cards(self):
        self.enemy_cards = [
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_back'], False, 1),
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_back'], False, 2),
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_back'], False, 3)
        ]
        self.player_cards = [
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_rock'], True, 1),
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_paper'], True, 2),
            Card(self.center_pos[0], self.center_pos[1], self.assets['card_scissors'], True, 3)
        ]
    def draw_all_cards(self):
        for card in self.player_cards:
            if card.selected == False:
                card.draw(self.screen)
        for card in self.player_cards:
            if card.selected:
                card.draw(self.screen)
        for card in self.enemy_cards:
            card.draw(self.screen)
    
    def start_duel(self):
        if self.game_phase == "selecting":
            for card in self.player_cards:
                card.selecting = False
            self.game_phase = "dueling"
    
    def update_card_select(self):
        for card in self.player_cards:
            if card.selecting == True:
                if card.hovered:
                    card.selected = True
                    self.start_duel()
                    
    def update_all_cards(self):
        if self.game_phase == "drawing":
            for card in self.player_cards:
                if self.enemy_cards[2].y == -60 and self.enemy_cards[2].position == 3:
                    if self.player_cards[0].y != 480 and self.player_cards[0].position == 1:
                        self.player_cards[0].set_target(self.player_cards[0].x-150, 480)
                if self.player_cards[0].y == 480:
                    if self.player_cards[1].y != 480:
                        self.player_cards[1].set_target(self.player_cards[1].x, 480)
                if self.player_cards[1].y == 480:
                    if self.player_cards[2].y != 480:
                        self.player_cards[2].set_target(self.player_cards[2].x+150, 480)
                if self.player_cards[2].y == 480:
                    if self.game_phase == "drawing":
                            self.game_phase = "selecting"
                card.update()
            for card in self.enemy_cards:
                if self.enemy_cards[0].y != -60 and self.enemy_cards[0].position == 1:
                    self.enemy_cards[0].set_target(self.enemy_cards[1].x-150, -60)
                if self.enemy_cards[0].y == -60 and self.enemy_cards[0].position == 1:
                    if self.enemy_cards[1].y != -60 and self.enemy_cards[1].position == 2:
                        self.enemy_cards[1].set_target(self.enemy_cards[1].x, -60)
                if self.enemy_cards[1].y == -60 and self.enemy_cards[1].position == 2:
                    if self.enemy_cards[2].y != -60 and self.enemy_cards[2].position == 3:
                        self.enemy_cards[2].set_target(self.enemy_cards[1].x+150, -60)
                card.update()
        if self.game_phase == "selecting":
            for card in self.player_cards:
                if card.selecting != True:
                    card.selecting = True
                card.check_hover(self.mouse_pos)
                card.update()
        # After select player and enemy face against each other
        if self.game_phase == "dueling":
            for card in self.player_cards:
                card.set_target(self.player_cards[1].x, 480)
                card.update()
            for card in self.enemy_cards:
                card.update()                
                
    def draw_center_card(self):
        # Draw the centered card
        self.screen.blit(self.assets['card_back'], self.center_pos)
        
    def draw(self):
        # Update moving layers
        self.background_anim()
        
        # Drawing Background
        self.draw_background()
        if self.game_phase == "waiting":
            self.draw_center_card()
            if self.start_time == None:
                self.start_time = pygame.time.get_ticks()  # Record the start time
                self.waiting = True
        if self.game_phase == "drawing":
            if self.player_cards == []:
                self.create_cards()
            if self.player_cards != []:
                self.draw_all_cards()
        if self.game_phase == "selecting":
            if self.player_cards != []:
                self.draw_all_cards()
        if self.game_phase == "dueling":
            if self.player_cards != []:
                self.draw_all_cards()
        
        # Always draw fade overlay if active
        self.draw_fade()
                
    def reset_waiting(self):
        self.wait_time = 1000  # 1 second in milliseconds
        self.start_time = None
        self.waiting = False 
        
    def wait(self):
        # Check if we are waiting
        if self.game_phase == "waiting":
            # Check if the wait time has passed
            if pygame.time.get_ticks() - self.start_time >= self.wait_time:
                self.reset_waiting()  # Stop waiting
                self.game_phase = "drawing"
    
    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
        # Left mouse button
        if self.mouse_buttons[0]:
            self.update_card_select()
        # Handle fade transitions first
        self.update_fade()
        # Handle drawings
        self.draw()
        # Handle cards update
        self.update_all_cards()
        self.wait()
        
def test():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Yu-Gi-Oh! ONLINE 2 (Janken)")
    icon = pygame.image.load("yo2.ico")  # or "icon.ico" (Windows prefers .ico)
    pygame.display.set_icon(icon)
    janken = Janken(screen)
    
    # Constants
    janken.screen_size = (800, 600)
    janken.card_size = (120, 180)
    janken.center_pos = (400 - janken.card_size[0]//2, 300 - janken.card_size[1]//2)
    
    janken.load_assets()
    janken.assets['bg_music'].play(loops=-1)
    janken.assets['bg_music'].set_volume(0.5)
    
    # Game state
    clock = pygame.time.Clock()
    running = True
    janken.phase_start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Drawing
        janken.screen.fill((0, 0, 0))  # Always black background
        janken.update()
        pygame.display.flip()
        clock.tick(60)
    # Cleanup
    janken.assets['bg_music'].fadeout(500)
    pygame.quit()
    sys.exit()
    
test()