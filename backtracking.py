import time


def est_valide(grille, ligne, col, num):
    # Vérification ligne
    for j in range(9):
        if grille[ligne][j] == num:
            return False
    # Vérification colonne
    for i in range(9):
        if grille[i][col] == num:
            return False
    # Vérification carré 3x3
    debut_l, debut_c = 3 * (ligne // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grille[debut_l + i][debut_c + j] == num:
                return False
    return True


def resoudre_sudoku(grille, app=None):
    # Initialisation du compteur
    if not hasattr(resoudre_sudoku, "compteur"):
        resoudre_sudoku.compteur = 0
        print("\n[IA] Tentative de forçage visuel...", end="")

    for ligne in range(9):
        for col in range(9):
            # On cherche une case vide
            if grille[ligne][col] in [0, " ", "", None]:
                for num in range(1, 10):
                    if est_valide(grille, ligne, col, num):
                        grille[ligne][col] = num
                        resoudre_sudoku.compteur += 1

                        # --- LE FORCEUR D'AFFICHAGE (VERSION MAC AGRESSIVE) ---
                        if app:
                            try:
                                # 1. On change le TITRE de la fenêtre pour prouver que l'IA communique
                                app.title(f"SUDOKU - IA en test sur ({ligne},{col})")

                                # 2. On récupère la cellule et on écrit
                                cell = app.cells.get((ligne, col))
                                if cell:
                                    cell.delete(0, "end")
                                    cell.insert(0, str(num))
                                    cell.configure(text_color="#4da6ff")

                                # 3. FORÇAGE DOUBLE (Le secret sur Mac)
                                app.update_idletasks()  # Prépare le dessin
                                app.update()  # Exécute le dessin MAINTENANT

                                # 4. Petit log terminal pour débugger
                                if resoudre_sudoku.compteur % 5 == 0:
                                    print(
                                        f"[{ligne},{col}]->{num}", end=" ", flush=True
                                    )

                                # Pause de 0.2s pour que l'œil humain capte le changement
                                time.sleep(0.01)

                            except Exception as e:
                                print(f"\n[Erreur lien interface] : {e}")
                                return False

                        # Appel récursif
                        if resoudre_sudoku(grille, app):
                            return True

                        # --- BACKTRACK (Effacement visuel) ---
                        grille[ligne][col] = 0
                        if app:
                            try:
                                app.cells[(ligne, col)].delete(0, "end")
                                app.update_idletasks()
                                app.update()
                                time.sleep(0.005)
                            except:
                                pass

                return False

    # Fin de l'algorithme
    if hasattr(resoudre_sudoku, "compteur"):
        del resoudre_sudoku.compteur
        if app:
            app.title("SUDOKU - ✅ RÉSOLU")
        print("\n✅ Terminé !")

    return True
