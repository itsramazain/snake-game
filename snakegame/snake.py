import random
import pygame
import sys


pygame.init()
appels_you_fucking_demolished = 0
# soooooooo we have a 20*20 size for each body part, in 600 width and height we can fit a 30 part in one row and one col
WIDTH = 20
HEIGHT = 20
NUMBEROFPARTSTHATFIT = 30
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('snake game')
pygame.display.set_icon(pygame.image.load('Graphics\\cutesnake101.png'))
sake_head_down = pygame.image.load('Graphics\\head_down.png').convert_alpha()
sake_head_left = pygame.image.load('Graphics\\head_left.png').convert_alpha()
sake_head_right = pygame.image.load('Graphics\\head_right.png').convert_alpha()
sake_head_up = pygame.image.load('Graphics\\head_up.png').convert_alpha()
sake_body_topleft = pygame.image.load('Graphics\\body_topleft.png').convert_alpha()
sake_body_bottomleft = pygame.image.load('Graphics\\body_bottomleft.png').convert_alpha()
sake_body_topright = pygame.image.load('Graphics\\body_topright.png').convert_alpha()
sake_body_bottomright = pygame.image.load('Graphics\\body_bottomright.png').convert_alpha()
sake_body_vertical = pygame.image.load('Graphics\\body_vertical.png').convert_alpha()
sake_body_horizantal = pygame.image.load('Graphics\\body_horizontal.png').convert_alpha()
appelpic = pygame.image.load('Graphics\\apple.png').convert_alpha()
snake_tail_up = pygame.image.load('Graphics\\tail_up.png').convert_alpha()
snake_tail_down = pygame.image.load('Graphics\\tail_down.png').convert_alpha()
snake_tail_left = pygame.image.load('Graphics\\tail_left.png').convert_alpha()
snake_tail_right = pygame.image.load('Graphics\\tail_right.png').convert_alpha()
clock = pygame.time.Clock()
ate = False
backgroundsound=pygame.mixer.Sound('Sounds\\backgroundsound.mp3')
backgroundsound.play(loops=-1)
die=pygame.mixer.Sound('Sounds\\gameover.mp3')
munch=pygame.mixer.Sound('Sounds\\munch.mp3')
timer=pygame.USEREVENT+2
pygame.time.set_timer(timer,1000)
class Apple():
    def __init__(self):
        self.image = appelpic
        # what i want is to be spawned in a random pos that is one of the 30 cells not just a random spot yk!!
        self.rect = self.image.get_rect(topleft=(random.randint(1, 29) * 20, random.randint(1, 29) * 20))

    def showappel(self):
        screen.blit(self.image, self.rect)


screenappel = Apple()
direction = 'down'


class Snake():
    global ate

    def __init__(self):
        self.topleftx_head = 0
        self.toplefty_head = 40
        self.body_parts = [(0, 0), (0, 20), (0, 40)]  # this takes in the topleft point for every bodypart

    def show_snake(self):
        global sound
        new_vector_list = []
        for toplefts in self.body_parts:
            new_vector_list.insert(0, pygame.math.Vector2(toplefts[0], toplefts[1]))
        for index, toplefts in enumerate(self.body_parts):
            if self.body_parts[-1][0] > self.body_parts[-2][0] and self.body_parts[-1][1] == self.body_parts[-2][
                1] and index == len(self.body_parts) - 1:
                self.part_image = sake_head_right  # the head
                # how to animate the rest of the body??
            elif self.body_parts[-1][0] < self.body_parts[-2][0] and self.body_parts[-1][1] == self.body_parts[-2][
                1] and index == len(self.body_parts) - 1:
                self.part_image = sake_head_left
            elif self.body_parts[-1][1] < self.body_parts[-2][1] and self.body_parts[-1][0] == self.body_parts[-2][
                0] and index == len(self.body_parts) - 1:
                self.part_image = sake_head_up
            elif self.body_parts[-1][1] > self.body_parts[-2][1] and self.body_parts[-1][0] == self.body_parts[-2][
                0] and index == len(self.body_parts) - 1:
                self.part_image = sake_head_down
            elif index == 0 and toplefts[1] > self.body_parts[1][1]:
                self.part_image = snake_tail_down
            elif index == 0 and toplefts[1] < self.body_parts[1][1]:
                self.part_image = snake_tail_up
            elif index == 0 and toplefts[0] < self.body_parts[1][0]:
                self.part_image = snake_tail_left
            elif index == 0 and toplefts[0] > self.body_parts[1][0]:
                self.part_image = snake_tail_right
            else:  # this means its the middel part of the snake its eather _ or | or curved
                # this fucking shit took me like 6 hours aHHHHHHHHHHHHHHHHHHHHHHHH
                # its the opposite of what i wanted, like have an l its supposed to be bottom left but its top right WTF is wrong with this game !!!!
                try:
                    my_block = toplefts
                    next_block = self.body_parts[index + 1]
                    pre_block = self.body_parts[index - 1]
                    if my_block[0] == next_block[0] == pre_block[0]:
                        self.part_image = sake_body_vertical
                    elif my_block[1] == next_block[1] == pre_block[1]:
                        self.part_image = sake_body_horizantal
                    elif my_block[0] == pre_block[0] < next_block[0] and my_block[1] == next_block[1] > pre_block[1]:
                        self.part_image = sake_body_topright
                    elif my_block[0] == next_block[0] < pre_block[0] and my_block[1] == pre_block[1] > next_block[1]:
                        self.part_image = sake_body_topright
                    elif my_block[0] == pre_block[0] > next_block[0] and my_block[1] == next_block[1] > pre_block[1]:
                        self.part_image = sake_body_topleft
                    elif my_block[0] == next_block[0] > pre_block[0] and my_block[1] == pre_block[1] > next_block[1]:
                        self.part_image = sake_body_topleft
                    elif my_block[0] == pre_block[0] < next_block[0] and my_block[1] == next_block[1] < pre_block[1]:
                        self.part_image = sake_body_bottomright
                    elif my_block[0] == next_block[0] < pre_block[0] and my_block[1] == pre_block[1] < next_block[1]:
                        self.part_image = sake_body_bottomright
                    elif my_block[0] == next_block[0] > pre_block[0] and my_block[1] == pre_block[1] < next_block[1]:
                        self.part_image = sake_body_bottomleft
                    elif my_block[0] == pre_block[0] > next_block[0] and my_block[1] == next_block[1] < pre_block[1]:
                        self.part_image = sake_body_bottomleft
                except:#this means its new game wit 3 parts
                    self.part_image = sake_body_vertical
            self.part_rect = self.part_image.get_rect(topleft=toplefts)
            screen.blit(self.part_image, self.part_rect)

    def move(self):
        global ate, game_on
        if direction == 'down':
            self.toplefty_head += 20
        if direction == 'up':
            self.toplefty_head -= 20
        if direction == 'right':
            self.topleftx_head += 20
        if direction == 'left':
            self.topleftx_head -= 20
        self.body_parts.append((self.topleftx_head, self.toplefty_head))
        for toplefts in self.body_parts[:-1]:
            if pygame.Rect(toplefts[0], toplefts[1], 20, 20).colliderect(
                    pygame.Rect(snake.body_parts[-1][0], snake.body_parts[-1][1], 20, 20)):
                game_on = False
                global sound
                sound=True
                with open('highscore.txt') as f:
                    highscore = int(f.read())
                    if highscore < appels_you_fucking_demolished:
                        with open('highscore.txt', 'w') as f:
                            f.write(str(appels_you_fucking_demolished))

        if not pygame.Rect(snake.body_parts[-1][0], snake.body_parts[-1][1], 20, 20).colliderect(screenappel.rect):
            self.body_parts = self.body_parts[1:]


