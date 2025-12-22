import keyboard
import os
import random
import time
from utils import BOARD_WIDTH, BOARD_HEIGHT, Pieces, PIECES_CHARS, PIECE_OPTIONS, SHAPES, SHAPE_BOXES

mem = [[PIECES_CHARS[Pieces.EMPTY.value] for i in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

def get_random_piece(options):
    return random.choice(options)


def is_valid_move(shape, x, y, mem):
    for x_draw, y_draw in shape:
        nx = x + x_draw
        ny = y + y_draw
        if nx < 0 or nx >= BOARD_WIDTH or ny >= BOARD_HEIGHT:
            return False
        if mem[ny][nx] != PIECES_CHARS[Pieces.EMPTY.value]:
            return False
    return True

def draw_piece(shape, char, x, y, mem):
    for x_draw, y_draw in shape:
        target_y = y + y_draw
        target_x = x + x_draw
        if 0 <= target_y < BOARD_HEIGHT and 0 <= target_x < BOARD_WIDTH:
            mem[target_y][target_x] = char

def draw_tetris_board(mem):
    tetris_board = ""
    for i in range(BOARD_HEIGHT):
        tetris_board += "|"
        for j in range(BOARD_WIDTH):
            tetris_board += mem[i][j]
        tetris_board += "|"
        tetris_board += "\n"
    return tetris_board

def rotate(shape_coords, N, x, y, mem):
    new_rotated_coords = []
    for x_s, y_s in shape_coords:
        nx = (N - 1) - y_s
        ny = x_s
        new_rotated_coords.append((nx, ny))

    min_x = min(p[0] for p in new_rotated_coords)
    min_y = min(p[1] for p in new_rotated_coords)

    candidate_shape = []
    for x_s, y_s in new_rotated_coords:
        candidate_shape.append((x_s - min_x, y_s - min_y))

    if is_valid_move(candidate_shape, x, y, mem):
        return candidate_shape
    else:
        return shape_coords

def clear_complete_lines(mem):
    new_mem = []
    for i in range(BOARD_HEIGHT):
        is_complete = True
        for j in range(BOARD_WIDTH):
            if mem[i][j] == PIECES_CHARS[Pieces.EMPTY.value]:
                is_complete = False
                break

        if not is_complete:
            new_mem.append(list(mem[i]))

    lines_cleared = BOARD_HEIGHT - len(new_mem)

    empty_rows = [[PIECES_CHARS[Pieces.EMPTY.value] for _ in range(BOARD_WIDTH)] for _ in range(lines_cleared)]

    return new_mem, empty_rows



get_next_piece = True
next_piece = Pieces.EMPTY

activate_rotate = False
add_gravity_ticks = 30

shape = None

gravity_timer = 0

x = 0
y = 0

os.system("cls")
while True:
    # exit the game
    if keyboard.is_pressed('q'):
        break

    if get_next_piece:
        next_piece = get_random_piece(PIECE_OPTIONS)
        get_next_piece = False
        shape = SHAPES[next_piece]
        x, y = BOARD_WIDTH // 2 - 2, 0

        new_mem, empty_rows = clear_complete_lines(mem)
        mem[:] = empty_rows + new_mem


    draw_piece(shape, PIECES_CHARS[Pieces.EMPTY.value], x, y, mem)

    new_x, new_y = x,y

    if gravity_timer >= add_gravity_ticks:
        gravity_timer = 0
        new_y += 1

    if keyboard.is_pressed('down'):
        new_y += 1

    if new_y >= y and not is_valid_move(shape, new_x, new_y, mem):
        get_next_piece = True
    else:
        y = new_y

    if keyboard.is_pressed('up'):
        activate_rotate = True

    if keyboard.is_pressed('right'):
        new_x += 1

    if keyboard.is_pressed('left'):
        new_x -= 1

    if activate_rotate:
        shape = rotate(shape, SHAPE_BOXES[next_piece.value], x, y, mem)

    if is_valid_move(shape, new_x, new_y, mem):
        x, y = new_x, new_y

    draw_piece(shape, PIECES_CHARS[next_piece.value], x, y, mem)

    ASCII_TETRIS_BOARD = draw_tetris_board(mem)

    print("\033[H", end="")

    print(ASCII_TETRIS_BOARD)
    activate_rotate = False

    gravity_timer += 1

    time.sleep(0.065)
