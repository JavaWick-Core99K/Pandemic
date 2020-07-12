import pygame
import math
import sys
import random
from players import Enemy
from players import Player


def random_position():
    x = random.choice(list(range(64, 897, 64)))
    y = random.choice(list(range(64, 897, 64)))
    pos = (x, y)
    return pos


# Initialize the game
pygame.init()

# Setup screen size
screen = pygame.display.set_mode((960, 960))

# Title and icon
pygame.display.set_caption("Pandemic")
icon = pygame.image.load('display_icon.png')
pygame.display.set_icon(icon)

# Start up page
start_page = pygame.image.load('start_page.png')
start_button = pygame.image.load('start_button.png')

# Create the player
player = Player(random_position(), "player.png")

# Create enemy
enemies = [Enemy(random_position(), "enemy.png")]
walls = []
multiplied = False

# pixel grid
pix = pygame.image.load('grid_pix.png')

# player lives
lives1 = pygame.image.load("heart.png")
lives2 = pygame.image.load("heart.png")
lives3 = pygame.image.load("heart.png")
count_hearts = 3

# set up goal for round and position
win = pygame.image.load("hole.png")
winPos = random_position()
winX = winPos[0]
winY = winPos[1]

end_goal = pygame.image.load("vaccine.png")
end_pos = random_position()
end_goalX = end_pos[0]
end_goalY = end_pos[1]

# settings and levels
game_over = False
lvl1 = True
lvl2 = False
lvl3 = False
lvl4 = False
lvl5 = False

# power up image loads
undo_one = pygame.image.load("undo_one.png")
undo_two = pygame.image.load("undo_two.png")
wall = pygame.image.load("wall.png")
water = pygame.image.load("water.png")
face_mask = pygame.image.load("face_mask.png")

power_ups = [{"img": undo_one, "location": random_position(), "name": "undo_1"},
             {"img": undo_two, "location": random_position(), "name": "undo_2"}]


def render_player():
    screen.blit(player.img, (player.x, player.y))


def render_enemy():
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))


def render_walls():
    for w in walls:
        screen.blit(w["img"], w["location"])


def render_power_ups():
    for p in power_ups:
        screen.blit(p["img"], p["location"])


def save_enemy_locations():
    for e in enemies:
        e.save_location()


def move_enemy():
    for e in enemies:
        e.move(player.x, player.y)


def rapid_enemy():
    for e in enemies:
        if e.is_rapid:
            e.randx()
            e.randy()


def reset_position():
    start_player = (128, 320)
    start_enemy = (896, 896)
    player.set_location(start_player)
    for e in enemies:
        e.set_location(start_enemy)


def reset_random_position():
    start_player = random_position()
    start_enemy = random_position()
    player.set_location(start_player)
    for e in enemies:
        e.set_location(start_enemy)

    for p in power_ups:
        p["location"] = random_position()


def collided():
    for e in enemies:
        distance = math.hypot(e.x - player.x, e.y - player.y)
        if distance <= 10:
            return True
    return False


# checks if player and goal collided
def next_lvl():
    if lvl5:
        distance = math.hypot(end_goalX - player.x, end_goalY - player.y)
    else:
        distance = math.hypot(winX - player.x, winY - player.y)
    if distance <= 10:
        return True
    return False


def three_power_ups():
    global power_ups
    power_ups = [{"img": undo_one, "location": random_position(), "name": "undo_1"},
                 {"img": undo_two, "location": random_position(), "name": "undo_2"},
                 {"img": water, "location": random_position(), "name": "water"}]


def four_power_ups():
    global power_ups
    power_ups = [{"img": undo_one, "location": random_position(), "name": "undo_1"},
                 {"img": undo_two, "location": random_position(), "name": "undo_2"},
                 {"img": water, "location": random_position(), "name": "water"},
                 {"img": face_mask, "location": random_position(), "name": "face_mask"}]


def activate_power_ups():
    for p in power_ups:
        if p["location"] == player.get_location():
            if p["name"] == "undo_1":
                for e in enemies:
                    e.undo_move(2)
            elif p["name"] == "undo_2":
                for e in enemies:
                    e.undo_move(4)
            elif p["name"] == "water":
                for e in enemies:
                    e.freeze()
            elif p["name"] == "face_mask":
                player.activate_jump()
            power_ups.remove(p)


