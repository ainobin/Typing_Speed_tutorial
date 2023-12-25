import pygame, random, copy

pygame.init()

from nltk.corpus import words

wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))
# print(len_indexes)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Typing Tutorial")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

level = 1
active_string = ""
score = 0
paused = False
submit = ''
word_objects = []
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
new_level = True
choices = [False, True, False, False, False, False, False]

fonts = pygame.font.Font("E:\JKKNIU\project typing tutorial\Typing Tutorial\Aroman.ttf", 40)

class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
    def draw(self):
        color = 'black'
        screen.blit(fonts.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(fonts.render(active_string, True, 'green'),(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed

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
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(fonts.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))

def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT-100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    # pygame.draw.rect(screen, 'Black', [0, 0, WIDTH, HEIGHT], 2)
    # pygame.draw.line(screen, 'white',(250, HEIGHT-100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white',(700, HEIGHT-100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white',(0, HEIGHT-100), (WIDTH, HEIGHT-100 ), 2)
    
    # screen.blit(fonts.render(f'Level: {level}', True, 'white'),(10, HEIGHT-75))
    screen.blit(fonts.render(f'=>{active_string}', True, 'white'),(20, HEIGHT-75))
    pause_btn = Button(748, HEIGHT-52, "| |", False, screen)
    pause_btn.draw()

    screen.blit(fonts.render(f'Score: {score}', True, 'black'), (10, 10))

    return pause_btn.clicked

def draw_pause():
    choices_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)

    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()
    for i in range(len(choices)):
        btn = Button(160 + (i*80), 350, str(i+2), False, surface)
        btn.draw()
        if btn.clicked:
            if choices_commits[i]:
                choices_commits[i] = False
            else:
                choices_commits[i] = True

        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i*80), 350), 35, 5)

    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choices_commits,

def generate_level():
    word_lst=[]
    include = []
    verticle_spacing = (HEIGHT-150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))
    for i in range(level):
        speed = 1.5
        y_pos = random.randint(10+(i*verticle_spacing), (i+1)*verticle_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 100)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_lst.append(new_word)

    return word_lst

def check_answer(score):
    for w in word_objects:
        if w.text == submit:
            point = len(w.text)
            score += int(point)
            word_objects.remove(w)
    return score


run = True
while run:
    screen.fill("gray")
    timer.tick(fps)

    pause_butt = draw_screen()

    if paused:
        resume_butt, changes = draw_pause()
        if resume_butt:
            paused = False
    if new_level and not paused:
        word_objects = generate_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
    if len(word_objects) <= 0 and not paused:
        new_level = True
    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letter:
                    active_string += event.unicode
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes
    if pause_butt:
        paused = True

    pygame.display.flip()
pygame.quit()