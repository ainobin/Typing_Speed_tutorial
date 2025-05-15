# it's ready with previous code 

import pygame, random, copy, sys
import os
import math
from pygame import mixer  # For sound effects

pygame.init()
mixer.init()  # Initialize the mixer for sound effects

# Set the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# from file
with open(os.path.join(current_dir, "Wordlist/10k_words.txt"), 'r') as file:
    wordlist = file.readlines()
wordlist = [word.strip() for word in wordlist]
final_name = ""
name = ""
len_indexes = []
length = 0
wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

# Constants and settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Speed Typing Adventure")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
level = 1
live = 3
user_input = ""
score = 0
speed = 1.5
paused = False
game_over = False  # New variable to track game over state
submit = ''
score_multiplier = 1
power_timers = {}
power_up_messages = []
power_ups = []
selected_level = "fair"  # Default level - "junior" or "fair"

# Game themes - each with different color schemes
THEMES = {
    "classic": {
        "background": (100, 149, 237),  # Cornflower blue
        "text": (0, 0, 0),
        "highlight": (0, 255, 0),
        "input_bg": (32, 42, 68),
        "border": (255, 255, 255)
    },
    "dark": {
        "background": (40, 44, 52),
        "text": (255, 255, 255),
        "highlight": (97, 175, 239),
        "input_bg": (30, 30, 30),
        "border": (86, 86, 86)
    },
    "nature": {
        "background": (76, 175, 80),
        "text": (33, 33, 33),
        "highlight": (255, 235, 59),
        "input_bg": (27, 94, 32),
        "border": (249, 251, 231)
    }
}

# Set initial theme
current_theme = "classic"
theme = THEMES[current_theme]

# Load sounds
try:
    typing_sound = mixer.Sound(os.path.join(current_dir, "assets/sounds/typing.wav"))
    correct_sound = mixer.Sound(os.path.join(current_dir, "assets/sounds/correct.wav"))
    wrong_sound = mixer.Sound(os.path.join(current_dir, "assets/sounds/wrong.wav"))
    level_up_sound = mixer.Sound(os.path.join(current_dir, "assets/sounds/level_up.wav"))
except:
    # Create placeholder sounds if files don't exist
    typing_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    correct_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    wrong_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    level_up_sound = mixer.Sound(pygame.sndarray.array(pygame.Surface((1, 1))))
    print("Sound files not found, using placeholder sounds")

# Initialize high_score with a default value
high_score = 0
try:
    with open(os.path.join(current_dir, "Wordlist/highestScore.txt"), 'r') as file:
        read = file.readlines()
        high_score = int(read[0])
except (FileNotFoundError, IndexError):
    # Create the file if it doesn't exist
    with open(os.path.join(current_dir, "Wordlist/highestScore.txt"), 'w') as file:
        file.write("0")

name = "none"
try:
    with open(os.path.join(current_dir, "Wordlist/highest_scorer.txt"), 'r') as file:
        name = file.read()
except FileNotFoundError:
    with open(os.path.join(current_dir, "Wordlist/highest_scorer.txt"), 'w') as file:
        file.write("none")
    
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
new_level = True
choices = [False, False, True, True, True, False, False]

# Load fonts and store their file paths
try:
    font_path = os.path.join(current_dir, "fonts/Aroman.ttf")
    action_man_path = os.path.join(current_dir, "fonts/Action_Man.ttf")
    action_man_bold_path = os.path.join(current_dir, "fonts/Action_Man_Bold.ttf")
    
    fonts = pygame.font.Font(font_path, 35)
    action_man_fonts = pygame.font.Font(action_man_path, 35)
    action_man_fonts_bold = pygame.font.Font(action_man_bold_path, 35)
except:
    # Fallback to default font if custom fonts are not available
    print("Custom fonts not found, using default font")
    font_path = None
    action_man_path = None
    action_man_bold_path = None
    fonts = pygame.font.Font(None, 35)
    action_man_fonts = pygame.font.Font(None, 35)
    action_man_fonts_bold = pygame.font.Font(None, 35)

# Particle system for visual effects
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-3, -1)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size -= 0.1
        return self.lifetime > 0 and self.size > 0
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Enhanced Word class with animations and effects
class Word:
    def __init__(self, text, speed, y_pos, x_pos, is_bonus=False):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
        self.particles = []
        self.is_bonus = is_bonus
        self.color = (255, 215, 0) if is_bonus else theme["text"]
        self.scale = 1.0
        self.pulse_direction = 0.01
        self.original_y = y_pos
        self.amplitude = random.randint(5, 15)
        self.frequency = random.uniform(0.01, 0.03)
        self.time = 0
        
    def draw(self):
        # Make bonus words pulse and have a gold color
        if self.is_bonus:
            self.scale += self.pulse_direction
            if self.scale > 1.1 or self.scale < 0.9:
                self.pulse_direction *= -1
            
            # Render with scaled font
            scaled_font = pygame.font.Font(font_path, int(35 * self.scale))
            text_surface = scaled_font.render(self.text, True, self.color)
        else:
            text_surface = fonts.render(self.text, True, self.color)
            
        screen.blit(text_surface, (self.x_pos, self.y_pos))
        
        # Highlight matched part
        act_len = len(user_input)
        if user_input == self.text[:act_len] and act_len > 0:
            highlight_surface = fonts.render(user_input, True, theme["highlight"])
            screen.blit(highlight_surface, (self.x_pos, self.y_pos))
            
        # Draw particles
        for particle in self.particles:
            if particle.update():
                particle.draw(screen)
            else:
                self.particles.remove(particle)
                
    def add_particles(self, count):
        for _ in range(count):
            color = random.choice([(255, 215, 0), (255, 255, 255), theme["highlight"]])
            self.particles.append(Particle(self.x_pos + len(self.text) * 10, 
                                          self.y_pos + 15, 
                                          color))
            
    def update(self):
        self.x_pos -= self.speed
        self.time += 1
        
        # Add a slight wave motion to make words float
        self.y_pos = self.original_y + math.sin(self.time * self.frequency) * self.amplitude