def boundary():
    if player.x > 896:
        player.left()
    elif player.x < 0:
        player.right()

    if player.y > 896:
        player.up()
    elif player.y < 0:
        player.down()

    for e in enemies:
        if e.x > 896:
            e.left()
        elif e.x < 0:
            e.right()

        if e.y > 896:
            e.up()
        elif e.y < 0:
            e.down()


def wall_boundary():
    for w in walls:
        if w["location"] == player.get_location():
            player.to_last_location()
            return True
    return False


def grid():
    for x in range(0, 960, 64):
        for y in range(961):
            screen.blit(pix, (x, y))
    for y in range(0, 960, 64):
        for x in range(961):
            screen.blit(pix, (x, y))


start = True
while start:
    screen.blit(start_page, (0, 0))
    screen.blit(start_button, (100, 400))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

# Create a while loop
running = True
while running:
    # Background
    screen.fill((100, 100, 100))
    grid()

    # load goal
    if lvl5:
        screen.blit(end_goal, (end_goalX, end_goalY))
        rapid_enemy()

        if not multiplied:
            enemies.append(Enemy(random_position(), "enemy.png", True))
            enemies.append(Enemy(random_position(), "enemy.png", True))
            enemies.append(Enemy(random_position(), "enemy.png", True))
            enemies.append(Enemy(random_position(), "enemy.png", True))
            enemies.append(Enemy(random_position(), "enemy.png", True))
            enemies.append(Enemy(random_position(), "enemy.png", True))
            multiplied = True

    else:
        screen.blit(win, (winX, winY))

    if lvl3 and not multiplied:
        enemies.append(Enemy(random_position(), "enemy.png"))
        enemies.append(Enemy(random_position(), "enemy.png"))
        multiplied = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke events
        if event.type == pygame.KEYDOWN:
            player.save_location()

            if event.key == pygame.K_a:
                player.left(player.pos_multiplier())
                save_enemy_locations()

            elif event.key == pygame.K_d:
                player.right(player.pos_multiplier())
                save_enemy_locations()

            elif event.key == pygame.K_w:
                player.up(player.pos_multiplier())
                save_enemy_locations()

            elif event.key == pygame.K_s:
                player.down(player.pos_multiplier())
                save_enemy_locations()

            elif event.key == pygame.K_SPACE:
                player.create_wall(walls)

            if not wall_boundary():
                move_enemy()

                for e in enemies:
                    e.unfreeze()

                if lvl4:
                    num = random.choice(list(range(1, 11)))
                    if num <= 3:
                        enemy = random.choice(enemies)
                        enemy.create_wall(walls)

        # unpressed keystroke events
        if event.type == pygame.KEYUP:
            pass

    boundary()
    render_player()
    render_enemy()
    render_walls()
    activate_power_ups()

    if lvl1:
        # checks if player interacted with goal
        if next_lvl():
            reset_random_position()
            lvl2 = True
            lvl1 = False
    elif lvl2:
        render_power_ups()
        # checks if player interacted with goal
        if next_lvl():
            reset_random_position()

            three_power_ups()

            lvl3 = True
            lvl2 = False
    elif lvl3:
        render_power_ups()
        # checks if player interacted with goal
        if next_lvl():
            del enemies[-2:]
            multiplied = False

            reset_random_position()
            four_power_ups()

            lvl3 = False
            lvl4 = True
    elif lvl4:
        render_power_ups()
        # checks if player interacted with goal
        if next_lvl():
            reset_random_position()
            four_power_ups()

            lvl4 = False
            lvl5 = True
    else:
        render_power_ups()

        # checks if player interacted with goal
        if next_lvl():
            game_win = True
            game_win_image = pygame.image.load('winner.png')
            while game_win:
                screen.blit(game_win_image, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = False
                        sys.exit()
                pygame.display.update()

    if collided():
        print('You died from touching the enemy')
        reset_position()
        count_hearts -= 1

    if count_hearts == 0:
        game_over = True
        game_over_image = pygame.image.load('gameover.png')
        while game_over:

            screen.blit(game_over_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False
                    sys.exit()

            pygame.display.update()

    elif count_hearts == 1:
        screen.blit(lives1, (10, 20))
    elif count_hearts == 2:
        screen.blit(lives1, (10, 20))
        screen.blit(lives2, (80, 20))
    else:
        screen.blit(lives1, (10, 20))
        screen.blit(lives2, (80, 20))
        screen.blit(lives3, (150, 20))

    # checks if player interacted with goal
    if next_lvl():
        print("You win")

    # update the display !!required
    pygame.display.update()
