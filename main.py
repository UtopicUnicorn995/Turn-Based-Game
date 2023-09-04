import pygame
import random

clock = pygame.time.Clock()
fps = 60

# game window
pygame.init()
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Battle")

# define game variables
current_fighter = 1
total_figthers = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False

# define fonts
font = pygame.font.SysFont("Times New Roman", 26)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)

# load images
# background image
background_img = pygame.image.load("img/Background/background.png").convert_alpha()
panel_img = pygame.image.load("img/Icons/panel.png").convert_alpha()
# function for drawing bg

# sword image
sword_img = pygame.image.load("img/Icons/sword.png").convert_alpha()


# Create function for drawing text
def draw_text(text, font, text_color, x_cor, y_cor):
    img = font.render(text, True, text_color)
    screen.blit(img, (x_cor, y_cor))


def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_panel():
    # draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # show knight stats
    draw_text(
        f"{knight.name} HP: {knight.hp}",
        font,
        red,
        100,
        screen_height - bottom_panel + 10,
    )
    for count, i in enumerate(bandit_list):
        # show name and health
        draw_text(
            f"{i.name} HP: {i.hp}",
            font,
            red,
            550,
            (screen_height - bottom_panel + 10) + count * 60,
        )


# fighter class
class Fighter:
    def __init__(self, x_cor, y_cor, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:death
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"img/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x_cor, y_cor)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enought time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # if the animation has run out, reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        # set variables to attack animatin
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False

        # set variables to attack animatin
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar:
    def __init__(self, x_cor, y_cor, hp, max_hp):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp

        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x_cor, self.y_cor, 150, 20))
        pygame.draw.rect(screen, green, (self.x_cor, self.y_cor, 150 * ratio, 20))


knight = Fighter(200, 260, "Knight", 30, 10, 3)
bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit_list = []

bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(
    100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp
)

bandit1_health_bar = HealthBar(
    550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp
)

bandit2_health_bar = HealthBar(
    550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp
)


game_on = True

while game_on:
    clock.tick(fps)

    # Draw bg
    # run draw bg function
    draw_bg()

    # draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    # draw fighters
    knight.update()
    knight.draw()

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    # control player actions
    # reset action variables
    attack = False
    potion = False
    target = None
    # make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            # hide mouse
            pygame.mouse.set_visible(False)
            # Show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True:
                attack = True
                target = bandit_list[count]

    # Player action
    if knight.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action
                # attack
                if attack == True and target != None:
                    knight.attack(target)
                    current_fighter += 1
                    action_cooldown = 0

    # Enemy action
    for count, bandit in enumerate(bandit_list):
        if current_fighter == 2 + count:
            if bandit.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    bandit.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

    # if all fighters have had a turn, reset
    if current_fighter > total_figthers:
        current_fighter = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()


pygame.quit()