# Power-up item class
class PowerUp:
    def __init__(self, x_pos, y_pos, power_type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = power_type  # 'extra_life', 'slow_time', 'double_points'
        self.width = 30
        self.height = 30
        self.active = True
        self.speed = 2
        self.angle = 0
        
        # Define colors based on power-up type
        if self.type == 'extra_life':
            self.color = (255, 0, 0)  # Red for life
        elif self.type == 'slow_time':
            self.color = (0, 191, 255)  # Blue for time slow
        elif self.type == 'double_points':
            self.color = (255, 215, 0)  # Gold for points
            
    def update(self):
        self.x_pos -= self.speed
        self.angle += 2  # Rotate the power-up
        return self.x_pos > -self.width
        
    def draw(self):
        # Draw a spinning icon based on power-up type
        if self.type == 'extra_life':
            # Heart shape
            center_x = self.x_pos + self.width // 2
            center_y = self.y_pos + self.height // 2
            points = []
            for i in range(0, 360, 10):
                rad = math.radians(i + self.angle)
                # Heart shape formula
                if i < 180:
                    r = 15 * (1 - math.cos(rad))
                else:
                    r = 10
                x = center_x + r * math.cos(rad)
                y = center_y + r * math.sin(rad)
                points.append((x, y))
            if len(points) > 2:
                pygame.draw.polygon(screen, self.color, points)
        elif self.type == 'slow_time':
            # Clock shape
            pygame.draw.circle(screen, self.color, 
                              (self.x_pos + self.width // 2, self.y_pos + self.height // 2), 
                              self.width // 2)
            # Clock hands
            center_x = self.x_pos + self.width // 2
            center_y = self.y_pos + self.height // 2
            # Hour hand
            hour_x = center_x + (self.width // 4) * math.cos(math.radians(self.angle))
            hour_y = center_y + (self.width // 4) * math.sin(math.radians(self.angle))
            pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (hour_x, hour_y), 2)
            # Minute hand
            min_x = center_x + (self.width // 3) * math.cos(math.radians(self.angle * 2))
            min_y = center_y + (self.width // 3) * math.sin(math.radians(self.angle * 2))
            pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (min_x, min_y), 2)
        elif self.type == 'double_points':
            # Star shape for points
            center_x = self.x_pos + self.width // 2
            center_y = self.y_pos + self.height // 2
            points = []
            for i in range(0, 360, 72):  # 5-pointed star
                # Outer point
                rad_outer = math.radians(i + self.angle)
                x_outer = center_x + (self.width // 2) * math.cos(rad_outer)
                y_outer = center_y + (self.width // 2) * math.sin(rad_outer)
                points.append((x_outer, y_outer))
                
                # Inner point
                rad_inner = math.radians(i + 36 + self.angle)
                x_inner = center_x + (self.width // 4) * math.cos(rad_inner)
                y_inner = center_y + (self.width // 4) * math.sin(rad_inner)
                points.append((x_inner, y_inner))
            
            if len(points) > 2:
                pygame.draw.polygon(screen, self.color, points)
                
    def check_collection(self, x, y, width, height):
        # Check if the power-up has been collected (collided with a word)
        if (isinstance(x, str)):  # If x is a string (user_input), don't use it for collision
            return False
        if (self.x_pos < x + width and
            self.x_pos + self.width > x and
            self.y_pos < y + height and
            self.y_pos + self.height > y):
            return True
        return False

# Background animation and effects
class Background:
    def __init__(self):
        self.stars = []
        self.generate_stars(100)
        
    def generate_stars(self, count):
        for _ in range(count):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT-100)  # Don't draw stars in input area
            size = random.uniform(0.5, 3)
            speed = random.uniform(0.2, 1.5)
            brightness = random.randint(100, 255)
            self.stars.append({
                'x': x, 
                'y': y, 
                'size': size, 
                'speed': speed,
                'brightness': brightness,
                'color': (brightness, brightness, brightness)
            })
            
    def update(self):
        for star in self.stars:
            # Move stars from right to left
            star['x'] -= star['speed']
            # If star goes off screen, reset to right side
            if star['x'] < 0:
                star['x'] = WIDTH
                star['y'] = random.randint(0, HEIGHT-100)
                
    def draw(self, surface):
        for star in self.stars:
            # Draw star as a small circle
            pygame.draw.circle(
                surface, 
                star['color'], 
                (int(star['x']), int(star['y'])), 
                int(star['size'])
            )

# Heart class for life display
class Heart:
    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size
        self.angle = 0
        self.pulse_direction = 0.02
        self.scale = 1.0
        # Add colors for gradient effect
        self.base_color = (255, 0, 0)  # Red
        self.highlight_color = (255, 100, 100)  # Light red
        self.outline_color = (150, 0, 0)  # Dark red for outline
        self.glow_particles = []
        
    def update(self):
        # Pulsating effect
        self.scale += self.pulse_direction
        if self.scale > 1.2 or self.scale < 0.8:
            self.pulse_direction *= -1
            
        # Occasionally add a glowing particle
        if random.random() < 0.05:
            self.glow_particles.append({
                'x': self.x,
                'y': self.y - self.size * 0.5,
                'size': random.uniform(1, 3),
                'alpha': 255,
                'speed': random.uniform(0.2, 0.8)
            })
            
        # Update glow particles
        for particle in list(self.glow_particles):
            particle['y'] -= particle['speed']
            particle['alpha'] -= 5
            if particle['alpha'] <= 0:
                self.glow_particles.remove(particle)
            
    def draw(self, surface):
        # Apply the scale from pulsing animation
        size = self.size * self.scale
        
        # Draw glow particles first (behind the heart)
        for particle in self.glow_particles:
            alpha = int(particle['alpha'])
            glow_color = (255, 100, 100, alpha)
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                glow_color,
                (particle['size'], particle['size']),
                particle['size']
            )
            surface.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Create a heart shape using Bezier approach
        # Two circles side by side with a triangle at the bottom
        
        # Create a surface for the heart with transparency
        heart_surface = pygame.Surface((int(size * 2.5), int(size * 2.5)), pygame.SRCALPHA)
        
        # Draw gradient for the heart
        # First the base color (main body)
        pygame.draw.circle(heart_surface, self.base_color, (int(size * 0.75), int(size * 0.75)), int(size * 0.75))
        pygame.draw.circle(heart_surface, self.base_color, (int(size * 1.75), int(size * 0.75)), int(size * 0.75))
        
        # Draw the bottom triangle part
        triangle_points = [
            (int(size * 0.25), int(size * 0.9)),  # Left point
            (int(size * 1.25), int(size * 2.0)),  # Bottom point
            (int(size * 2.25), int(size * 0.9))   # Right point
        ]
        pygame.draw.polygon(heart_surface, self.base_color, triangle_points)
        
        # Add highlights for 3D effect (lighter color at the top)
        highlight_radius = int(size * 0.5)
        pygame.draw.circle(heart_surface, self.highlight_color, (int(size * 0.65), int(size * 0.65)), highlight_radius)
        pygame.draw.circle(heart_surface, self.highlight_color, (int(size * 1.85), int(size * 0.65)), highlight_radius)
        
        # Add outline for definition
        pygame.draw.circle(heart_surface, self.outline_color, (int(size * 0.75), int(size * 0.75)), int(size * 0.75), 2)
        pygame.draw.circle(heart_surface, self.outline_color, (int(size * 1.75), int(size * 0.75)), int(size * 0.75), 2)
        pygame.draw.polygon(heart_surface, self.outline_color, triangle_points, 2)
        
        # Position and blit the heart
        heart_rect = heart_surface.get_rect(center=(self.x, self.y))
        surface.blit(heart_surface, heart_rect)

# Function to render text with shadow for better visibility
def render_text_with_shadow(text, font, color, shadow_color=(0, 0, 0), offset=2):
    # First render the shadow
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect()
    
    # Then render the text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    # Create a surface that can hold both
    combined_surface = pygame.Surface((text_rect.width + offset, text_rect.height + offset), 
                                     pygame.SRCALPHA)
    
    # Blit the shadow first, then the text
    combined_surface.blit(shadow_surface, (offset, offset))
    combined_surface.blit(text_surface, (0, 0))
    
    return combined_surface

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf
    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                self.clicked = True
        pygame.draw.circle(self.surf, theme["border"], (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(fonts.render(self.text, True, theme["text"]), (self.x_pos - 15, self.y_pos - 25))

def draw_screen():
    # Draw the input area and border
    pygame.draw.rect(screen, theme["input_bg"], [0, HEIGHT-100, WIDTH, 100], 0)
    pygame.draw.rect(screen, theme["border"], [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, theme["border"], (700, HEIGHT-100), (700, HEIGHT), 2)
    pygame.draw.line(screen, theme["border"], (0, HEIGHT-100), (WIDTH, HEIGHT-100), 2)
    
    # Draw current input
    screen.blit(fonts.render(f'=>{user_input}', True, theme["text"]), (20, HEIGHT-75))
    
    # Draw score with shadow for better visibility
    score_text = render_text_with_shadow(f'Score: {score}', fonts, theme["text"])
    screen.blit(score_text, (325, 10))
    
    # Draw high score
    high_score_text = render_text_with_shadow(f'Highest: {high_score}', fonts, theme["text"])
    screen.blit(high_score_text, (10, 10))
    
    # Draw scorer name
    name_text = render_text_with_shadow(f'MAX_Scorer: {name}', action_man_fonts_bold, theme["text"])
    screen.blit(name_text, (10, 75))
    
    # Draw hearts for lives
    for i in range(live):
        hearts[i].update()
        hearts[i].draw(screen)
    
    # Draw active power-ups
    if 'double_points' in power_timers and power_timers['double_points'] > 0:
        time_left = power_timers['double_points'] // fps
        multiplier_text = render_text_with_shadow(f'2x Points: {time_left}s', fonts, (255, 215, 0))
        screen.blit(multiplier_text, (325, 50))
    
    # Draw theme switcher button
    theme_btn = Button(698, HEIGHT-52, "T", False, screen)
    theme_btn.draw()
    
    # Draw pause button
    pause_btn = Button(748, HEIGHT-52, "| |", False, screen)
    pause_btn.draw()
    
    # Return button states
    return pause_btn.clicked, theme_btn.clicked

def draw_pause():
    level = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    resume_btn = Button(360, 200, '>', False, surface)
    resume_btn.draw()
    for i in range(len(choices)):
        btn = Button(160 + (i*80), 350, str(i+1), False, surface)
        btn.draw()
        if btn.clicked:
            if level[i]:
                level[i] = False
            else:
                level[i] = True
        if choices[i]:
            pygame.draw.circle(surface, theme["highlight"], (160 + (i*80), 350), 35, 3)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, level,

def Word_generate():
    word_lst = []
    include = []
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))

    y_pos = random.randint(150, 350)  # Randomize vertical position
    x_pos = WIDTH
    ind_sel = random.choice(include)
    index = random.randint(ind_sel[0], ind_sel[1])-1
    text = wordlist[index]
    
    # 10% chance of generating a bonus word
    is_bonus = random.random() < 0.1
    
    new_word = Word(text, speed, y_pos, x_pos, is_bonus)
    word_lst.append(new_word)
    
    # 5% chance of generating a power-up
    if random.random() < 0.05:
        power_type = random.choice(['extra_life', 'slow_time', 'double_points'])
        power_y = random.randint(100, 400)
        power_ups.append(PowerUp(WIDTH, power_y, power_type))
        
    return word_lst

def apply_power_up(power_type):
    global live, speed, score_multiplier
    
    if power_type == 'extra_life':
        live += 1
        # Flash a message
        power_up_messages.append({
            'text': "+1 Life!",
            'color': (255, 0, 0),
            'x': WIDTH // 2,
            'y': HEIGHT // 2,
            'lifetime': 60,
            'scale': 2.0
        })
    elif power_type == 'slow_time':
        # Slow down all words
        for word in word_list:
            word.speed *= 0.7
        # Flash a message
        power_up_messages.append({
            'text': "Slow Motion!",
            'color': (0, 191, 255),
            'x': WIDTH // 2,
            'y': HEIGHT // 2,
            'lifetime': 60,
            'scale': 2.0
        })
    elif power_type == 'double_points':
        # Double points for 10 seconds
        score_multiplier = 2
        # Start countdown timer
        power_timers['double_points'] = fps * 10  # 10 seconds
        # Flash a message
        power_up_messages.append({
            'text': "2x Points!",
            'color': (255, 215, 0),
            'x': WIDTH // 2,
            'y': HEIGHT // 2,
            'lifetime': 60,
            'scale': 2.0
        })

def input_name():
    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = fonts
    input_box_width, input_box_height = 300, 60
    input_box = pygame.Rect(WIDTH//2 - input_box_width//2, HEIGHT//2 - input_box_height//2 - 40, input_box_width, input_box_height)
    active = True
    text = ''
    done = False
    
    # For level selection
    selected_level = "fair"  # Default level
    
    # Create background effects
    bg = Background()
    particles = []
    
    # Add cursor blink effect
    cursor_visible = True
    cursor_timer = 0
    cursor_blink_rate = 30  # Frames between blinks
    
    # Create animated title text
    title_scale = 1.0
    title_scale_direction = 0.005
    title_rotation = 0
    
    # Decorative elements
    decorative_stars = []
    for _ in range(20):
        decorative_stars.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT//3),
            'size': random.uniform(1, 3),
            'angle': random.uniform(0, 360),
            'spin_speed': random.uniform(0.5, 2),
            'color': random.choice([(255, 255, 100), (255, 200, 100), (200, 255, 255)])
        })

    # Create a start button (moved further down)
    button_width, button_height = 200, 60
    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    button_rect = button_surface.get_rect(center=(WIDTH//2, HEIGHT - 80))  # Moved closer to bottom
    
    # Create level selection buttons
    level_button_width, level_button_height = 120, 50
    
    # Improved vertical spacing by adjusting the level elements position
    # Moved select level text further down from the name input
    level_text_y = HEIGHT//2 + 50
    
    # Junior level button - positioned on left side with more spacing and proper vertical position
    junior_button_surface = pygame.Surface((level_button_width, level_button_height), pygame.SRCALPHA)
    junior_button_rect = junior_button_surface.get_rect(center=(WIDTH//2 - 120, level_text_y + 60))
    
    # Fair level button - positioned on right side with more spacing and proper vertical position
    fair_button_surface = pygame.Surface((level_button_width, level_button_height), pygame.SRCALPHA)
    fair_button_rect = fair_button_surface.get_rect(center=(WIDTH//2 + 120, level_text_y + 60))
    
    while not done:
        # Update background
        screen.fill(theme["background"])
        bg.update()
        bg.draw(screen)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip():  # Only proceed if there's text
                            done = True
                            # Add particle burst on submit
                            for _ in range(50):
                                particles.append(Particle(WIDTH//2, HEIGHT//2, 
                                                        random.choice([(255, 215, 0), (255, 255, 255), theme["highlight"]])))
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        # Add particle when backspacing
                        if random.random() < 0.3:  # 30% chance for particle
                            particles.append(Particle(input_box.right - 10, input_box.centery, 
                                                    (255, 100, 100)))
                    else:
                        if len(text) < 20:  # Limit name length
                            text += event.unicode
                            # Play typing sound
                            typing_sound.play()
                            # Add typing particle
                            particles.append(Particle(input_box.x + len(text) * 15, 
                                                    input_box.centery, 
                                                    theme["highlight"]))
            
            # Check for button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(pygame.mouse.get_pos()) and text.strip():
                    done = True
                    # Add particle burst on submit
                    for _ in range(50):
                        particles.append(Particle(WIDTH//2, HEIGHT//2, 
                                                random.choice([(255, 215, 0), (255, 255, 255), theme["highlight"]])))
                # Check level button clicks
                if junior_button_rect.collidepoint(pygame.mouse.get_pos()):
                    selected_level = "junior"
                    # Add particles for visual feedback
                    for _ in range(20):
                        particles.append(Particle(junior_button_rect.centerx, junior_button_rect.centery, 
                                                (100, 255, 100)))
                elif fair_button_rect.collidepoint(pygame.mouse.get_pos()):
                    selected_level = "fair"
                    # Add particles for visual feedback
                    for _ in range(20):
                        particles.append(Particle(fair_button_rect.centerx, fair_button_rect.centery, 
                                                (255, 215, 0)))

        # Animate title
        title_scale += title_scale_direction
        if title_scale > 1.1 or title_scale < 0.9:
            title_scale_direction *= -1
        
        title_rotation += 0.2
        title_font = pygame.font.Font(action_man_bold_path, int(48 * title_scale))
        title_text = render_text_with_shadow("Speed Typing Adventure", title_font, 
                                           (255, 215, 0), offset=3)
        
        # Rotate title slightly for dynamic effect
        title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        title_surface.blit(title_text, (0, 0))
        title_surface = pygame.transform.rotate(title_surface, math.sin(math.radians(title_rotation)) * 3)
        
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Draw animated subtitle
        subtitle_text = render_text_with_shadow("Enter Your Name", font, theme["text"], offset=2)
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 170))
        screen.blit(subtitle_text, subtitle_rect)

        # Update cursor blink
        cursor_timer += 1
        if cursor_timer >= cursor_blink_rate:
            cursor_timer = 0
            cursor_visible = not cursor_visible
            
        # Draw decorative stars
        for star in decorative_stars:
            star['angle'] += star['spin_speed']
            # Draw 5-pointed star
            points = []
            for i in range(0, 360, 72):  # 5-pointed star
                rad_outer = math.radians(i + star['angle'])
                x_outer = star['x'] + star['size'] * 2 * math.cos(rad_outer)
                y_outer = star['y'] + star['size'] * 2 * math.sin(rad_outer)
                points.append((x_outer, y_outer))
                
                rad_inner = math.radians(i + 36 + star['angle'])
                x_inner = star['x'] + star['size'] * math.cos(rad_inner)
                y_inner = star['y'] + star['size'] * math.sin(rad_inner)
                points.append((x_inner, y_inner))
            
            if len(points) > 2:
                pygame.draw.polygon(screen, star['color'], points)

        # Draw enhanced input box with gradient
        # Create gradient background for input box
        input_surface = pygame.Surface((input_box.width, input_box.height), pygame.SRCALPHA)
        for i in range(input_box.height):
            # Create a subtle gradient
            alpha = 150  # Semi-transparent
            color = (theme["input_bg"][0], theme["input_bg"][1], theme["input_bg"][2], alpha)
            pygame.draw.line(input_surface, color, (0, i), (input_box.width, i))
            
        # Draw the input box with rounded corners
        pygame.draw.rect(input_surface, (255, 255, 255, 30), 
                        (0, 0, input_box.width, input_box.height), 0, border_radius=10)
        pygame.draw.rect(input_surface, theme["border"], 
                        (0, 0, input_box.width, input_box.height), 2, border_radius=10)
        
        # Add a subtle glow effect
        glow_size = 4
        for i in range(glow_size, 0, -1):
            alpha = 50 - i * 10
            glow_color = (255, 255, 255, alpha)
            pygame.draw.rect(
                input_surface, 
                glow_color, 
                (glow_size-i, glow_size-i, input_box.width-2*(glow_size-i), input_box.height-2*(glow_size-i)), 
                2, border_radius=10
            )
        
        # Draw text in input box
        if text:
            txt_surface = font.render(text, True, (255, 255, 255))
            txt_rect = txt_surface.get_rect(midleft=(input_box.x + 15, input_box.centery))
            # Ensure text stays within bounds
            if txt_rect.width > input_box.width - 20:
                txt_rect.x = input_box.x + input_box.width - txt_rect.width - 15
            
            # Blit input surface and text
            screen.blit(input_surface, input_box)
            screen.blit(txt_surface, txt_rect)
            
            # Add blinking cursor at end of text if visible
            if cursor_visible:
                cursor_x = txt_rect.right + 2
                if cursor_x < input_box.right - 10:
                    pygame.draw.line(screen, (255, 255, 255), 
                                    (cursor_x, txt_rect.y + 5), 
                                    (cursor_x, txt_rect.y + txt_rect.height - 5), 2)
        else:
            # Draw placeholder text
            placeholder = font.render("Type your name...", True, (200, 200, 200, 128))
            placeholder_rect = placeholder.get_rect(center=input_box.center)
            
            # Blit input surface and placeholder
            screen.blit(input_surface, input_box)
            screen.blit(placeholder, placeholder_rect)
            
            # Add blinking cursor if visible
            if cursor_visible:
                cursor_x = input_box.x + 15
                pygame.draw.line(screen, (255, 255, 255), 
                                (cursor_x, input_box.centery - 15), 
                                (cursor_x, input_box.centery + 15), 2)
        
        # Draw "Select Level" text
        level_text = render_text_with_shadow("Select Level:", font, theme["text"], offset=2)
        level_text_rect = level_text.get_rect(center=(WIDTH//2, level_text_y))
        screen.blit(level_text, level_text_rect)
        
        # Draw Junior button
        # Create gradient background for junior button
        for i in range(level_button_height):
            if selected_level == "junior":
                # Brighter gradient when selected
                color = (0, min(255, 100 + i * 4), min(255, 50 + i * 4))
            else:
                # Darker gradient when not selected
                color = (0, min(255, 50 + i * 3), min(255, 25 + i * 3))
            pygame.draw.line(junior_button_surface, color, (0, i), (level_button_width, i))
        
        # Add border and glow if selected
        if selected_level == "junior":
            # Draw glow effect
            glow_size = 4
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 20
                glow_color = (100, 255, 100, alpha)
                pygame.draw.rect(
                    junior_button_surface, 
                    glow_color, 
                    (glow_size-i, glow_size-i, level_button_width-2*(glow_size-i), level_button_height-2*(glow_size-i)), 
                    3
                )
            border_color = (255, 255, 255)
        else:
            border_color = (180, 180, 180)
            
        pygame.draw.rect(junior_button_surface, border_color, 
                        (0, 0, level_button_width, level_button_height), 2, border_radius=10)
        
        # Add text to junior button
        junior_text = render_text_with_shadow("Junior", action_man_fonts, (255, 255, 255), offset=2)
        junior_text_rect = junior_text.get_rect(center=(level_button_width // 2, level_button_height // 2))
        junior_button_surface.blit(junior_text, junior_text_rect)
        
        # Display junior mode description - positioned below its button
        if selected_level == "junior":
            description = pygame.font.Font(action_man_path, 16).render("Word speed stays constant", True, (100, 255, 100))
            description_rect = description.get_rect(midtop=(junior_button_rect.centerx, junior_button_rect.bottom + 5))
            screen.blit(description, description_rect)
            
        # Draw Fair button
        # Create gradient background for fair button
        for i in range(level_button_height):
            if selected_level == "fair":
                # Brighter gradient when selected
                color = (min(255, 200 + i * 1), min(255, 150 + i * 2), 0)
            else:
                # Darker gradient when not selected
                color = (min(255, 100 + i * 1), min(255, 75 + i * 2), 0)
            pygame.draw.line(fair_button_surface, color, (0, i), (level_button_width, i))
        
        # Add border and glow if selected
        if selected_level == "fair":
            # Draw glow effect
            glow_size = 4
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 20
                glow_color = (255, 200, 0, alpha)
                pygame.draw.rect(
                    fair_button_surface, 
                    glow_color, 
                    (glow_size-i, glow_size-i, level_button_width-2*(glow_size-i), level_button_height-2*(glow_size-i)), 
                    3
                )
            border_color = (255, 255, 255)
        else:
            border_color = (180, 180, 180)
            
        pygame.draw.rect(fair_button_surface, border_color, 
                        (0, 0, level_button_width, level_button_height), 2, border_radius=10)
        
        # Add text to fair button
        fair_text = render_text_with_shadow("Fair", action_man_fonts, (255, 255, 255), offset=2)
        fair_text_rect = fair_text.get_rect(center=(level_button_width // 2, level_button_height // 2))
        fair_button_surface.blit(fair_text, fair_text_rect)
        
        # Display fair mode description - positioned below its button
        if selected_level == "fair":
            description = pygame.font.Font(action_man_path, 16).render("Word speed increases over time", True, (255, 200, 0))
            description_rect = description.get_rect(midtop=(fair_button_rect.centerx, fair_button_rect.bottom + 5))
            screen.blit(description, description_rect)
                
        # Draw particles
        for particle in list(particles):
            if particle.update():
                particle.draw(screen)
            else:
                particles.remove(particle)
                
        # Draw the Start button with the same style as game over buttons
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)
        
        # Different button colors based on whether name is entered
        button_enabled = bool(text.strip())
        
        if button_hovered and button_enabled:
            # Create gradient for hover state (brighter colors)
            for i in range(button_height):
                # Gradient from green to teal when hovered
                color = (0, 255, min(255, i * 4))
                pygame.draw.line(button_surface, color, (0, i), (button_width, i))
            
            # Add glow effect when hovered
            glow_size = 4
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 20
                glow_color = (100, 255, 100, alpha)
                pygame.draw.rect(
                    button_surface, 
                    glow_color, 
                    (glow_size-i, glow_size-i, button_width-2*(glow_size-i), button_height-2*(glow_size-i)), 
                    3
                )
        else:
            # Normal state gradient (darker or disabled)
            for i in range(button_height):
                if button_enabled:
                    # Gradient from dark green to green
                    color = (0, min(255, 100 + i * 2), min(255, 50 + i * 2))
                else:
                    # Disabled gray gradient
                    gray = min(180, 100 + i)
                    color = (gray, gray, gray)
                pygame.draw.line(button_surface, color, (0, i), (button_width, i))
        
        # Add border
        pygame.draw.rect(button_surface, theme["border"], 
                        (0, 0, button_width, button_height), 2, border_radius=10)
        
        # Add text with shadow to button
        if button_enabled:
            button_text = render_text_with_shadow("Start Game", action_man_fonts_bold, (255, 255, 255), offset=2)
        else:
            button_text = render_text_with_shadow("Start Game", action_man_fonts_bold, (180, 180, 180), offset=2)
            
        button_text_rect = button_text.get_rect(center=(button_width // 2, button_height // 2))
        button_surface.blit(button_text, button_text_rect)
        
        # Blit buttons to screen
        screen.blit(button_surface, button_rect)
        screen.blit(junior_button_surface, junior_button_rect)
        screen.blit(fair_button_surface, fair_button_rect)
        
        # Add instructions at the bottom
        instruction_text = render_text_with_shadow("Press ENTER or click button to start", 
                                                 pygame.font.Font(action_man_path, 20), 
                                                 (200, 200, 200), offset=1)
        instruction_rect = instruction_text.get_rect(midbottom=(WIDTH//2, HEIGHT - 20))
        screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        timer.tick(fps)
        
    return text, selected_level

def final_screen():
    global score, final_name, selected_level
    
    # Setup
    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Create a background with animated effects
    bg = Background()
    particles = []
    decorative_stars = []
    
    # Create decorative elements - colorful stars in background
    for _ in range(30):
        decorative_stars.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'size': random.uniform(1.5, 4),
            'angle': random.uniform(0, 360),
            'spin_speed': random.uniform(0.5, 2),
            'color': random.choice([(255, 215, 0), (255, 100, 100), (100, 200, 255), (100, 255, 150)])
        })
    
    # Animation variables
    title_scale = 1.0
    title_scale_direction = 0.005
    title_rotation = 0
    time_elapsed = 0
    
    # Create share button
    share_button_width, share_button_height = 200, 60
    share_button_surface = pygame.Surface((share_button_width, share_button_height), pygame.SRCALPHA)
    share_button_rect = share_button_surface.get_rect(center=(WIDTH//2, HEIGHT - 80))
    
    # Create save screenshot button
    screenshot_button_width, screenshot_button_height = 240, 60
    screenshot_button_surface = pygame.Surface((screenshot_button_width, screenshot_button_height), pygame.SRCALPHA)
    screenshot_button_rect = screenshot_button_surface.get_rect(center=(WIDTH//2, HEIGHT - 150))
    
    # Create stats panel surface
    stats_panel_width, stats_panel_height = 500, 350
    stats_panel = pygame.Surface((stats_panel_width, stats_panel_height), pygame.SRCALPHA)
    stats_panel_rect = stats_panel.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    
    # For screenshot function
    screenshot_taken = False
    screenshot_message_timer = 0
    screenshot_count = 1
    
    # Create animated trophy
    trophy_angle = 0
    trophy_scale = 1.0
    trophy_scale_direction = 0.01
    
    # Track if we've already created the high score particles
    high_score_particles_created = False
    
    # Main loop
    done = False
    while not done:
        # Update timers
        time_elapsed += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_high_score()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
            
            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Share button click
                if share_button_rect.collidepoint(mouse_pos):
                    # Create screenshot when share button is clicked
                    timestamp = pygame.time.get_ticks()
                    screenshot_filename = f"typing_score_{timestamp}.png"
                    pygame.image.save(screen, os.path.join(current_dir, screenshot_filename))
                    screenshot_taken = True
                    screenshot_message_timer = 180  # Show message for 3 seconds
                    
                    # Add particles for visual feedback
                    for _ in range(30):
                        particles.append(Particle(share_button_rect.centerx, share_button_rect.centery, 
                                               (255, 215, 0)))
                
                # Screenshot button click
                if screenshot_button_rect.collidepoint(mouse_pos):
                    # Take a screenshot and save it with a unique name
                    screenshot_filename = f"typing_score_{screenshot_count}.png"
                    pygame.image.save(screen, os.path.join(current_dir, screenshot_filename))
                    screenshot_taken = True
                    screenshot_message_timer = 180  # Show message for 3 seconds
                    screenshot_count += 1
                    
                    # Add particles for visual feedback
                    for _ in range(30):
                        particles.append(Particle(screenshot_button_rect.centerx, screenshot_button_rect.centery, 
                                               (100, 255, 255)))

        # Clear screen with a gradient background
        screen.fill(theme["background"])
        bg.update()
        bg.draw(screen)
        
        # Update and draw decorative stars
        for star in decorative_stars:
            star['angle'] += star['spin_speed']
            # Draw 5-pointed star
            points = []
            for i in range(0, 360, 72):  # 5-pointed star
                rad_outer = math.radians(i + star['angle'])
                x_outer = star['x'] + star['size'] * 3 * math.cos(rad_outer)
                y_outer = star['y'] + star['size'] * 3 * math.sin(rad_outer)
                points.append((x_outer, y_outer))
                
                rad_inner = math.radians(i + 36 + star['angle'])
                x_inner = star['x'] + star['size'] * 1.5 * math.cos(rad_inner)
                y_inner = star['y'] + star['size'] * 1.5 * math.sin(rad_inner)
                points.append((x_inner, y_inner))
            
            if len(points) > 2:
                pygame.draw.polygon(screen, star['color'], points)
                
        # Draw animated title
        title_scale += title_scale_direction
        if title_scale > 1.1 or title_scale < 0.9:
            title_scale_direction *= -1
        
        title_rotation += 0.2
        title_font = pygame.font.Font(action_man_bold_path, int(48 * title_scale))
        title_text = render_text_with_shadow("Game Complete!", title_font, 
                                           (255, 215, 0), offset=3)
        
        # Rotate title slightly for dynamic effect
        title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        title_surface.blit(title_text, (0, 0))
        title_surface = pygame.transform.rotate(title_surface, math.sin(math.radians(title_rotation)) * 3)
        
        title_rect = title_surface.get_rect(center=(screen_width // 2, 80))
        screen.blit(title_surface, title_rect)
        
        # Draw stats panel with gradient background
        for i in range(stats_panel_height):
            alpha = 220  # Semi-transparent
            color_value = min(50 + i//2, 150)
            color = (color_value//3, color_value//2, color_value, alpha)
            pygame.draw.line(stats_panel, color, (0, i), (stats_panel_width, i))
        
        # Add border and glow
        pygame.draw.rect(stats_panel, (255, 255, 255, 100), 
                        (0, 0, stats_panel_width, stats_panel_height), 3, border_radius=15)
        
        # Add glow effect
        glow_size = 6
        for i in range(glow_size, 0, -1):
            alpha = 30 - i * 4
            glow_color = (255, 255, 255, alpha)
            pygame.draw.rect(
                stats_panel, 
                glow_color, 
                (glow_size-i, glow_size-i, stats_panel_width-2*(glow_size-i), stats_panel_height-2*(glow_size-i)), 
                3, border_radius=15
            )
        
        # Draw player info in the stats panel
        player_name_font = pygame.font.Font(action_man_bold_path, 40)
        player_name_text = render_text_with_shadow(f"Player: {final_name}", player_name_font, (255, 255, 255))
        player_name_rect = player_name_text.get_rect(center=(stats_panel_width//2, 60))
        stats_panel.blit(player_name_text, player_name_rect)
        
        # Draw animated trophy if score is high enough
        trophy_y_offset = math.sin(time_elapsed * 0.05) * 5  # Gentle floating effect
        trophy_scale += trophy_scale_direction
        if trophy_scale > 1.1 or trophy_scale < 0.9:
            trophy_scale_direction *= -1
            
        # Draw trophy at the right and animate it
        trophy_angle += 1
        trophy_points = []
        
        # Trophy cup
        cup_center_x = stats_panel_width - 80
        cup_center_y = 140 + trophy_y_offset
        
        # Base trophy color is gold
        trophy_color = (255, 215, 0)
        
        # Draw trophy cup with size based on score
        trophy_size = min(40, max(20, score // 100))
        
        # Trophy cup (circle)
        pygame.draw.circle(stats_panel, trophy_color, (cup_center_x, cup_center_y), trophy_size * trophy_scale)
        
        # Trophy handles (semi-circles on sides)
        pygame.draw.arc(stats_panel, trophy_color, 
                      (cup_center_x - trophy_size*2, cup_center_y - trophy_size, 
                       trophy_size*2, trophy_size*2), 
                      math.pi/2, 3*math.pi/2, 3)
        
        pygame.draw.arc(stats_panel, trophy_color, 
                      (cup_center_x + trophy_size*0.5, cup_center_y - trophy_size, 
                       trophy_size*2, trophy_size*2), 
                      -math.pi/2, math.pi/2, 3)
        
        # Trophy base
        pygame.draw.rect(stats_panel, trophy_color, 
                       (cup_center_x - trophy_size*0.5, cup_center_y + trophy_size*0.8, 
                        trophy_size, trophy_size*0.5))
        
        pygame.draw.rect(stats_panel, trophy_color, 
                       (cup_center_x - trophy_size, cup_center_y + trophy_size*1.3, 
                        trophy_size*2, trophy_size*0.3))
        
        # Check if player got high score
        is_high_score = score >= high_score
        
        # If high score, add particles around trophy
        if is_high_score and not high_score_particles_created:
            for _ in range(50):  # Create burst of particles
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(0.5, 2)
                color = random.choice([(255, 215, 0), (255, 255, 255), (255, 100, 100)])
                
                # Position particles around the trophy
                particles.append(Particle(
                    stats_panel_rect.x + cup_center_x,
                    stats_panel_rect.y + cup_center_y,
                    color
                ))
                
            high_score_particles_created = True
            
        # Add "NEW HIGH SCORE" text if appropriate
        if is_high_score:
            high_score_font = pygame.font.Font(action_man_bold_path, 24)
            high_score_text = render_text_with_shadow("NEW HIGH SCORE!", high_score_font, (255, 215, 0))
            
            # Make the text pulse
            pulse_scale = 1.0 + 0.1 * math.sin(time_elapsed * 0.1)
            high_score_text = pygame.transform.scale(high_score_text, 
                                                  (int(high_score_text.get_width() * pulse_scale),
                                                   int(high_score_text.get_height() * pulse_scale)))
            
            high_score_rect = high_score_text.get_rect(center=(cup_center_x, cup_center_y - 80))
            stats_panel.blit(high_score_text, high_score_rect)
        
        # Draw big score
        score_font = pygame.font.Font(action_man_bold_path, 72)
        score_color = (255, 255, 255) if not is_high_score else (255, 215, 0)
        score_text = render_text_with_shadow(f"{score}", score_font, score_color)
        score_rect = score_text.get_rect(center=(stats_panel_width//2, 150))
        stats_panel.blit(score_text, score_rect)
        
        # Draw "POINTS" text
        points_font = pygame.font.Font(action_man_path, 24)
        points_text = render_text_with_shadow("POINTS", points_font, (200, 200, 200))
        points_rect = points_text.get_rect(center=(stats_panel_width//2, 195))
        stats_panel.blit(points_text, points_rect)
        
        # Draw difficulty level
        level_label = "Junior Mode" if selected_level == "junior" else "Fair Mode"
        level_font = pygame.font.Font(action_man_path, 28)
        level_text = render_text_with_shadow(f"Difficulty: {level_label}", level_font, (200, 200, 200))
        level_rect = level_text.get_rect(center=(stats_panel_width//2, 230))
        stats_panel.blit(level_text, level_rect)
        
        # Draw max level reached
        max_level_font = pygame.font.Font(action_man_path, 28)
        max_level_text = render_text_with_shadow(f"Max Level: {level}", max_level_font, (200, 200, 200))
        max_level_rect = max_level_text.get_rect(center=(stats_panel_width//2, 265))
        stats_panel.blit(max_level_text, max_level_rect)
        
        # Blit the stats panel to the screen
        screen.blit(stats_panel, stats_panel_rect)
        
        # Draw share button with gradient and glow
        mouse_pos = pygame.mouse.get_pos()
        share_button_hovered = share_button_rect.collidepoint(mouse_pos)
        
        # Clear the button surface
        share_button_surface.fill((0, 0, 0, 0))
        
        if share_button_hovered:
            # Bright gradient when hovered
            for i in range(share_button_height):
                color = (min(255, 50 + i * 3), min(255, 150 + i * 2), 255)
                pygame.draw.line(share_button_surface, color, (0, i), (share_button_width, i))
                
            # Add glow effect
            glow_size = 5
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 15
                glow_color = (100, 200, 255, alpha)
                pygame.draw.rect(
                    share_button_surface, 
                    glow_color, 
                    (glow_size-i, glow_size-i, share_button_width-2*(glow_size-i), share_button_height-2*(glow_size-i)), 
                    3, border_radius=10
                )
        else:
            # Normal gradient when not hovered
            for i in range(share_button_height):
                color = (min(255, 30 + i * 1), min(255, 100 + i * 1), min(255, 200 + i * 1))
                pygame.draw.line(share_button_surface, color, (0, i), (share_button_width, i))
        
        # Add border to button
        pygame.draw.rect(share_button_surface, (255, 255, 255), 
                       (0, 0, share_button_width, share_button_height), 2, border_radius=10)
        
        # Add share text to button
        share_text = render_text_with_shadow("Share to Social", action_man_fonts_bold, (255, 255, 255), offset=2)
        share_text_rect = share_text.get_rect(center=(share_button_width // 2, share_button_height // 2))
        share_button_surface.blit(share_text, share_text_rect)
        
        # Draw screenshot button with gradient and glow
        screenshot_button_hovered = screenshot_button_rect.collidepoint(mouse_pos)
        
        # Clear the button surface
        screenshot_button_surface.fill((0, 0, 0, 0))
        
        if screenshot_button_hovered:
            # Bright gradient when hovered
            for i in range(screenshot_button_height):
                color = (min(255, 50 + i * 3), min(255, 200 + i), min(255, 150 + i * 2))
                pygame.draw.line(screenshot_button_surface, color, (0, i), (screenshot_button_width, i))
                
            # Add glow effect
            glow_size = 5
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 15
                glow_color = (100, 255, 200, alpha)
                pygame.draw.rect(
                    screenshot_button_surface, 
                    glow_color, 
                    (glow_size-i, glow_size-i, screenshot_button_width-2*(glow_size-i), screenshot_button_height-2*(glow_size-i)), 
                    3, border_radius=10
                )
        else:
            # Normal gradient when not hovered
            for i in range(screenshot_button_height):
                color = (min(255, 30 + i * 1), min(255, 150 + i * 1), min(255, 100 + i * 1))
                pygame.draw.line(screenshot_button_surface, color, (0, i), (screenshot_button_width, i))
        
        # Add border to button
        pygame.draw.rect(screenshot_button_surface, (255, 255, 255), 
                       (0, 0, screenshot_button_width, screenshot_button_height), 2, border_radius=10)
        
        # Add save screenshot text to button
        screenshot_text = render_text_with_shadow("Save Screenshot", action_man_fonts_bold, (255, 255, 255), offset=2)
        screenshot_text_rect = screenshot_text.get_rect(center=(screenshot_button_width // 2, screenshot_button_height // 2))
        screenshot_button_surface.blit(screenshot_text, screenshot_text_rect)
        
        # Blit buttons to screen
        screen.blit(share_button_surface, share_button_rect)
        screen.blit(screenshot_button_surface, screenshot_button_rect)
        
        # Show screenshot taken message if needed
        if screenshot_taken:
            screenshot_message_timer -= 1
            if screenshot_message_timer > 0:
                alpha = min(255, screenshot_message_timer * 4)
                message_font = pygame.font.Font(action_man_bold_path, 24)
                message_text = render_text_with_shadow("Screenshot Saved!", message_font, (100, 255, 100))
                message_text.set_alpha(alpha)
                message_rect = message_text.get_rect(center=(WIDTH//2, HEIGHT - 200))
                screen.blit(message_text, message_rect)
            else:
                screenshot_taken = False
                
        # Display instructions
        instruction_text = render_text_with_shadow("Press ENTER to continue", 
                                                pygame.font.Font(action_man_path, 20), 
                                                (200, 200, 200), offset=1)
        instruction_rect = instruction_text.get_rect(midbottom=(WIDTH//2, HEIGHT - 20))
        screen.blit(instruction_text, instruction_rect)
        
        # Update and draw particles
        for particle in list(particles):
            if particle.update():
                particle.draw(screen)
            else:
                particles.remove(particle)
        
        pygame.display.flip()
        timer.tick(fps)
    
    check_high_score()
    return final_name

def check_answer(score):
    global speed
    global level
    global score_multiplier
    global selected_level
    
    for w in word_list:
        if w.text == submit:
            point = len(w.text)
            # Apply score multiplier for bonus words or power-ups
            if w.is_bonus:
                point *= 2
                power_up_messages.append({
                    'text': "Bonus Word!",
                    'color': (255, 215, 0),
                    'x': w.x_pos + len(w.text) * 10,
                    'y': w.y_pos,
                    'lifetime': 40,
                    'scale': 1.5
                })
            
            # Apply current score multiplier
            score += int(int(point) * speed * score_multiplier)
            
            # Create particle effect at word position
            w.add_particles(20)
            
            # Remove the word and play sound
            word_list.remove(w)
            
            # Only increase speed in Fair mode, keep constant in Junior mode
            if selected_level == "fair":
                speed += 0.5
                
            correct_sound.play()
            
            # Show the points gained
            power_up_messages.append({
                'text': f"+{int(int(point) * speed * score_multiplier)}",
                'color': (0, 255, 0),
                'x': w.x_pos + len(w.text) * 10,
                'y': w.y_pos - 30,
                'lifetime': 30,
                'scale': 1.0
            })
            
    return score

def check_high_score():
    global high_score
    global final_name
    if score > high_score:
        high_score = score
        with open(os.path.join(current_dir, "Wordlist/highestScore.txt"), 'w') as file:
            file.write(str(int(high_score)))

        with open(os.path.join(current_dir, "Wordlist/highest_scorer.txt"), 'w') as name_file:
            if(final_name == ''):
                name_file.write(str("none"))
            else:
                name_file.write(str(final_name))

def cycle_theme():
    global current_theme, theme
    themes = list(THEMES.keys())
    current_index = themes.index(current_theme)
    current_index = (current_index + 1) % len(themes)
    current_theme = themes[current_index]
    theme = THEMES[current_theme]
    
    # Add a message showing the theme change
    power_up_messages.append({
        'text': f"Theme: {current_theme.capitalize()}",
        'color': theme["highlight"],
        'x': WIDTH // 2,
        'y': HEIGHT // 2,
        'lifetime': 60,
        'scale': 1.5
    })

def draw_game_over_screen():
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Dark semi-transparent background
    screen.blit(overlay, (0, 0))
    
    # Game over text
    game_over_text = render_text_with_shadow("Game Over", action_man_fonts_bold, (255, 0, 0), offset=3)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(game_over_text, game_over_rect)
    
    # Score display
    score_text = render_text_with_shadow(f"Your Score: {score}", fonts, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)
    
    # Display difficulty level
    level_label = "Junior" if selected_level == "junior" else "Fair"
    level_text = render_text_with_shadow(f"Difficulty: {level_label}", fonts, (200, 200, 200))
    level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(level_text, level_rect)
    
    # Create beautiful buttons with gradients and animations
    # Restart button
    restart_button_width, restart_button_height = 180, 60
    restart_surface = pygame.Surface((restart_button_width, restart_button_height), pygame.SRCALPHA)
    
    # New game button
    new_game_button_width, new_game_button_height = 180, 60
    new_game_surface = pygame.Surface((new_game_button_width, new_game_button_height), pygame.SRCALPHA)
    
    # Get mouse position for hover effects
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    
    # Position the buttons
    restart_rect = restart_surface.get_rect(center=(WIDTH // 3, HEIGHT * 2 // 3))
    new_game_rect = new_game_surface.get_rect(center=(WIDTH * 2 // 3, HEIGHT * 2 // 3))
    
    # Check if mouse is hovering over restart button
    restart_hovered = restart_rect.collidepoint(mouse_pos)
    restart_clicked = False
    
    # Draw restart button with gradient and glow effect
    if restart_hovered:
        # Create gradient for hover state (brighter colors)
        for i in range(restart_button_height):
            # Gradient from red to orange when hovered
            color = (255, min(255, i * 4), 0)
            pygame.draw.line(restart_surface, color, (0, i), (restart_button_width, i))
        
        # Add glow effect when hovered
        glow_size = 4
        for i in range(glow_size, 0, -1):
            alpha = 100 - i * 20
            glow_color = (255, 200, 0, alpha)
            pygame.draw.rect(
                restart_surface, 
                glow_color, 
                (glow_size-i, glow_size-i, restart_button_width-2*(glow_size-i), restart_button_height-2*(glow_size-i)), 
                3
            )
            
        # Check for click
        if mouse_pressed:
            restart_clicked = True
    else:
        # Normal state gradient (darker)
        for i in range(restart_button_height):
            # Gradient from dark red to red
            color = (min(255, 150 + i * 2), min(255, i * 2), 0)
            pygame.draw.line(restart_surface, color, (0, i), (restart_button_width, i))
    
    # Add border
    pygame.draw.rect(restart_surface, (255, 255, 255), 
                    (0, 0, restart_button_width, restart_button_height), 2, border_radius=10)
    
    # Add text with shadow to restart button
    restart_text = render_text_with_shadow("Restart", action_man_fonts_bold, (255, 255, 255), offset=2)
    restart_text_rect = restart_text.get_rect(center=(restart_button_width // 2, restart_button_height // 2))
    restart_surface.blit(restart_text, restart_text_rect)
    
    # Check if mouse is hovering over new game button
    new_game_hovered = new_game_rect.collidepoint(mouse_pos)
    new_game_clicked = False
    
    # Draw new game button with gradient and glow effect
    if new_game_hovered:
        # Create gradient for hover state (brighter colors)
        for i in range(new_game_button_height):
            # Gradient from blue to cyan when hovered
            color = (0, min(255, 100 + i * 2), 255)
            pygame.draw.line(new_game_surface, color, (0, i), (new_game_button_width, i))
            
        # Add glow effect when hovered
        glow_size = 4
        for i in range(glow_size, 0, -1):
            alpha = 100 - i * 20
            glow_color = (0, 200, 255, alpha)
            pygame.draw.rect(
                new_game_surface, 
                glow_color, 
                (glow_size-i, glow_size-i, new_game_button_width-2*(glow_size-i), new_game_button_height-2*(glow_size-i)), 
                3
            )
            
        # Check for click
        if mouse_pressed:
            new_game_clicked = True
    else:
        # Normal state gradient (darker)
        for i in range(new_game_button_height):
            # Gradient from dark blue to blue
            color = (0, min(255, i * 2), min(255, 150 + i * 2))
            pygame.draw.line(new_game_surface, color, (0, i), (new_game_button_width, i))
    
    # Add border
    pygame.draw.rect(new_game_surface, (255, 255, 255), 
                    (0, 0, new_game_button_width, new_game_button_height), 2, border_radius=10)
    
    # Add text with shadow to new game button
    new_game_text = render_text_with_shadow("New Game", action_man_fonts_bold, (255, 255, 255), offset=2)
    new_game_text_rect = new_game_text.get_rect(center=(new_game_button_width // 2, new_game_button_height // 2))
    new_game_surface.blit(new_game_text, new_game_text_rect)
    
    # Blit buttons to screen
    screen.blit(restart_surface, restart_rect)
    screen.blit(new_game_surface, new_game_rect)
    
    return restart_clicked, new_game_clicked

run = True
final_name, selected_level = input_name()
background = Background()
hearts = [Heart(600 + i * 30, 10) for i in range(5)]
word_list = []  # Initialize word_list at the start

# Main game loop
while run:
    screen.fill(theme["background"])
    background.update()
    background.draw(screen)
    timer.tick(fps)
    
    pause_butt, theme_butt = draw_screen()
    if theme_butt:
        cycle_theme()
        
    # Handle paused state
    if paused:
        resume_butt, changes = draw_pause()
        if resume_butt:
            check_high_score()
            paused = False
            
    # Handle game over state
    if game_over:
        restart_clicked, new_game_clicked = draw_game_over_screen()
        if restart_clicked:
            # Reset game state when restart button is clicked
            game_over = False
            paused = False
            level = 1
            live = 3
            word_list = []
            new_level = True
            score = 0
            speed = 1.5  # Reset speed to initial value
            user_input = ""
            power_ups = []
            power_timers = {}
            power_up_messages = []
            score_multiplier = 1
        elif new_game_clicked:
            # Reset game state and prompt for new name
            final_name, selected_level = input_name()
            game_over = False
            paused = False
            level = 1
            live = 3
            word_list = []
            new_level = True
            score = 0
            speed = 1.5  # Reset speed to initial value
            user_input = ""
            power_ups = []
            power_timers = {}
            power_up_messages = []
            score_multiplier = 1
    # Only proceed with normal game logic if not in game over state
    elif not paused:
        # Generate words for new level
        if new_level:
            word_list = Word_generate()
            new_level = False
            # level_up_sound.play()
        else:
            # Process words
            for w in word_list:
                w.draw()
                w.update()
                if w.x_pos < -100:
                    word_list.remove(w)
                    live -= 1
                    user_input = ''
                    wrong_sound.play()
                    
            # Process power-ups
            for power_up in power_ups:
                power_up.draw()
                power_up.update()
                if power_up.check_collection(user_input, HEIGHT-100, WIDTH, 100):
                    apply_power_up(power_up.type)
                    power_ups.remove(power_up)
                    
            # Check if level completed
            if len(word_list) <= 0:
                level += 1
                new_level = True
                
            # Check if game over
            if live == 0:
                check_high_score() 
                game_over = True
    
    # Handle input regardless of game state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        if event.type == pygame.KEYDOWN:
            if not paused and not game_over:
                if event.unicode.lower() in letter:
                    user_input += event.unicode
                    typing_sound.play()
                if event.key == pygame.K_BACKSPACE and len(user_input) > 0:
                    user_input = user_input[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = user_input
                    user_input = ''
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes
                
    # Process submitted text           
    if submit != '' and not game_over:
        score = check_answer(score)
        submit = ''
        
    # Handle pause button
    if pause_butt and not game_over:
        paused = True
        
    # Update power-up timers
    for power_type in list(power_timers.keys()):
        if power_timers[power_type] > 0:
            power_timers[power_type] -= 1
            if power_timers[power_type] <= 0:
                if power_type == 'double_points':
                    score_multiplier = 1
                power_timers.pop(power_type)
                
    # Update and draw power-up messages
    for msg in list(power_up_messages):
        msg['lifetime'] -= 1
        if msg['lifetime'] <= 0:
            power_up_messages.remove(msg)
        else:
            # Fade out and float up
            alpha = min(255, msg['lifetime'] * 6)
            text_surface = render_text_with_shadow(msg['text'], fonts, msg['color'])
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=(msg['x'], msg['y'] - (60 - msg['lifetime']) * 0.5))
            screen.blit(text_surface, text_rect)
            
    pygame.display.flip()
    
ok = final_screen()
pygame.quit()