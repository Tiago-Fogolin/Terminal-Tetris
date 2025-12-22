from enum import Enum

VERMELHO = '\033[31m'
VERDE = '\033[32m'
AZUL = '\033[34m'
AMARELO = '\033[33m'
ROXO = '\033[35m'
LARANJA = '\033[38;5;208m'
ROSA = '\033[38;5;201m'
RESET = '\033[0m'

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

class Pieces(Enum):
    EMPTY = 0
    LINE = 1
    SQUARE = 2
    S = 3
    Z = 4
    L = 5
    J = 6
    T = 7

PIECES_CHARS = [
    "  ",
    f"{AZUL}██{RESET}",
    f"{AMARELO}██{RESET}",
    f"{VERMELHO}██{RESET}",
    f"{VERDE}██{RESET}",
    f"{LARANJA}██{RESET}",
    f"{ROSA}██{RESET}",
    f"{ROXO}██{RESET}",
]

PIECE_OPTIONS = [
    Pieces.LINE,
    Pieces.SQUARE,
    Pieces.S,
    Pieces.Z,
    Pieces.J,
    Pieces.T,
]


# isso aqui é o N da rotação
# usado em rotate()
SHAPE_BOXES = [
    0,
    4,
    2,
    3,
    3,
    3,
    3,
    3
]

SHAPES = {
    Pieces.LINE: [
        (0,0),
        (1,0),
        (2,0),
        (3,0)
    ],
    Pieces.SQUARE: [
        (0,0),
        (0,1),
        (1,0),
        (1,1)
    ],
    Pieces.S: [
        (0,0),
        (1,0),
        (1,1),
        (2,1)
    ],
    Pieces.Z: [
        (0,1),
        (1,1),
        (1,0),
        (2,0)
    ],
    Pieces.L: [
        (0,0),
        (1,0),
        (2,0),
        (2,1)
    ],
    Pieces.J: [
        (2,0),
        (2,1),
        (1,1),
        (0,1)
    ],
    Pieces.T: [
        (1,0),
        (1,1),
        (1,2),
        (0,1)
    ]
}
