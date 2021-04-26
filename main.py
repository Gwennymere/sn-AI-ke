import pygame
import time

# Settings
#   window
resolution = (400, 400)
pixel_size = 10

#   colors
red = (255, 0, 0)
lime = (75, 100, 0)
white = (255, 255, 255)
black = (0, 0, 0)

#   board
board_size = {"width": 20, "height": 20}

#   game
field_types = {"WALL": 4,
               "GROUND": 0,
               "FOOD": 1,
               "HEAD": 2,
               "TAIL": 3}
directions = {"right": 0,
              "left": 1,
              "up": 2,
              "down": 3}
game_speed = 0.5

#   snake
snake_starting_length = 3

# game_data
#   board
board_data = []

#   metrics
game_over = False

#   snake
snake_position = [{"x": 0, "y": 0}]
snake_direction = directions["left"]
snake_last_direction = snake_direction


def main():
    window = init()

    time_last_update = time.time()
    time_game_start = time_last_update

    total_updates = 0
    while not game_over:
        time_to_next_update = time_last_update - time_game_start - total_updates * game_speed
        event_handling()
        if time_to_next_update >= 0:
            game_update()
            total_updates += 1
            log_grid()
        draw(window)
        pygame.display.update()
        time_last_update = time.time()

    pygame.quit()
    quit()


def init():
    pygame.init()
    init_game()
    return init_window()


def init_window():
    return pygame.display.set_mode(resolution)


def init_game():
    init_snake()
    init_board()


def init_board():
    board_width = board_size["width"]
    board_height = board_size["height"]

    # set positions of elements like, walls, the snake and the food
    for x in range(board_width):
        tile_data = []
        board_data.append(tile_data)
        for y in range(board_height):
            # Wände
            if x % (board_width - 1) is 0 or y % (board_height - 1) is 0:
                tile_data.append(field_types["WALL"])
            else:
                # Boden
                tile_data.append(0)

    # Snake
    add_snake_to_board()


def init_snake():
    board_width = board_size["width"]
    board_height = board_size["height"]

    # position and create snake
    snake_position[0]["x"] = int(board_width / 2)
    snake_position[0]["y"] = int(board_height / 2)
    snake_head_position_x = snake_position[0]["x"]
    snake_head_position_y = snake_position[0]["y"]

    for i in range(snake_starting_length):
        snake_position.append({"x": snake_head_position_x + i + 1, "y": snake_head_position_y})


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
    pygame.draw.rect(window, black, [0, 0, board_size["width"] * pixel_size, board_size["height"] * pixel_size])
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


def game_update():
    snake_move()


def snake_move():
    clear_snake_from_board()
    global snake_last_direction

    if snake_direction == directions["left"]:
        snake_move_to((snake_position[0]["x"] - 1, snake_position[0]["y"]))
    elif snake_direction == directions["right"]:
        snake_move_to((snake_position[0]["x"] + 1, snake_position[0]["y"]))
    elif snake_direction == directions["up"]:
        snake_move_to((snake_position[0]["x"], snake_position[0]["y"] - 1))
    elif snake_direction == directions["down"]:
        snake_move_to((snake_position[0]["x"], snake_position[0]["y"] + 1))
    snake_last_direction = snake_direction

    add_snake_to_board()


def snake_move_to(tile: (int, int)):
    last_element = len(snake_position) - 1
    snake_position[last_element] = {"x": tile[0], "y": tile[1]}
    snake_position.insert(0, snake_position.pop(last_element))


def clear_snake_from_board():
    for body_part in snake_position:
        board_data[body_part["x"]][body_part["y"]] = 0


def add_snake_to_board():
    for i in range(len(snake_position)):
        body_part = snake_position[i]
        if i is 0:
            board_data[body_part["x"]][body_part["y"]] = field_types["HEAD"]
        else:
            board_data[body_part["x"]][body_part["y"]] = field_types["TAIL"]


def event_handling():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global game_over
            game_over = True
        if event.type == pygame.KEYUP:
            global snake_direction
            if event.key == pygame.K_a and snake_last_direction is not directions["right"]:
                snake_direction = directions["left"]
            elif event.key == pygame.K_d and snake_last_direction is not directions["left"]:
                snake_direction = directions["right"]
            elif event.key == pygame.K_w and snake_last_direction is not directions["down"]:
                snake_direction = directions["up"]
            elif event.key == pygame.K_s and snake_last_direction is not directions["up"]:
                snake_direction = directions["down"]


def log_grid():
    for row in enumerate(board_data):
        print(row)


main()