snake = Snake()
move_time = pygame.USEREVENT + 1
pygame.time.set_timer(move_time, 100)
game_on = False


def ateappel():
    global appels_you_fucking_demolished
    if pygame.Rect(snake.body_parts[-1][0], snake.body_parts[-1][1], 20, 20).colliderect(screenappel.rect):
        appels_you_fucking_demolished += 1

        return True
    else:
        return False

sound=False
def end_game():
    did_snake_touch_corner = pygame.Rect(snake.body_parts[-1][0], snake.body_parts[-1][1], 20, 20).colliderect(
        screen.get_rect(topleft=(0, 0)))
    if did_snake_touch_corner:
        global sound
        sound = True
        with open('highscore.txt') as f:
            highscore = int(f.read())
            if highscore < appels_you_fucking_demolished:
                with open('highscore.txt', 'w') as f:
                    f.write(str(appels_you_fucking_demolished))
    for toplefts in snake.body_parts[:-1]:
        did_snakecolide_withitself = pygame.Rect(toplefts[0], toplefts[1], 20, 20).colliderect(
            pygame.Rect(snake.body_parts[-1][0], snake.body_parts[-1][1], 20, 20))
        return did_snake_touch_corner or did_snakecolide_withitself


text_font = pygame.font.Font('font\\Pixeltype.ttf', 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_on:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                if event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'
                if event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
            if event.type == move_time:
                snake.move()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_on = True
                    direction = 'down'
                    snake.body_parts.clear()
                    snake=Snake()
                    appels_you_fucking_demolished=0
    if game_on:
        screen.fill('light blue')
        screenappel.showappel()
        snake.show_snake()
        ate = ateappel()
        if ate:
            munch.play()
            screenappel.rect.topleft = (random.randint(1, 14) * 20, random.randint(1, 14) * 20)
            ate=False
        game_on = end_game()
    else:
        if sound:
            die.play()
            sound=False
        screen.fill('light blue')
        with open('highscore.txt') as f:
            highscore = f.read()
        highscore_surf = text_font.render("high score:" + str(highscore), True, 'black')
        highscore_rect = highscore_surf.get_rect(center=(300, 450))
        screen.blit(highscore_surf, highscore_rect)
        game_name = text_font.render('snake game', True, 'black')
        game_name_surf = game_name.get_rect(center=(300, 150))
        screen.blit(game_name, game_name_surf)
        cutesnake = pygame.image.load('Graphics\\cutesnake101.png').convert_alpha()
        cutesnake_rect = cutesnake.get_rect(center=(300, 300))
        screen.blit(cutesnake, cutesnake_rect)
        game_score = text_font.render(f'last game score:{appels_you_fucking_demolished}', True, 'black')
        game_text = text_font.render('press space to play', True, 'black')
        game_score_surf = game_score.get_rect(center=(300, 500))
        game_text_surf = game_text.get_rect(center=(300, 500))

        if appels_you_fucking_demolished == 0:
            screen.blit(game_text, game_text_surf)
        else:
            screen.blit(game_score, game_score_surf)
            pll = text_font.render('press space to play again', True, 'black')
            pll_rect = game_score.get_rect(center=(250, 570))
            screen.blit(pll, pll_rect)

    pygame.display.update()

    clock.tick(60)