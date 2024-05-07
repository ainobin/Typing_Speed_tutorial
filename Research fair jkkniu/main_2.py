import pygame, random, copy, sys

pygame.init()

# from nltk.corpus import words
# from nltk.corpus import words
# wordlist = words.words()

# from file
with open(r"E:\Research fair jkkniu\10k_words.txt", 'r') as file:
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

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Typing Tutorial")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
level = 1
live = 3
user_input = ""
score = 0
speed = 1.5
paused = False
submit = ''
file = open(r"E:\Research fair jkkniu\highestScore.txt", 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

with open(r"E:\Research fair jkkniu\highest_scorer.txt", 'r') as file:
    name = file.read()
    
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
new_level = True
choices = [False, False, True, True, True, False, False]
fonts = pygame.font.Font(r"E:\JKKNIU\project typing tutorial\Typing Tutorial\Aroman.ttf", 35)
High_fonts = pygame.font.Font(r"E:\JKKNIU\project typing tutorial\Typing Tutorial\Aroman.ttf", 30)
class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
    def draw(self):
        screen.blit(fonts.render(self.text, True, 'black'), (self.x_pos, self.y_pos))
        act_len = len(user_input)
        if user_input == self.text[:act_len]:
            screen.blit(fonts.render(user_input, True, 'green'), (self.x_pos, self.y_pos))
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
                # pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(fonts.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))
def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT-100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white',(700, HEIGHT-100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white',(0, HEIGHT-100), (WIDTH, HEIGHT-100 ), 2)
    screen.blit(fonts.render(f'=>{user_input}', True, 'white'),(20, HEIGHT-75))
    screen.blit(fonts.render(f'Score: {score}', True, 'black'), (325, 10))
    screen.blit(fonts.render(f'Highest: {high_score}', True, 'black'), (10, 10))
    screen.blit(fonts.render(f'MAX_Scorer: {name}', True, 'black'), (10, 75))
    screen.blit(fonts.render(f'Lives: {live}', True, 'black'), (600, 10))
    pause_btn = Button(748, HEIGHT-52, "| |", False, screen)
    pause_btn.draw()
    return pause_btn.clicked

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
            pygame.draw.circle(surface, 'green', (160 + (i*80), 350), 35, 3)
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

    y_pos = 250
    x_pos = WIDTH
    ind_sel = random.choice(include)
    index = random.randint(ind_sel[0], ind_sel[1])-1
    # text = wordlist[index].lower()
    # print(index)
    text = wordlist[index]
    new_word = Word(text, speed, y_pos, x_pos)
    word_lst.append(new_word)
    return word_lst

def input_name():
    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = fonts
    input_box = pygame.Rect(300, 250, 100, 50)
    color = pygame.Color('white')
    active = True
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))

        caption = font.render("Enter Your Name", True, (255, 255, 255))
        caption_rect = caption.get_rect(center=(screen_width // 2, 100))
        screen.blit(caption, caption_rect)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
    return text

def final_screen():
    global score
    screen_width = WIDTH
    screen_height = HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = fonts
    input_box = pygame.Rect(300, 250, 100, 50)
    color = pygame.Color(30,30,30)
    active = True
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))

        caption = font.render("Thanks for playing", True, (255, 255, 255))
        screen.blit(font.render(f'your score is:  {score}', True, 'white'),(275,300))
        caption_rect = caption.get_rect(center=(screen_width // 2, 100))
        screen.blit(caption, caption_rect)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
    check_high_score()
    return text

def check_answer(score):
    global speed
    global level
    for w in word_list:
        if w.text == submit:
            point = len(w.text)
            score += int(int(point)*speed)
            word_list.remove(w)
            speed += 0.5
    return score

def check_high_score():
    global high_score
    global final_name
    if score > high_score:
        high_score = score
        file = open(r"E:\Research fair jkkniu\highestScore.txt", 'w')
        file.write(str(int(high_score)))
        file.close()

        name_file = open(r"E:\Research fair jkkniu\highest_scorer.txt", 'w')
        if(final_name == ''):
            name_file.write(str("none"))
        else:
            name_file.write(str(final_name))
        name_file.close()




run = True
final_name = input_name()
while run:
    screen.fill("gray")
    timer.tick(fps)
    pause_butt = draw_screen()
    if paused:
        resume_butt, changes = draw_pause()
        if resume_butt:
            check_high_score()
            paused = False
    if new_level and not paused:
        word_list = Word_generate()
        new_level = False
    else:
        for w in word_list:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -100:
                word_list.remove(w)
                live -= 1
    if len(word_list) <= 0 and not paused:
        level += 1
        new_level = True
    if live == 0:
        check_high_score() 
        run = False
    if len(word_list) <= 0 and not paused:
        new_level = True
    if submit != '':
        score = check_answer(score)
        submit = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letter:
                    user_input += event.unicode
                if event.key == pygame.K_BACKSPACE and len(user_input) > 0:
                    user_input = user_input[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = user_input
                    user_input = ''
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes
    if pause_butt:
        paused = True
    if live < 0:
        paused = True
        level = 1
        live = 3
        word_objects = []
        new_level = True
        check_high_score()
        score = 0    
    pygame.display.flip()
ok = final_screen()
pygame.quit()