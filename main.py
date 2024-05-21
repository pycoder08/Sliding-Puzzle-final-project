import pygame
import random

########################################

########################################
# Variable setup

tile_size = 80  # size of the tiles
origin = 50  # where the start of the board will be drawn

# length and height of the game window
window_width = 1024
window_height = 600

fps = 60  # frames per second value

blank = None

# Color variables

black = (0, 0, 0)  # 0 red, blue, and green

white = (255, 255, 255)  # maximum red, blue, and green

dark_blue = (3, 54, 73)  # 3 red, 54 green, 73 blue

green = (141, 220, 164)  # 0 red/blue, origin0 green

background_color = dark_blue

Tile_color = green

# Formatting
pygame.font.init()

class Game:  # creates the class 'Game'
    def __init__(self):  # creates the object 'self' within the class 'Game'
        pygame.init()  # initiates all modules within the pygame library
        self.screen = pygame.display.set_mode(
            (window_width, window_height))  # defines the instance variable self.screen as the pygame display window
        pygame.display.set_caption("Sliding Puzzle - CS 101 Final Project")
        self.clock = pygame.time.Clock()  # defines an instance variable as a pygame object that can keep track of time
        self.all_sprites = pygame.sprite.Group()
        self.board_size = 4
        self.unsolved = True

    def new(self):  # a method that will create a new game board when called
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.starting_grid = self.create_game()
        self.winning_grid = self.create_game()
        self.white_grid = self.create_game()
        self.buttons_list = []
        self.buttons_list.append(Button(470, 50, 200, 50, "Shuffle", white, black))
        self.buttons_list.append(Button(470, 120, 200, 50, "Solve", white, black))
        self.buttons_list.append(Button(470, 190, 50, 50, "3x", white, black))
        self.buttons_list.append(Button(545, 190, 50, 50, "4x", white, black))
        self.buttons_list.append(Button(620, 190, 50, 50, "5x", white, black))
        self.shuffle()
        while self.check_win():
            self.shuffle()
        self.draw_tiles()


    def shuffle(self):
        for a in (1, 20):
            while True:
                length_list = []
                for i in range(1, self.board_size):
                    length_list.append(i)

                # Initialize the grid with the winning configuration
                self.tiles_grid = self.create_game()

                # Shuffle the tiles
                for row in length_list:
                    for column in length_list:
                        rand_loc_x = random.randint(0, self.board_size - 1)
                        rand_loc_y = random.randint(0, self.board_size - 1)
                        if ((rand_loc_x == self.board_size - 1 and rand_loc_y) or (row and column) == self.board_size - 1):
                             pass
                        else:
                            self.tiles_grid[row][column], self.tiles_grid[rand_loc_x][rand_loc_y] = self.tiles_grid[rand_loc_x][rand_loc_y], self.tiles_grid[row][column]

                # Check if the shuffled board is solvable
                if self.is_solvable(self.tiles_grid) and not self.check_win() :
                    break



    def is_solvable(self, grid):
        inversion_count = 0
        for i in range(self.board_size * self.board_size - 1):
            for j in range(i + 1, self.board_size * self.board_size):
                if grid[j // self.board_size][j % self.board_size] and grid[i // self.board_size][i % self.board_size] and grid[i // self.board_size][i % self.board_size] > grid[j // self.board_size][j % self.board_size]:
                    inversion_count += 1

        # For even grid sizes, adjust the inversion count if necessary
        if self.board_size % 2 == 0:
            blank_row = 0
            for i in range(self.board_size):
                if grid[i][-1] == 0:
                    blank_row = i
                    break
            if blank_row % 2 == 0:
                inversion_count += blank_row
            else:
                inversion_count += self.board_size - blank_row - 1

        # The grid is solvable if inversion count is even
        return inversion_count % 2 == 0

    def create_game(self):
        grid = [[x + y * self.board_size for x in range(1, self.board_size + 1)] for y in range(self.board_size)]
        grid[-1][-1] = 0
        return grid

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for column, tile in enumerate(x):
                if tile != 0:
                    if self.tiles_grid[row][column] == self.starting_grid[row][column]:
                        self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), green))
                    else:
                        self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), white))
                else:
                    self.tiles[row].append(
                        Tile(self, column + (origin / tile_size), row + (origin / tile_size), "empty", background_color))

    def draw_winning_tiles(self):
        self.green_tiles = []
        for row, x in enumerate(self.winning_grid):
            self.green_tiles.append([])
            for column, tile in enumerate(x):
                if tile != 0:
                    self.green_tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), green))
                else:
                    self.green_tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), "empty", background_color))

    def draw_white_tiles(self):
        self.white_tiles = []

        for row, x in enumerate(self.tiles_grid):
            self.white_tiles.append([])
            for column, tile in enumerate(x):
                if tile != 0:
                    self.white_tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), green))
                else:
                    self.white_tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), "empty", background_color))


    def play(self):  # a method that will run the game
        self.playing = True  # defines the instance variable 'self.playing' as true
        while self.playing:  # while the game is being run
            self.clock.tick(fps)  # start counting
            self.events()  # calls on methods that will be defined later
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(origin, (self.board_size * tile_size) + tile_size + origin,
                         tile_size):  # a range from -1 to the product of self.board_size * tile_size, with an increment of tile_size
            pygame.draw.line(self.screen, black, (row, origin), (row, (self.board_size * tile_size) + origin))
        for column in range(origin, (self.board_size * tile_size) + tile_size + origin, tile_size):
            pygame.draw.line(self.screen, black, (origin, column), ((self.board_size * tile_size) + origin, column))

    def draw(self):
        self.screen.fill(background_color)  # fills the screen with the background color (dark blue)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        if self.check_win():
            self.display_winning_message()
        pygame.display.flip()  # updates the display

    def display_winning_message(self):
        # Fill only the board area with the background color
        pygame.draw.rect(self.screen, green,(origin, origin, self.board_size * tile_size + 1, self.board_size * tile_size + 1))
        # Draw the winning message in the center of the board area
        font = pygame.font.SysFont("rockwell", 17 * self.board_size)
        text_surface = font.render("You Win!", True, black)
        text_rect = text_surface.get_rect(
            center=(origin + (self.board_size * tile_size) // 2, origin + (self.board_size * tile_size) // 2))
        self.screen.blit(text_surface, text_rect)

    def events(self):  # a method that checks for events that are happening in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the player quits the game:
                pygame.quit()  # de-initialize all pygame modules
                quit(0)  # quits the program

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for column, tile in enumerate(tiles):

                        if tile.click(mouse_x, mouse_y):

                            if column + 1 < self.board_size and (tile.right() and self.tiles_grid[row][column + 1] == 0):
                                self.tiles_grid[row][column], self.tiles_grid[row][column + 1] = self.tiles_grid[row][column + 1], self.tiles_grid[row][column]

                            elif tile.left() and self.tiles_grid[row][column - 1] == 0:
                                self.tiles_grid[row][column], self.tiles_grid[row][column - 1] = self.tiles_grid[row][column - 1], self.tiles_grid[row][column]

                            elif row + 1 < self.board_size and (tile.down() and self.tiles_grid[row + 1][column] == 0):
                                self.tiles_grid[row][column], self.tiles_grid[row + 1][column] = self.tiles_grid[row + 1][column], self.tiles_grid[row][column]

                            elif tile.up() and self.tiles_grid[row - 1][column] == 0:
                                self.tiles_grid[row][column], self.tiles_grid[row - 1][column] = self.tiles_grid[row - 1][column], self.tiles_grid[row][column]
                            self.draw_tiles()

                        if self.check_win():
                            pass



                    for button in self.buttons_list:
                        if button.click(mouse_x, mouse_y):
                            if button.text == "Shuffle":
                                self.shuffle()
                                self.draw_tiles()

                            if button.text == "Solve":
                                self.tiles_grid = self.winning_grid
                                self.draw_tiles()

                            if button.text == "3x":
                                self.board_size = 3
                                self.create_game()
                                self.new()
                                self.play()
                                self.update()
                                self.draw_tiles()
                                self.shuffle()


                            if button.text == "4x":
                                self.board_size = 4
                                self.create_game()
                                self.new()
                                self.play()
                                self.update()
                                self.draw_tiles()
                                self.shuffle()

                            if button.text == "5x":
                                self.board_size = 5
                                self.create_game()
                                self.new()
                                self.play()
                                self.update()
                                self.draw_tiles()
                                self.shuffle()


    def check_win(self):
        if self.tiles_grid == self.starting_grid:
            self.unsolved = False
            return True
        return False



class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, color):
        self.groups = self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((tile_size, tile_size))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("rockwell", 50)
            font_surface = self.font.render(self.text, True, black)
            self.image.fill(color)
            self.font_size = self.font.size(self.text)
            draw_x = (tile_size / 2) - self.font_size[0] / 2
            draw_y = (tile_size / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(background_color)

    def update(self):
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + tile_size < self.game.board_size * tile_size

    def left(self):
        return self.rect.x - tile_size >= 0

    def up(self):
        return self.rect.y - tile_size >= 0

    def down(self):
        return self.rect.y + tile_size < self.game.board_size * tile_size

    def change_color(self, color):
        if self.text != "empty":
            font_surface = self.font.render(self.text, True, black)
            self.image.fill(color)
            draw_x = (tile_size / 2) - self.font_size[0] / 2
            draw_y = (tile_size / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))


class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.color = color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.draw(game.screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("rockwell", 30)
        text = font.render(self.text, True, self.text_color)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))


    def click(self, mouse_x, mouse_y):
     return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height



game = Game()
while True:
    game.new()
    game.play()
    game.clock.tick(60)
    print(game.clock)


game = Game()
while True:
    game.new()
    game.play()
    game.clock.tick(60)
    print(game.clock)