import keyboard
import os
import random
import time
from utils import BOARD_WIDTH, BOARD_HEIGHT, HOLDING_PIECE_OFFSET, Pieces, PIECES_CHARS, PIECE_OPTIONS, SHAPES, SHAPE_BOXES, \
                    PREVIEW_PIECE_OFFSET, LEFT_PADDING

mem = [[PIECES_CHARS[Pieces.EMPTY.value] for i in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]

def get_random_piece(options):
    selected = random.choice(options)
    options.remove(selected)
    return selected

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

def posicionar_cursor(linha, coluna):
    print(f"\033[{linha};{coluna}H", end="")

def draw_standalone_piece(preview_piece, offset):
    # clear previews preview
    for y in range(4):
        posicionar_cursor(y + 2, offset)
        print("        ")

    preview_piece_shape = SHAPES[preview_piece]
    preview_piece_char = PIECES_CHARS[preview_piece.value]
    for prev_x, prev_y in preview_piece_shape:
        posicionar_cursor(prev_y + 2, (prev_x * 2) + offset)
        print(preview_piece_char)

def draw_tetris_board(mem):
    for i in range(BOARD_HEIGHT):
        posicionar_cursor(i + 1, LEFT_PADDING)

        linha_str = "|"
        for j in range(BOARD_WIDTH):
            char = mem[i][j]
            linha_str += char
            if char == PIECES_CHARS[Pieces.GHOST.value]:
                mem[i][j] = PIECES_CHARS[Pieces.EMPTY.value]

        linha_str += "|"
        print(linha_str)

def rotate(shape_coords, N, x, y, mem, clock_wise=True):
    new_rotated_coords = []
    for x_s, y_s in shape_coords:
        if clock_wise:
            nx = (N - 1) - y_s
            ny = x_s
        else:
            ny = (N - 1) - x_s
            nx = y_s
        new_rotated_coords.append((nx, ny))

    if is_valid_move(new_rotated_coords, x, y, mem):
        return new_rotated_coords

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

    return empty_rows + new_mem

def get_y_raycast(shape, x, y, mem):
    next_y = y
    while is_valid_move(shape,x,next_y+1,mem):
        next_y += 1
    return next_y


add_gravity_ticks = 30

shape = None

gravity_timer = 0

x,y = 0, 0
ghost_y = 0

piece_pool = PIECE_OPTIONS.copy()
get_next_piece = True
next_piece = Pieces.EMPTY
holding_piece = None
preview_piece = get_random_piece(piece_pool)
os.system("cls")

while True:
    # exit the game
    if keyboard.is_pressed('q'):
        break

    if not piece_pool:
        piece_pool = PIECE_OPTIONS.copy()

    if get_next_piece:
        next_piece = preview_piece

        preview_piece = get_random_piece(piece_pool)
        draw_standalone_piece(preview_piece, PREVIEW_PIECE_OFFSET)

        shape = SHAPES[next_piece]
        x, y = BOARD_WIDTH // 2 - 2, 0

        mem[:] = clear_complete_lines(mem)

        # check for game over
        if not is_valid_move(shape, x, y, mem):
            os.system("cls")
            print("Game Over!")
            break

        get_next_piece = False

    if keyboard.is_pressed('c'):
        draw_piece(shape, PIECES_CHARS[Pieces.EMPTY.value], x, y, mem)

        if holding_piece is None:
            holding_piece = next_piece
            get_next_piece = True
        else:
            holding_piece, next_piece = next_piece, holding_piece
            shape = SHAPES[next_piece]
            x, y = BOARD_WIDTH // 2 - 2, 0


        draw_standalone_piece(holding_piece, HOLDING_PIECE_OFFSET)

        while keyboard.is_pressed('c'):
            time.sleep(0.01)

        continue

    draw_piece(shape, PIECES_CHARS[Pieces.EMPTY.value], x, y, mem)

    new_x, new_y = x,y

    if gravity_timer >= add_gravity_ticks:
        gravity_timer = 0
        new_y += 1

    if keyboard.is_pressed('down'):
        new_y += 1
        gravity_timer = 0

    if keyboard.is_pressed('space'):
        draw_piece(shape, PIECES_CHARS[Pieces.EMPTY.value], x, y, mem)

        y = get_y_raycast(shape, x, y, mem)

        draw_piece(shape, PIECES_CHARS[next_piece.value], x, y, mem)
        get_next_piece = True

        while keyboard.is_pressed('space'):
            time.sleep(0.01)

        continue


    if new_y >= y and not is_valid_move(shape, new_x, new_y, mem):
        get_next_piece = True
    else:
        y = new_y

    if keyboard.is_pressed('right'):
        new_x += 1

    if keyboard.is_pressed('left'):
        new_x -= 1

    if keyboard.is_pressed('up'):
        shape = rotate(shape, SHAPE_BOXES[next_piece.value], new_x, new_y, mem, clock_wise=True)
    elif keyboard.is_pressed('z'):
        shape = rotate(shape, SHAPE_BOXES[next_piece.value], new_x, new_y, mem, clock_wise=False)

    if is_valid_move(shape, new_x, new_y, mem):
        x, y = new_x, new_y

    ghost_y = get_y_raycast(shape,x,y,mem)
    draw_piece(shape, PIECES_CHARS[Pieces.GHOST.value], x, ghost_y, mem)

    draw_piece(shape, PIECES_CHARS[next_piece.value], x, y, mem)
    draw_tetris_board(mem)

    gravity_timer += 1

    time.sleep(0.065)
