import pygame
import sys
import math
import asyncio
import os
import random

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# --- COLORS ---
BLACK = (15, 15, 25)
WHITE = (240, 240, 240)
GATOR_GREEN = (46, 204, 113)
DARK_GREEN = (30, 130, 70)
WALL_GREY = (100, 100, 100)
FLOOR_BLUE = (50, 60, 80)
GOLD = (241, 196, 15)
RED = (231, 76, 60)
WOOD_BROWN = (139, 69, 19)
HEART_RED = (255, 50, 50)
TOUCH_BG = (50, 50, 50, 150) 
TOUCH_ACTIVE = (100, 100, 100, 180)

# --- MAPS ---
LEVEL_1_HALLWAY = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.H.............R..W",
    "W.P...WWWW...O.....W",
    "W.....W..W.........W",
    "W..H..W..W...E.....W",
    "WW.WWWW..WWWWWWWW..W",
    "W..........H.......W",
    "W...R......WW...H..W",
    "W..........WW......W",
    "W.H...E............W",
    "WWWWWWWWWWWWWWWWWWWW",
]

LEVEL_2_CLASSROOMS = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.....W.......H....W",
    "W.D.D.W.DD.DD.DDDD.W",
    "W.D.D.W.D...D.D..D.W",
    "W.DHD...D.H.D.D..D.W",
    "WW.W.WWWW.W.WWWW.WWW",
    "W..P......W........W",
    "W.WW.WWWW.WWWWWW.W.W",
    "W.W...E..........W.W",
    "W.H.......R......O.W",
    "WWWWWWWWWWWWWWWWWWWW",
]

LEVEL_3_CAFETERIA = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.O......E.........W",
    "W...DD.......DD....W",
    "W...DD...H...DD....W",
    "W..................W",
    "W.R......H.......R.W",
    "W..................W",
    "W...DD.......DD....W",
    "W...DD...H...DD....W",
    "W.P......E.........W",
    "WWWWWWWWWWWWWWWWWWWW",
]

LEVEL_4_CEREMONY = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W...O...H..H...O...W", 
    "W.WWWWWWW..WWWWWWW.W", 
    "W.........E........W", 
    "W..DDDHDD..DD.DDD..W", 
    "W..DDD.DD..DD.DDDH.W",
    "W.H......R.H.......W", 
    "W..DDD.DD..DDHDDD..W", 
    "W..DDD.DD..DD.DDDH.W",
    "W.P......E.........W", 
    "WWWWWWWWWWWWWWWWWWWW",
]

ALL_LEVELS = [LEVEL_1_HALLWAY, LEVEL_2_CLASSROOMS, LEVEL_3_CAFETERIA, LEVEL_4_CEREMONY]

