import customtkinter as ctk
import copy
import os
import threading
import sys
import io
import time

# Imports de tes modules
from sudoku_engine import init_game, has_error, is_victory
from infos import start_timer, stop_timer, get_system_stats
from backtracking import resoudre_sudoku
from force_brute import resoudre_force_brute
from force_brute_dichotomique import resoudre_optimise
from complexite import comparer_fonctions

# --- Palette de couleurs ---
COLORS = {
    "bg": "#0f0f14",
    "surface": "#1a1a24",
    "border_thin": "#2e2e42",
    "border_thick": "#c8a96e",
    "text_fixed": "#e8e6f0",
    "text_player": "#7c6fcd",
    "error_bg": "#3a1c20",
    "error_text": "#e05c6a",
    "success": "#5cc98a",
    "success_flash": "#2e7a4d",
    "info": "#4da6ff",
}


class SudokuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku - Édition Premium & Benchmark")
        self.geometry("600x850")
        self.configure(fg_color=COLORS["bg"])
        ctk.set_appearance_mode("dark")

        self.cells = {}
        self.player_grid = []
        self.fixed = []
        self.show_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ─── VUES ───────────────────────────────────────────────────────────────

    def show_menu(self):
        self.clear_window()
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(expand=True, fill="both", padx=40, pady=80)

        ctk.CTkLabel(
            menu_frame,
            text="✦ JEU & ALGORITHMES ✦",
            font=("DM Sans", 14, "bold"),
            text_color=COLORS["border_thick"],
        ).pack(pady=(0, 10))
        ctk.CTkLabel(
            menu_frame,
            text="SUDOKU",
            font=("Playfair Display", 60, "bold"),
            text_color=COLORS["text_fixed"],
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            menu_frame,
            text="▶ JOUER UNE PARTIE",
            font=("DM Sans", 16, "bold"),
            height=50,
            fg_color=COLORS["surface"],
            border_width=2,
            border_color=COLORS["border_thick"],
            text_color=COLORS["border_thick"],
            command=self.start_game,
        ).pack(fill="x", padx=50, pady=10)
        ctk.CTkButton(
            menu_frame,
            text="⚙️ BENCHMARK SOLVEUR",
            font=("DM Sans", 16, "bold"),
            height=50,
            fg_color=COLORS["surface"],
            border_width=2,
            border_color=COLORS["info"],
            text_color=COLORS["info"],
            command=self.start_solver,
        ).pack(fill="x", padx=50, pady=10)
        ctk.CTkButton(
            menu_frame,
            text="📁 CHARGER UN FICHIER",
            font=("DM Sans", 16, "bold"),
            height=50,
            fg_color=COLORS["surface"],
            border_width=2,
            border_color="#ffcc00",
            text_color="#ffcc00",
            command=self.show_file_selector,
        ).pack(fill="x", padx=50, pady=10)

    def show_file_selector(self):
        self.clear_window()
        self.build_header("MES GRILLES", "#ffcc00")
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=30, pady=20)
        folder_path = "pages"
        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
            for file_name in files:
                ctk.CTkButton(
                    scroll_frame,
                    text=f"📄 {file_name}",
                    fg_color=COLORS["surface"],
                    text_color=COLORS["text_fixed"],
                    anchor="w",
                    height=40,
                    command=lambda f=file_name: self.load_sudoku_from_file(f),
                ).pack(fill="x", pady=5)
        else:
            ctk.CTkLabel(scroll_frame, text="Dossier 'pages' introuvable...").pack()

    def load_sudoku_from_file(self, filename):
        path = os.path.join("pages", filename)
        with open(path, "r") as f:
            lines = f.readlines()
        grid, fixed = [], []
        for line in lines[:9]:
            row, fixed_row = [], []
            clean_line = line.strip().replace(".", "0")
            for char in clean_line[:9]:
                val = int(char) if char.isdigit() and char != "0" else 0
                row.append(val)
                fixed_row.append(True if val != 0 else False)
            grid.append(row)
            fixed.append(fixed_row)
        self.player_grid, self.fixed = grid, fixed
        self.start_solver()

    def build_header(self, title_text, color):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        self.lbl_status = ctk.CTkLabel(
            header,
            text=title_text,
            font=("Playfair Display", 28, "bold"),
            text_color=COLORS["text_fixed"],
        )
        self.lbl_status.pack(side="left")
        ctk.CTkButton(
            header,
            text="🏠 Menu",
            width=80,
            fg_color=COLORS["surface"],
            command=self.show_menu,
        ).pack(side="right", padx=(10, 0))

    def build_grid_ui(self, is_interactive=True):
        main_grid_frame = ctk.CTkFrame(
            self, fg_color=COLORS["border_thick"], corner_radius=0
        )
        main_grid_frame.pack(pady=10, padx=20)
        for block_y in range(3):
            for block_x in range(3):
                block_frame = ctk.CTkFrame(
                    main_grid_frame, fg_color=COLORS["border_thick"], corner_radius=0
                )
                block_frame.grid(row=block_y, column=block_x, padx=1.5, pady=1.5)
                for cell_y in range(3):
                    for cell_x in range(3):
                        y, x = block_y * 3 + cell_y, block_x * 3 + cell_x
                        val, is_fixed = self.player_grid[y][x], self.fixed[y][x]
                        cell = ctk.CTkEntry(
                            block_frame,
                            width=45,
                            height=45,
                            justify="center",
                            font=("DM Sans", 22, "bold"),
                            corner_radius=0,
                        )
                        cell.grid(row=cell_y, column=cell_x, padx=0.5, pady=0.5)
                        self.cells[(y, x)] = cell
                        if is_fixed:
                            cell.insert(0, str(val))
                            cell.configure(
                                state="disabled",
                                fg_color=COLORS["surface"],
                                text_color=COLORS["text_fixed"],
                            )
                        else:
                            if val != 0:
                                cell.insert(0, str(val))
                            cell.configure(
                                fg_color="#252533",
                                text_color=(
                                    COLORS["text_player"]
                                    if is_interactive
                                    else COLORS["info"]
                                ),
                            )

    # ─── LOGIQUE DE JEU & SOLVEUR ───────────────────────────────────────────

    def start_game(self):
        self.clear_window()
        self.solution, self.fixed, self.puzzle, self.player_grid = init_game()
        self.build_header("SUDOKU", COLORS["text_fixed"])
        self.build_grid_ui(is_interactive=True)

    def start_solver(self):
        self.clear_window()
        if not hasattr(self, "player_grid") or not self.player_grid:
            self.solution, self.fixed, self.puzzle, self.player_grid = init_game()

        self.build_header("BENCHMARK", COLORS["info"])
        self.build_grid_ui(is_interactive=False)

        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=30, pady=10)

        self.algo_var = ctk.StringVar(value="Backtracking Classique")
        ctk.CTkOptionMenu(
            ctrl_frame,
            variable=self.algo_var,
            values=[
                "Backtracking Classique",
                "Force Brute (Lent)",
                "MRV Optimisé (Rapide)",
            ],
            fg_color=COLORS["surface"],
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(
            ctrl_frame,
            text="▶ RÉSOUDRE",
            command=self.run_algorithm,
            fg_color=COLORS["info"],
        ).pack(side="right")

        self.stats_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"])
        self.stats_frame.pack(fill="x", padx=30, pady=10)
        self.lbl_stats = ctk.CTkLabel(
            self.stats_frame, text="En attente...", font=("DM Sans", 14)
        )
        self.lbl_stats.pack(padx=15, pady=15)

        ctk.CTkButton(
            self,
            text="📊 ANALYSE COMPLEXITÉ",
            font=("DM Sans", 13, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color="#9b59b6",
            text_color="#9b59b6",
            command=self.run_complexity_analysis,
        ).pack(fill="x", padx=30, pady=(10, 20))

    def run_algorithm(self):
        self.lbl_status.configure(text="RÉFLEXION...", text_color=COLORS["info"])
        self.update()
        self._execute_algo_logic()

    def _execute_algo_logic(self):
        algo = self.algo_var.get()
        # Nettoyage visuel forcé
        for r in range(9):
            for c in range(9):
                if not self.fixed[r][c]:
                    self.player_grid[r][c] = 0
                    self.cells[(r, c)].delete(0, "end")
        self.update()

        if algo == "Force Brute (Lent)":
            # La vraie force brute ne finit jamais : on lance dans un thread
            self.lbl_status.configure(text="FORCE BRUTE...", text_color="#e05c6a")
            self.lbl_stats.configure(text="⚠️ Calcul infini en cours — ne se terminera pas")
            threading.Thread(
                target=resoudre_force_brute,
                args=(self.player_grid,),
                kwargs={"fixed": self.fixed, "app": self},
                daemon=True
            ).start()
            return

        t0 = start_timer()
        if algo == "Backtracking Classique":
            resoudre_sudoku(self.player_grid, app=self)
        elif algo == "MRV Optimisé (Rapide)":
            resoudre_optimise(self.player_grid, app=self)

        t_total = stop_timer(t0)
        stats = get_system_stats()
        self._update_final_stats(t_total, stats)

    def _update_final_stats(self, t_total, stats):
        self.lbl_status.configure(text="TERMINÉ", text_color=COLORS["success"])
        # Restauration de l'affichage RAM et CPU
        stat_text = f"⏱️ {t_total:.4f}s | CPU: {stats.get('cpu_usage', 'N/A')}% | RAM: {stats.get('ram_usage', 'N/A')}%"
        self.lbl_stats.configure(text=stat_text)

    def run_complexity_analysis(self):
        self.complex_win = ctk.CTkToplevel(self)
        self.complex_win.title("Analyse de Complexité")
        self.complex_win.geometry("600x450")
        self.txt_output = ctk.CTkTextbox(
            self.complex_win, width=550, height=400, font=("Courier", 12)
        )
        self.txt_output.pack(pady=20, padx=20)
        threading.Thread(target=self._execute_complexity_logic, daemon=True).start()

    def _execute_complexity_logic(self):
        algos = {
            "Force Brute": lambda g: resoudre_force_brute(g, app=None),
            "Backtracking": lambda g: resoudre_sudoku(g, app=None),
        }
        buffer = io.StringIO()
        sys.stdout = buffer
        comparer_fonctions(
            algos, lambda n: init_game()[3], tailles=[5, 10, 15], repetitions=1
        )
        sys.stdout = sys.__stdout__
        self.after(0, lambda: self.txt_output.insert("end", buffer.getvalue()))


if __name__ == "__main__":
    SudokuApp().mainloop()