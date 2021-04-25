import pygame

# Settings
#   window
resolution = (400, 400)
pixel_size = 10

#   colors
red = (255, 0, 0)
lime = (75, 100, 0)
white = (255, 255, 255)

#   board
board_size = {"width": 20, "height": 20}

#   game
field_types = {"WALL": 4,
               "GROUND": 0,
               "FOOD": 1,
               "HEAD": 2,
               "TAIL": 3}

#   snake
snake_starting_length = 3

# game_data
#   board
board_data = []

#   metrics
directions = ("right", "left", "up", "down")

#   snake
snake_position = [{"x": 0, "y": 0}]
head_direction = directions[0]


def main():
    window = init()

    game_over = False
    while not game_over:
        draw(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

    pygame.quit()
    quit()


def init():
    pygame.init()
    init_game()
    return init_window()


def init_window():
    return pygame.display.set_mode(resolution)


def init_game():
    init_board()


def init_board():
    board_width = board_size["width"]
    board_height = board_size["height"]

    # position and create snake
    snake_position[0]["x"] = int(board_width / 2)
    snake_position[0]["y"] = int(board_height / 2)
    snake_head_position_x = snake_position[0]["x"]
    snake_head_position_y = snake_position[0]["y"]

    for i in range(snake_starting_length):
        snake_position.append({"x": snake_head_position_x + i + 1, "y": snake_head_position_y})

    # calculate start_positions

    # set positions of elements like, walls, the snake and the food
    for x in range(board_width):
        tile_data = []
        board_data.append(tile_data)
        for y in range(board_height):
            # Wände
            if x % (board_width - 1) is 0 or y % (board_height - 1) is 0:
                tile_data.append(field_types["WALL"])
            # Kopf
            elif x is snake_head_position_x and y is snake_head_position_y:
                tile_data.append(field_types["HEAD"])
            else:
                # Boden
                tile_data.append(0)

    # Schwanz
    for i in range(1, len(snake_position)):
        body_part = snake_position[i]
        board_data[body_part["x"]][body_part["y"]] = field_types["TAIL"]


def which_body_part_is_overlapping(position: (int, int)):
    for body_part_position in snake_position:
        if position is body_part_position["x"] and position is body_part_position["y"]:
            return position
    return -1, -1


def is_position_overlapping_with_snake(position: (int, int)):
    if which_body_part_is_overlapping(position)[0] is not -1:
        return True
    return False


def draw(window):
    for x, row in enumerate(board_data):
        for y, tile in enumerate(row):
            color = "NONE"
            if tile is field_types["HEAD"]:
                color = red
            elif tile is field_types["TAIL"]:
                color = lime
            elif tile is field_types["WALL"]:
                color = white

            if color != "NONE":
                pygame.draw.rect(window, color, [x * pixel_size, y * pixel_size, pixel_size, pixel_size])


main()