class TouchController:
    def __init__(self):
        self.size = 65  
        gap = 15
        
        # --- FIXED COORDINATES ---
        # Screen height is 600. Map ends at 440.
        # Previous logic put buttons at y=645 (off screen).
        # New base_y (Top of UP button) = 350
        # This means:
        # UP:    350 -> 415 (Overlaps map slightly)
        # L/R:   430 -> 495 (In black bar)
        # DOWN:  510 -> 575 (In black bar, safe from bottom edge)
        
        base_y = 350 
        base_x = 30
        
        # D-PAD (Left Side)
        self.btn_up = pygame.Rect(base_x + self.size + gap, base_y, self.size, self.size)
        self.btn_left = pygame.Rect(base_x, base_y + self.size + gap, self.size, self.size)
        self.btn_right = pygame.Rect(base_x + self.size*2 + gap*2, base_y + self.size + gap, self.size, self.size)
        self.btn_down = pygame.Rect(base_x + self.size + gap, base_y + self.size*2 + gap*2, self.size, self.size)
        
        # ACTION BUTTONS (Right Side)
        # Align these with the "Left/Right" row (y=430) for better ergonomics
        action_y = 430
        
        # "RUN" button (Sprint)
        self.btn_sprint = pygame.Rect(SCREEN_WIDTH - 210, action_y, 80, 80)
        # "GO" button (Start/Action)
        self.btn_action = pygame.Rect(SCREEN_WIDTH - 110, action_y, 80, 80)
        
        self.font = pygame.font.SysFont('Arial', 24, bold=True) # Slightly larger arrows

    def get_active_buttons(self):
        active = set()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if mouse_pressed:
            if self.btn_up.collidepoint(mouse_pos): active.add('UP')
            if self.btn_down.collidepoint(mouse_pos): active.add('DOWN')
            if self.btn_left.collidepoint(mouse_pos): active.add('LEFT')
            if self.btn_right.collidepoint(mouse_pos): active.add('RIGHT')
            if self.btn_sprint.collidepoint(mouse_pos): active.add('SPRINT')
            if self.btn_action.collidepoint(mouse_pos): active.add('ACTION')
        return active

    def draw(self, screen):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        def draw_btn(rect, label, color=TOUCH_BG):
            pygame.draw.rect(s, color, rect, border_radius=15)
            pygame.draw.rect(s, WHITE, rect, width=2, border_radius=15)
            if label:
                text = self.font.render(label, True, WHITE)
                s.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

        # D-Pad
        draw_btn(self.btn_up, "▲")
        draw_btn(self.btn_down, "▼")
        draw_btn(self.btn_left, "◀")
        draw_btn(self.btn_right, "▶")
        
        # Action Buttons
        draw_btn(self.btn_sprint, "RUN", (200, 180, 50, 150)) # Yellowish
        draw_btn(self.btn_action, "GO", (50, 180, 100, 150)) # Greenish 
        
        screen.blit(s, (0,0))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Compass High: Ivan's Journey")
        self.clock = pygame.time.Clock()
        
        # Font Setup
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.big_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.title_font = pygame.font.SysFont('Arial', 70, bold=True)
        
        self.touch_controls = TouchController()
        self.assets = {}
        self.load_images()

        self.current_level_index = 0
        self.game_state = "START_MENU"
        self.lives = 3
        self.detentions = 0 
        self.start_ticks = 0
        self.final_time_str = "0:00"
        self.state_timer = 0
        
        self.walls, self.desks, self.goals = [], [], []
        self.homework_items, self.enemies = [], []
        self.player = None
        self.message = ""
        self.score = 0
        self.total_homework = 0

        self.move_timer = 0
        self.walk_delay = 150
        self.sprint_delay = 70
        self.confetti = []

    def load_images(self):
        files = {
            'player': 'player.png',
            'wall': 'wall.png',
            'floor': 'floor.png',
            'homework': 'homework.png',
            'enemy': 'enemy.png',
            'door': 'door.png',
            'desk': 'desk.png',
            'heart': 'heart.png',
            'compass': 'compass.png'
        }
        for name, filename in files.items():
            path = os.path.join("assets", filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    if name in ['heart', 'compass']: self.assets[name] = pygame.transform.scale(img, (25, 25))
                    else: self.assets[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                except: self.assets[name] = None
            else: self.assets[name] = None

    def create_confetti(self):
        self.confetti = []
        for _ in range(100):
            self.confetti.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'speed': random.randint(2, 6),
                'color': random.choice([GOLD, WHITE, GATOR_GREEN, RED]),
                'size': random.randint(5, 10),
                'type': random.choice(['rect', 'compass']) if self.assets['compass'] else 'rect'
            })

    def update_confetti(self):
        for p in self.confetti:
            p['y'] += p['speed']
            if p['y'] > SCREEN_HEIGHT:
                p['y'] = random.randint(-100, -10)
                p['x'] = random.randint(0, SCREEN_WIDTH)

    def get_time_string(self):
        if self.game_state == "PLAYING" or self.game_state == "LEVEL_COMPLETE":
            if self.start_ticks == 0: return "0:00"
            seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        else:
            return self.final_time_str
        m = seconds // 60
        s = seconds % 60
        return f"{m}:{s:02}"

    def load_level(self, level_idx):
        self.lives = 3
        current_map = ALL_LEVELS[level_idx]
        self.walls, self.desks, self.goals = [], [], []
        self.homework_items, self.enemies = [], []
        self.start_pos = (0, 0)
        self.score = 0
        self.total_homework = 0
        
        for r, row in enumerate(current_map):
            for c, tile in enumerate(row):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                if tile == 'W': self.walls.append(rect)
                elif tile == 'D': 
                    self.walls.append(rect)
                    self.desks.append(rect)
                elif tile == 'P': 
                    self.player = Player(x, y)
                    self.start_pos = (x, y)
                elif tile == 'O': self.goals.append(rect)
                elif tile == 'H': 
                    self.homework_items.append(pygame.Rect(x+10, y+10, 20, 20))
                    self.total_homework += 1
                elif tile == 'E': 
                    spd = random.choice([0.8, 1.0, 1.2, 1.5])
                    self.enemies.append(Enemy(x, y, 'vertical', spd))
                elif tile == 'R': 
                    spd = random.choice([0.8, 1.0, 1.2, 1.5])
                    self.enemies.append(Enemy(x, y, 'horizontal', spd))
        
        self.message = f"Homework Collected: 0/{self.total_homework}"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        touch_keys = self.touch_controls.get_active_buttons()
        current_time = pygame.time.get_ticks()
        
        is_action = keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or 'ACTION' in touch_keys
        
        is_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or 'SPRINT' in touch_keys
        is_left  = keys[pygame.K_LEFT] or 'LEFT' in touch_keys
        is_right = keys[pygame.K_RIGHT] or 'RIGHT' in touch_keys
        is_up    = keys[pygame.K_UP] or 'UP' in touch_keys
        is_down  = keys[pygame.K_DOWN] or 'DOWN' in touch_keys

        if self.game_state == "START_MENU":
            if is_action:
                self.game_state = "PLAYING"
                self.current_level_index = 0
                self.detentions = 0
                self.start_ticks = pygame.time.get_ticks()
                self.load_level(0)
            return

        if current_time - self.state_timer > 1000:
            if (self.game_state == "GAME_OVER" or self.game_state == "VICTORY") and is_action:
                self.game_state = "START_MENU"
                return
            if self.game_state == "LEVEL_COMPLETE" and is_action:
                self.game_state = "PLAYING"
                self.current_level_index += 1
                self.load_level(self.current_level_index)
                return

        if self.game_state != "PLAYING": return

        delay = self.sprint_delay if is_shift else self.walk_delay
        if current_time - self.move_timer > delay:
            dx, dy = 0, 0
            if is_left: dx = -TILE_SIZE
            elif is_right: dx = TILE_SIZE
            elif is_up: dy = -TILE_SIZE
            elif is_down: dy = TILE_SIZE
            if dx or dy:
                self.player.move(dx, dy, self.walls)
                self.move_timer = current_time

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.handle_input()
        
        if self.game_state == "PLAYING":
            for enemy in self.enemies: enemy.update(self.walls)
            self.check_interactions()
        
        if self.game_state == "VICTORY":
            self.update_confetti()

    def check_interactions(self):
        player_rect = self.player.rect
        for paper in self.homework_items[:]: 
            if player_rect.colliderect(paper):
                self.homework_items.remove(paper)
                self.score += 1
                self.message = f"Homework Collected: {self.score}/{self.total_homework}"
        
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.rect.inflate(-10, -10)):
                self.lives -= 1
                self.detentions += 1
                if self.lives > 0:
                    self.player.rect.topleft = self.start_pos
                    self.message = f"Caught! Chances: {self.lives}"
                else:
                    self.final_time_str = self.get_time_string()
                    self.game_state = "GAME_OVER"
                    self.state_timer = pygame.time.get_ticks()
        
        for goal in self.goals:
            if player_rect.colliderect(goal):
                if self.score == self.total_homework:
                    if self.current_level_index == len(ALL_LEVELS) - 1:
                        self.final_time_str = self.get_time_string()
                        self.game_state = "VICTORY"
                        self.create_confetti()
                        self.state_timer = pygame.time.get_ticks()
                    else:
                        self.game_state = "LEVEL_COMPLETE"
                        self.state_timer = pygame.time.get_ticks()
                else: 
                    self.message = f"Locked! Need {self.total_homework - self.score} more papers."

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == "START_MENU":
            # Simple grid background
            for x in range(0, SCREEN_WIDTH, TILE_SIZE*2):
                for y in range(0, SCREEN_HEIGHT, TILE_SIZE*2):
                    pygame.draw.rect(self.screen, (20, 20, 35), (x, y, TILE_SIZE, TILE_SIZE))

            t1 = self.title_font.render("COMPASS HIGH", True, GATOR_GREEN)
            t2 = self.big_font.render("Ivan's Journey", True, WHITE)
            alpha = (math.sin(pygame.time.get_ticks() / 300) + 1) * 127
            
            t3 = self.font.render("Press ENTER or Tap GO to Start", True, (255, 255, 255))
            t3.set_alpha(int(alpha))

            self.screen.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, 150))
            self.screen.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, 230))
            self.screen.blit(t3, (SCREEN_WIDTH//2 - t3.get_width()//2, 400))
            
            if self.assets['player']:
                big_ivan = pygame.transform.scale(self.assets['player'], (80, 80))
                self.screen.blit(big_ivan, (SCREEN_WIDTH//2 - 40, 300))
                
            self.touch_controls.draw(self.screen)
            pygame.display.flip()
            return

        if self.game_state in ["PLAYING", "LEVEL_COMPLETE"]:
            # Draw Map
            for r, row in enumerate(ALL_LEVELS[self.current_level_index]):
                for c, tile in enumerate(row):
                    x, y = c * TILE_SIZE, r * TILE_SIZE
                    if self.assets['floor']: self.screen.blit(self.assets['floor'], (x, y))
                    else: pygame.draw.rect(self.screen, FLOOR_BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                    
                    if tile == 'W': 
                        if self.assets['wall']: self.screen.blit(self.assets['wall'], (x, y))
                        else: pygame.draw.rect(self.screen, WALL_GREY, (x, y, TILE_SIZE, TILE_SIZE))
                    elif tile == 'D':
                        if self.assets['desk']: self.screen.blit(self.assets['desk'], (x, y))
                        else: pygame.draw.rect(self.screen, WOOD_BROWN, (x, y, TILE_SIZE, TILE_SIZE))
                    elif tile == 'O': 
                        if self.assets['door']: self.screen.blit(self.assets['door'], (x, y))
                        else: pygame.draw.rect(self.screen, (200, 50, 50), (x, y, TILE_SIZE, TILE_SIZE))
            
            # Draw Items & Entities
            for paper in self.homework_items:
                if self.assets['homework']: self.screen.blit(self.assets['homework'], paper)
                else: pygame.draw.rect(self.screen, WHITE, paper)
            
            for enemy in self.enemies:
                if self.assets['enemy']: self.screen.blit(self.assets['enemy'], enemy.rect)
                else: pygame.draw.rect(self.screen, RED, enemy.rect)
            
            if self.assets['player']: self.screen.blit(self.assets['player'], self.player.rect)
            else: pygame.draw.rect(self.screen, GATOR_GREEN, self.player.rect)
            
            # Draw Direction Arrow
            if self.homework_items:
                px, py = self.player.rect.center
                closest = min(self.homework_items, key=lambda i: math.hypot(i.centerx-px, i.centery-py))
                angle = math.atan2(closest.centery - py, closest.centerx - px)
                pygame.draw.line(self.screen, GOLD, (px, py), (px + math.cos(angle)*30, py + math.sin(angle)*30), 4)

            # --- HUD (TOP BAR) ---
            hud_bg = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
            hud_bg.fill((0, 0, 0, 180))
            self.screen.blit(hud_bg, (0,0))
            
            # Lives
            for i in range(self.lives):
                h_x = 10 + (i * 30)
                if self.assets['heart']: self.screen.blit(self.assets['heart'], (h_x, 8))
                else: pygame.draw.circle(self.screen, HEART_RED, (h_x + 10, 20), 8)

            # Center Message
            msg_text = self.font.render(self.message, True, WHITE)
            self.screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, 10))

            # Timer
            timer_text = self.font.render(f"Time: {self.get_time_string()}", True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 10, 10))

            self.touch_controls.draw(self.screen)

        if self.game_state == "LEVEL_COMPLETE":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0,0))
            t1 = self.big_font.render("LEVEL COMPLETE!", True, GOLD)
            t2 = self.font.render("Press ENTER or Tap GO to Continue", True, WHITE)
            self.screen.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, SCREEN_HEIGHT//2 + 10))
            self.touch_controls.draw(self.screen)
            
        if self.game_state == "GAME_OVER":
            self.screen.fill(BLACK) 
            t1 = self.big_font.render("SUMMER SCHOOL!", True, RED)
            stats = f"Time: {self.final_time_str} | Detentions: {self.detentions}"
            t2 = self.font.render(stats, True, WHITE)
            t3 = self.font.render("Press ENTER or Tap GO to Restart", True, (200, 200, 200))
            self.screen.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, SCREEN_HEIGHT//2 + 10))
            self.screen.blit(t3, (SCREEN_WIDTH//2 - t3.get_width()//2, SCREEN_HEIGHT//2 + 50))
            self.touch_controls.draw(self.screen)

        if self.game_state == "VICTORY":
            self.screen.fill(DARK_GREEN)
            for p in self.confetti:
                if p['type'] == 'compass' and self.assets['compass']:
                    scaled = pygame.transform.scale(self.assets['compass'], (p['size']*2, p['size']*2))
                    self.screen.blit(scaled, (p['x'], p['y']))
                else:
                    pygame.draw.rect(self.screen, p['color'], (p['x'], p['y'], p['size'], p['size']))
            
            t1 = self.title_font.render("YOU GRADUATED!", True, GOLD)
            t1_s = self.title_font.render("YOU GRADUATED!", True, BLACK)
            title_y = SCREEN_HEIGHT // 2 - 130
            self.screen.blit(t1_s, (SCREEN_WIDTH//2 - t1.get_width()//2 + 3, title_y + 3))
            self.screen.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, title_y))
            
            stats = f"Final Time: {self.final_time_str} | Detentions: {self.detentions}"
            t2 = self.font.render(stats, True, WHITE)
            t3 = self.font.render("Press ENTER or Tap GO to Return", True, (200, 200, 200))
            
            box_y = SCREEN_HEIGHT // 2
            pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH//2 - 200, box_y, 400, 80))
            pygame.draw.rect(self.screen, GOLD, (SCREEN_WIDTH//2 - 200, box_y, 400, 80), 3)
            
            self.screen.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, box_y + 20))
            self.screen.blit(t3, (SCREEN_WIDTH//2 - t3.get_width()//2, box_y + 50))
            self.touch_controls.draw(self.screen)
        
        pygame.display.flip()

    async def run(self):
        while True:
            self.update()
            self.draw()
            await asyncio.sleep(0)

class Player:
    def __init__(self, x, y): self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    def move(self, dx, dy, walls):
        self.rect.x += dx
        for w in walls: 
            if self.rect.colliderect(w): self.rect.x -= dx
        self.rect.y += dy
        for w in walls: 
            if self.rect.colliderect(w): self.rect.y -= dy

class Enemy:
    def __init__(self, x, y, d, speed=1.0):
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.dir = d
        self.spd = speed 
        self.md = 1 
    
    def update(self, walls):
        if self.dir == 'horizontal':
            self.x += self.spd * self.md
            self.rect.x = int(self.x)
            for w in walls:
                if self.rect.colliderect(w):
                    self.md *= -1
                    self.x += self.spd * self.md 
                    self.rect.x = int(self.x)
        else:
            self.y += self.spd * self.md
            self.rect.y = int(self.y)
            for w in walls:
                if self.rect.colliderect(w):
                    self.md *= -1
                    self.y += self.spd * self.md
                    self.rect.y = int(self.y)

if __name__ == "__main__":
    asyncio.run(Game().run())
