import time


class SudokuOptimise:
    def __init__(self, grille_gui, app=None):
        self.app = app
        # On initialise la grille interne
        self.grille = [[0] * 9 for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]

        # Chargement initial
        for r in range(9):
            for c in range(9):
                val = grille_gui[r][c]
                # On gère tous les types de cases vides
                if val not in [" ", 0, "", None]:
                    num = int(val)
                    self.rows[r].add(num)
                    self.cols[c].add(num)
                    self.boxes[self._box(r, c)].add(num)
                    self.grille[r][c] = num

    def _box(self, r, c):
        return (r // 3) * 3 + (c // 3)

    def _placer(self, r, c, val):
        self.rows[r].add(val)
        self.cols[c].add(val)
        self.boxes[self._box(r, c)].add(val)
        self.grille[r][c] = val

        # --- VISUALISATION ---
        if self.app:
            try:
                # Vert pour montrer que l'IA est "intelligente"
                self.app.cells[(r, c)].configure(text_color="#5cc98a")
                self.app.cells[(r, c)].delete(0, "end")
                self.app.cells[(r, c)].insert(0, str(val))

                # Force le dessin sur Mac
                self.app.update_idletasks()
                self.app.update()

                # Vitesse optimisée : 0.01 est un bon compromis
                time.sleep(0.01)
            except:
                pass

    def _retirer(self, r, c, val):
        self.rows[r].discard(val)
        self.cols[c].discard(val)
        self.boxes[self._box(r, c)].discard(val)
        self.grille[r][c] = 0

        # --- NETTOYAGE VISUEL ---
        if self.app:
            try:
                self.app.cells[(r, c)].delete(0, "end")
                self.app.update_idletasks()
                self.app.update()
                time.sleep(0.005)
            except:
                pass

    def _candidats(self, r, c):
        utilises = self.rows[r] | self.cols[c] | self.boxes[self._box(r, c)]
        return set(range(1, 10)) - utilises

    def _mrv(self):
        """Trouve la case avec le moins de possibilités (Heuristique MRV)"""
        meilleur = None
        meilleurs_can = None
        min_options = 10

        for r in range(9):
            for c in range(9):
                if self.grille[r][c] == 0:
                    candidats = self._candidats(r, c)
                    n = len(candidats)
                    if n == 0:
                        return r, c, set()  # Impasse
                    if n < min_options:
                        min_options = n
                        meilleur = (r, c)
                        meilleurs_can = candidats
                        if n == 1:
                            return r, c, meilleurs_can  # On a trouvé une case forcée

        return (
            (meilleur[0], meilleur[1], meilleurs_can)
            if meilleur
            else (None, None, None)
        )

    def solve(self):
        r, c, candidats = self._mrv()

        # Si plus de cases vides, c'est gagné
        if r is None:
            return True

        # Si on est dans une impasse
        if not candidats:
            return False

        for num in sorted(list(candidats)):
            self._placer(r, c, num)
            if self.solve():
                return True
            self._retirer(r, c, num)
        return False


def resoudre_optimise(grille, app=None):
    optimiseur = SudokuOptimise(grille, app)
    if optimiseur.solve():
        # On recopie la solution dans la grille d'origine
        for r in range(9):
            for c in range(9):
                grille[r][c] = optimiseur.grille[r][c]
        return True
    return False
