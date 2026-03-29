import random

SIZE = 9
SPACE = 40  # Nombre de cases vides (tu peux l'ajuster)

# ─── Fonctions utilitaires de génération ─────────────────────────────────────


def is_number_valid(matrix, current_row_data, number):
    """Vérifie si un nombre peut être placé pendant la GÉNÉRATION de la grille"""
    current_col = len(current_row_data)

    # 1. Vérification de la ligne actuelle
    if number in current_row_data:
        return False

    # 2. Vérification de la colonne
    for row in matrix:
        if row[current_col] == number:
            return False

    # 3. Vérification du bloc 3x3
    row_idx = len(matrix)
    start_row = (row_idx // 3) * 3
    start_col = (current_col // 3) * 3

    for r in range(start_row, row_idx):
        for c in range(start_col, start_col + 3):
            if c < len(matrix[r]) and matrix[r][c] == number:
                return False

    return True


def make_sudoku():
    """Génère une grille de Sudoku complète et valide"""
    matrix = []
    for i in range(SIZE):
        new_row = []
        numbers = list(range(1, SIZE + 1))
        essais = 0

        while len(new_row) < SIZE:
            random.shuffle(numbers)
            found = False
            for number in numbers:
                if is_number_valid(matrix, new_row, number):
                    new_row.append(number)
                    found = True
                    break

            if not found:
                # Si blocage, on recommence la ligne
                new_row = []
                essais += 1
                # Si trop d'échecs sur une ligne, on reset TOUTE la grille (rare mais safe)
                if essais > 50:
                    return make_sudoku()

        matrix.append(new_row)
    return matrix


# ─── Initialisation du jeu ───────────────────────────────────────────────────


def make_spaces(matrix, fixed):
    """Crée les trous dans la grille en utilisant 0 pour le vide"""
    coords = []
    for r in range(9):
        for c in range(9):
            coords.append((r, c))

    random.shuffle(coords)
    for i in range(SPACE):
        y, x = coords[i]
        matrix[y][x] = 0  # CRUCIAL : On utilise 0 pour les algos
        fixed[y][x] = False


def init_game():
    """Prépare toutes les grilles nécessaires au lancement"""
    solution = make_sudoku()
    fixed = [[True] * 9 for _ in range(9)]
    puzzle = [row.copy() for row in solution]
    make_spaces(puzzle, fixed)
    player_grid = [row.copy() for row in puzzle]
    return solution, fixed, puzzle, player_grid


# ─── Détection des erreurs (Interface) ───────────────────────────────────────


def has_error(grid, y, x):
    """Vérifie si le chiffre à la position (y, x) est en conflit"""
    valeur = grid[y][x]

    # Pas d'erreur si la case est vide (0, None ou espace)
    if valeur in [0, " ", "", None]:
        return False

    valeur_str = str(valeur)

    # Vérification ligne
    for x2 in range(9):
        if x2 != x and str(grid[y][x2]) == valeur_str:
            return True

    # Vérification colonne
    for y2 in range(9):
        if y2 != y and str(grid[y2][x]) == valeur_str:
            return True

    # Vérification bloc 3x3
    bloc_y, bloc_x = (y // 3) * 3, (x // 3) * 3
    for dy in range(3):
        for dx in range(3):
            ry, rx = bloc_y + dy, bloc_x + dx
            if (ry != y or rx != x) and str(grid[ry][rx]) == valeur_str:
                return True

    return False


# ─── Condition de victoire ───────────────────────────────────────────────────


def is_victory(grid, solution):
    """Vérifie si la grille du joueur est identique à la solution"""
    for y in range(9):
        for x in range(9):
            if str(grid[y][x]) != str(solution[y][x]):
                return False
    return True
