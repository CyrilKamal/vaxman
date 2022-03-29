# Vaxman for EA Forage (with a little attack on titan twist ;))
# https://github.com/cyrilkamal/vaxman

import pygame, sys, time
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

icon = pygame.image.load('images/levi.png')
pygame.display.set_icon(icon)

# Add music
pygame.mixer.init()
pygame.mixer.music.load('vaxman.mp3')
pygame.mixer.music.play(-1, 0.0)


# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    # This class represents the bar at the bottom that the player controls


class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, loc, filename, name):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.turn = 0
        self.steps = 0
        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = loc[1]
        self.rect.left = loc[0]
        self.prev_x = loc[0]
        self.prev_y = loc[1]

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):
        # Get the old position, in case we need to go back to it

        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        prev_y = old_y + self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


# Inheritime Player klassist
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


def duplicate(monsta_list, locs):
    new_ghost_list = []
    for ghost in monsta_list:
        image_path = 'images/' + str(ghost.name) + '.png'
        n = np.random.randint(1, 18)
        new_ghost = Ghost(locs[ghost.name], image_path, ghost.name)
        new_ghost_list.append(new_ghost)
    return new_ghost_list


directions = {"pinky": [
    [0, -30, 4],
    [15, 0, 9],
    [0, 15, 11],
    [-15, 0, 23],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 19],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 7],
    [0, 15, 3],
    [-15, 0, 19],
    [0, -15, 11],
    [15, 0, 9]
],
    "blinky": [
        [0, -15, 4],
        [15, 0, 9],
        [0, 15, 11],
        [15, 0, 3],
        [0, 15, 7],
        [-15, 0, 11],
        [0, 15, 3],
        [15, 0, 15],
        [0, -15, 15],
        [15, 0, 3],
        [0, -15, 11],
        [-15, 0, 3],
        [0, -15, 11],
        [-15, 0, 3],
        [0, -15, 3],
        [-15, 0, 7],
        [0, -15, 3],
        [15, 0, 15],
        [0, 15, 15],
        [-15, 0, 3],
        [0, 15, 3],
        [-15, 0, 3],
        [0, -15, 7],
        [-15, 0, 3],
        [0, 15, 7],
        [-15, 0, 11],
        [0, -15, 7],
        [15, 0, 5]
    ],
    "inky": [
        [30, 0, 2],
        [0, -15, 4],
        [15, 0, 10],
        [0, 15, 7],
        [15, 0, 3],
        [0, -15, 3],
        [15, 0, 3],
        [0, -15, 15],
        [-15, 0, 15],
        [0, 15, 3],
        [15, 0, 15],
        [0, 15, 11],
        [-15, 0, 3],
        [0, -15, 7],
        [-15, 0, 11],
        [0, 15, 3],
        [-15, 0, 11],
        [0, 15, 7],
        [-15, 0, 3],
        [0, -15, 3],
        [-15, 0, 3],
        [0, -15, 15],
        [15, 0, 15],
        [0, 15, 3],
        [-15, 0, 15],
        [0, 15, 11],
        [15, 0, 3],
        [0, -15, 11],
        [15, 0, 11],
        [0, 15, 3],
        [15, 0, 1],
    ],
    "clyde": [
        [-30, 0, 2],
        [0, -15, 4],
        [15, 0, 5],
        [0, 15, 7],
        [-15, 0, 11],
        [0, -15, 7],
        [-15, 0, 3],
        [0, 15, 7],
        [-15, 0, 7],
        [0, 15, 15],
        [15, 0, 15],
        [0, -15, 3],
        [-15, 0, 11],
        [0, -15, 7],
        [15, 0, 3],
        [0, -15, 11],
        [15, 0, 9],
    ]
}

L = {"pinky": len(directions["pinky"]) - 1, "blinky": len(directions["blinky"]) - 1,
     "inky": len(directions["inky"]) - 1, "clyde": len(directions["clyde"]) - 1}

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# Set the title of the window
pygame.display.set_caption('Vax-Man')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# default locations for vaxman and monstas
locations = {"vaxman": (303 - 16, (7 * 60) + 19), "blinky": (303 - 16, (3 * 60) + 19),
             "pinky": (303 - 16, (4 * 60) + 19), "inky": (303 - 16 - 32, (4 * 60) + 19),
             "clyde": (303 + (32 - 16), (4 * 60) + 19)}


def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monsta_list = pygame.sprite.RenderPlain()

    vaxman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    turn_step = {"pinky": [0, 0], "blinky": [0, 0], "inky": [0, 0], "clyde": [0, 0]}

    # Create the player paddle object
    vaxman = Player(locations["vaxman"], "images/levi.png", "vaxman")
    all_sprites_list.add(vaxman)
    vaxman_collide.add(vaxman)

    Blinky = Ghost(locations["blinky"], "images/blinky.png", "blinky")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(locations["pinky"], "images/pinky.png", "pinky")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(locations["inky"], "images/inky.png", "inky")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(locations["clyde"], "images/clyde.png", "clyde")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, vaxman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)

    score = 0

    done = False

    i = 0
    start = time.time()
    while done == False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vaxman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    vaxman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    vaxman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    vaxman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    vaxman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    vaxman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    vaxman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    vaxman.changespeed(0, -30)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        vaxman.update(wall_list, gate)
        for ghost in monsta_list:
            n = np.random.randint(4, 25)
            if n % 2 == 0:
                n = 0
            elif n % 3 == 0:
                n = 4
            ghost.turn, ghost.steps = ghost.changespeed(np.roll(directions[ghost.name], n, axis=0), ghost.name,
                                                        ghost.turn, ghost.steps, L[ghost.name])
            ghost.changespeed(directions[ghost.name], ghost.name, ghost.turn, ghost.steps, L[ghost.name])
            ghost.update(wall_list, False)

        # See if the vaxman block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(vaxman, block_list, True)

        elapsed = round(time.time() - start, 1)
        c = 0
        if elapsed % 30 == 0 and elapsed != 0:
            new_ghosts = duplicate(monsta_list, locations)
            for ghost in new_ghosts:
                monsta_list.add(ghost)

        # Check the list of collisions
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        num_ghosts = len(monsta_list.sprites())
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Score: " + str(score) + "/" + str(bll), True, red)
        ghosts = font.render("Ghosts:" + str(num_ghosts), True, red)
        screen.blit(text, [10, 10])
        screen.blit(ghosts, [450, 10])

        if score == bll:
            doNext("Congratulations, you won!", 145, all_sprites_list, block_list, monsta_list, vaxman_collide,
                   wall_list, gate)

        monsta_hit_list = pygame.sprite.spritecollide(vaxman, monsta_list, True)

        for hit_ghost in monsta_hit_list:
            monsta_list.remove(hit_ghost)
            all_sprites_list.remove(hit_ghost
                                    )
        if len(monsta_list.sprites()) >= 128:
            doNext("Game Over!", 235, all_sprites_list, block_list, monsta_list, vaxman_collide, wall_list, gate)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monsta_list, vaxman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    all_sprites_list = []
                    block_list = []
                    monsta_list = []
                    vaxman_collide = []
                    wall_list = []
                    gate = []
                    startGame()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


startGame()

pygame.quit()