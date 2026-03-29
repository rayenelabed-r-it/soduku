import time
import math
import statistics
import copy

# 1. ══════════ CLASSES DE COMPLEXITÉ ══════════
_CLASSES = {
    "O(1)": lambda n: 1,
    "O(log n)": lambda n: math.log2(n) if n > 1 else 1,
    "O(n)": lambda n: n,
    "O(n log n)": lambda n: n * math.log2(n) if n > 1 else n,
    "O(n²)": lambda n: n**2,
    "O(n³)": lambda n: n**3,
    "O(2ⁿ)": lambda n: 2**n,
    "O(9ⁿ)": lambda n: 9**n,  # Spécifique au Sudoku (Backtracking)
}

# 2. ══════════ FONCTIONS MOTEURS ══════════


def _mesurer(fonction, entree, repetitions=2):
    """Mesure le temps moyen en évitant les blocages infinis"""
    temps = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        # On exécute la fonction.
        # Note : On ne peut pas facilement killer un thread Python,
        # mais on mesure ici le temps réel.
        fonction(entree)
        fin = time.perf_counter() - debut
        temps.append(fin)
    return statistics.median(temps)


def comparer_fonctions(fonctions, generateur_entree, tailles=None, repetitions=2):
    if tailles is None:
        tailles = [5, 10, 15]  # Tailles prudentes

    resultats = {}
    print("\n" + "═" * 70)
    print("  RÉSULTATS DU BENCHMARK (ms)")
    print("═" * 70)

    # En-tête du tableau
    header = f"{'Vides (n)':>10}"
    for nom in fonctions:
        header += f" | {nom:>15}"
    print(header)
    print("-" * len(header))

    for n in tailles:
        # On génère une grille avec exactement 'n' cases vides
        entree = generateur_entree(n)
        row_str = f"{n:>10}"

        for nom, fn in fonctions.items():
            # Sécurité : Si Force Brute et n > 20, on prévient que c'est risqué
            if nom == "Force Brute" and n > 25:
                row_str += f" | {'SKIP (> long)':>15}"
                continue

            try:
                # On passe une COPIE pour ne pas modifier la grille pour l'algo suivant
                t = _mesurer(fn, copy.deepcopy(entree), repetitions)
                row_str += f" | {t * 1000:>12.2f} ms"
                resultats.setdefault(nom, []).append(t)
            except Exception as e:
                row_str += f" | {'ERREUR':>15}"

        print(row_str)

    print("═" * 70)
    return resultats


# 3. ══════════ BLOC D'EXÉCUTION ══════════

if __name__ == "__main__":
    # Import local pour éviter les imports circulaires
    from force_brute import resoudre_force_brute
    from backtracking import resoudre_sudoku
    from force_brute_dichotomique import resoudre_optimise
    from sudoku_engine import make_sudoku, make_spaces

    def generer_grille_test(n_vides):
        """Génère une grille complète puis retire n cases"""
        soluce = make_sudoku()
        fixed = [[True] * 9 for _ in range(9)]
        puzzle = copy.deepcopy(soluce)

        # On vide manuellement n cases
        coords = [(r, c) for r in range(9) for c in range(9)]
        import random

        random.shuffle(coords)
        for i in range(min(n_vides, 81)):
            r, c = coords[i]
            puzzle[r][c] = 0
        return puzzle

    algos = {
        "Force Brute": lambda g: resoudre_force_brute(g, app=None),
        "Backtracking": lambda g: resoudre_sudoku(g, app=None),
        "MRV Optimisé": lambda g: resoudre_optimise(g, app=None),
    }

    # Test sur des petites tailles de difficulté (nombre de cases vides)
    comparer_fonctions(
        fonctions=algos,
        generateur_entree=generer_grille_test,
        tailles=[5, 10, 15, 20, 25],
        repetitions=1,  # 1 seule rép suffit pour un benchmark visuel
    )
