import pygame
import time
import random

# Settings
#   window
resolution = (400, 400)
pixel_size = 10

#   colors
red = (255, 0, 0)
orange = (255, 165, 0)
lime = (75, 100, 0)
white = (255, 255, 255)
black = (0, 0, 0)

#   board
board_size = {"width": 20, "height": 20}

#   game
tile_types = {"WALL": 4,
              "GROUND": 0,
              "FOOD": 1,
              "HEAD": 2,
              "TAIL": 3}
directions = {"right": 0,
              "left": 1,
              "up": 2,
              "down": 3}
game_speed = 0.2

#   snake
snake_starting_length = 3

# game_data
#   board
board_data = []

#   metrics
game_over = False
food_was_eaten = True

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
    reset_game_state()
    init_snake()
    init_board()
    spawn_food()


def reset_game_state():
    global snake_direction
    global snake_last_direction
    global board_data
    global food_was_eaten
    snake_direction = directions["left"]
    snake_last_direction = snake_direction
    board_data = []
    food_was_eaten = True


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
                tile_data.append(tile_types["WALL"])
            else:
                # Boden
                tile_data.append(0)

    # Snake
    add_snake_to_board()


def init_snake():
    global snake_position
    snake_position = [{"x": 0, "y": 0}]

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
            if tile is tile_types["HEAD"]:
                color = orange
            elif tile is tile_types["TAIL"]:
                color = lime
            elif tile is tile_types["WALL"]:
                color = white
            elif tile is tile_types["FOOD"]:
                color = red

            if color != "NONE":
                pygame.draw.rect(window, color, [x * pixel_size, y * pixel_size, pixel_size, pixel_size])


def game_update():
    snake_update()
    if food_was_eaten:
        spawn_food()


def snake_update():
    clear_snake_from_board()
    global snake_last_direction

    snake_head = snake_position[0]

    if snake_direction == directions["left"]:
        snake_check_tile((snake_head["x"] - 1, snake_head["y"]))
    elif snake_direction == directions["right"]:
        snake_check_tile((snake_head["x"] + 1, snake_head["y"]))
    elif snake_direction == directions["up"]:
        snake_check_tile((snake_head["x"], snake_head["y"] - 1))
    elif snake_direction == directions["down"]:
        snake_check_tile((snake_head["x"], snake_head["y"] + 1))
    snake_last_direction = snake_direction

    add_snake_to_board()


def snake_check_tile(tile: (int, int)):
    tile_type = board_data[tile[0]][tile[1]]
    if tile_type is tile_types["FOOD"]:
        snake_eat(tile)
    elif tile_type is tile_types["GROUND"]:
        snake_move(tile)
    elif tile_type >= tile_types["TAIL"]:
        init_game()


def snake_move(tile: (int, int)):
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
            board_data[body_part["x"]][body_part["y"]] = tile_types["HEAD"]
        else:
            board_data[body_part["x"]][body_part["y"]] = tile_types["TAIL"]


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


def spawn_food():
    global food_was_eaten
    while food_was_eaten:
        food_x = random.randint(0, board_size["width"] - 1)
        food_y = random.randint(0, board_size["height"] - 1)

        if board_data[food_x][food_y] is 0:
            board_data[food_x][food_y] = tile_types["FOOD"]
            food_was_eaten = False


def snake_eat(tile: (int, int)):
    global food_was_eaten
    food_was_eaten = True
    snake_position.insert(0, {"x": tile[0], "y": tile[1]})


main()
