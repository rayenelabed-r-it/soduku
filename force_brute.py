import time


def find_empty(grille):
    for r in range(9):
        for c in range(9):
            if grille[r][c] in [0, " ", "", None]:
                return (r, c)
    return None


def grille_valide(grille):
    """Vérifie la grille complète uniquement à la fin."""
    for i in range(9):
        ligne = [grille[i][j] for j in range(9) if grille[i][j] != 0]
        col = [grille[j][i] for j in range(9) if grille[j][i] != 0]
        if len(ligne) != len(set(ligne)) or len(col) != len(set(col)):
            return False
    for br in range(3):
        for bc in range(3):
            bloc = [
                grille[br * 3 + r][bc * 3 + c]
                for r in range(3) for c in range(3)
                if grille[br * 3 + r][bc * 3 + c] != 0
            ]
            if len(bloc) != len(set(bloc)):
                return False
    return True


def resoudre_force_brute(grille, fixed=None, app=None):
    """
    Vraie force brute classique : aucune vérification en cours de route.
    Essaie toutes les combinaisons (9^cases_vides), ne finit jamais en pratique.
    """
    case = find_empty(grille)
    if case is None:
        return grille_valide(grille)

    ligne, col = case
    for num in range(1, 10):
        grille[ligne][col] = num

        # Visualisation de chaque tentative en rouge
        if app:
            try:
                app.cells[(ligne, col)].delete(0, "end")
                app.cells[(ligne, col)].insert(0, str(num))
                app.cells[(ligne, col)].configure(text_color="#e05c6a")
                app.update_idletasks()
                app.update()
                time.sleep(0.001)
            except:
                return False

        # Aucune vérification de validité : on descend dans tous les cas
        if resoudre_force_brute(grille, fixed, app):
            return True

        # Backtrack
        grille[ligne][col] = 0
        if app:
            try:
                app.cells[(ligne, col)].delete(0, "end")
                app.update_idletasks()
                app.update()
            except:
                pass

    return False