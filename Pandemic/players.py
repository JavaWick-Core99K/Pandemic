import pygame
import random


class Character:
    def __init__(self, pos, img_name, pos_change=64):
        self.x = pos[0]
        self.y = pos[1]
        self.change = pos_change
        self.previous_locations = []

        self.frozen = False
        self.moves_before_unfreeze = 1

        self.jump = False

        self.img = pygame.image.load(img_name)

    def get_location(self):
        loc = (self.x, self.y)
        return loc

    def set_location(self, loc):
        self.x = loc[0]
        self.y = loc[1]

    def save_location(self):
        self.previous_locations.append(self.get_location())

    def to_last_location(self):
        self.set_location(self.previous_locations[-1])

    def up(self, m=1):
        self.y -= self.change * m

    def down(self, m=1):
        self.y += self.change * m

    def left(self, m=1):
        self.x -= self.change * m

    def right(self, m=1):
        self.x += self.change * m

    def move(self, pX, pY):
        if self.frozen:
            return None

        direction = random.choice(("x", "y"))
        m = 1

        if direction == "x":
            if self.x < pX:
                self.right(m)
            elif self.x > pX:
                self.left(m)
        else:
            if self.y < pY:
                self.down(m)
            elif self.y > pY:
                self.up(m)

    def activate_jump(self):
        self.jump = True

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        if self.frozen:
            if self.moves_before_unfreeze > 0:
                self.moves_before_unfreeze -= 1
            else:
                self.frozen = False
                self.moves_before_unfreeze = 1

    def pos_multiplier(self):
        m = 2 if self.jump else 1
        self.jump = False
        return m

    def addenemy(self, enemy_list, location):
        enemy_list.append(Enemy(location, "enemy.png"))

    def create_wall(self, wall_list):
        wall_img = pygame.image.load('wall.png')
        wall_location = self.get_location()
        wall = {"img": wall_img, "location": wall_location}
        wall_list.append(wall)

    def undo_move(self, steps):
        """
        undo one move of the AI
        :return:
        """
        self.set_location(self.previous_locations[-steps])


class Enemy(Character):
    def __init__(self, pos, img_name, rapid=False):
        super().__init__(pos, img_name)
        self.is_rapid = rapid

    def randx(self):
        self.change = random.choice((8, -8))
        self.x += self.change

    def randy(self):
        self.change = random.choice((8, -8))
        self.y += self.change


class Player(Character):
    pass


