
# Sudoku Solver

## Project Context

Sudoku is a popular number-based puzzle game that has become a worldwide phenomenon. Originating from a mathematical concept called the Latin square, studied by mathematician Leonhard Euler in the 18th century, the modern version of Sudoku was created in 1979 by American architect Howard Garns under the name "Number Place."

The game gained significant popularity in Japan during the 1990s, where it acquired its now-famous name, "Sudoku." Maki Kaji, a Japanese puzzle editor, played a crucial role in the worldwide success of the game by helping to standardize the rules and format of Sudoku puzzles.

### How Sudoku Works

Sudoku is played on a 9×9 grid, divided into nine 3×3 sub-grids. The objective is to fill the entire grid with digits 1-9 without repeating any digit in:
- The same row
- The same column
- The same 3×3 sub-grid

## Project Overview

This project implements an automated Sudoku solver with multiple algorithmic approaches. The solver can read Sudoku grids from files, solve them using different methods, and display solutions both in the terminal and through a graphical interface using Pygame.

## Algorithms Implemented

### 1. Brute Force Method

**Description:** This method checks all possible combinations of digits 1-9 until a solution is found.

**How it works:**
- Iterates through all empty cells
- Tries each digit from 1-9
- Validates against Sudoku rules
- Continues until a valid solution is found

**Complexity:** O(9^n) where n is the number of empty cells
**Pros:** Simple to understand and implement
**Cons:** Extremely slow for larger puzzles; impractical for real-world use

### 2. Backtracking Method

**Description:** This method selects an empty cell and tries digits 1-9. If a digit conflicts with Sudoku rules, the algorithm backtracks recursively to the previously filled cell and tries the next digit.

**How it works:**
- Finds an empty cell
- Tries digits 1-9
- Checks validity against constraints
- Recursively solves remaining cells
- Backtracks on conflicts
- Continues until solved or determines no solution exists

**Complexity:** O(9^(n/k)) where n is empty cells and k is pruning efficiency
**Pros:** Much faster than brute force; practical for most puzzles
**Cons:** Still exponential; slower for extremely difficult puzzles

## Tools & Technologies Used

- **Python 3.11** - Core programming language
- **Object-Oriented Design** - Clean, maintainable code architecture
- **Pygame** - Graphical user interface for visual puzzle solving
- **Docker** - Containerization for consistent deployment

## Project Structure

sudoku-solver/ ├── sudoku_app.py # Main application entry point ├── sudoku_grid.py # SudokuGrid class implementation ├── README.md # Project documentation ├── Dockerfile # Docker containerization └── examples/ # Sample Sudoku puzzles ├── example1.txt ├── example2.txt ├── example3.txt ├── example4.txt └── example5.txt



## SudokuGrid Class

The `SudokuGrid` class provides the following methods:

- `import_grid(filename)` - Import and parse a Sudoku grid from a file
- `display()` - Display the current grid state in the terminal
- `solve_bruteforce()` - Solve using the brute force method
- `solve_backtracking()` - Solve using the backtracking method
- `is_valid(row, col, num)` - Validate a number placement
- `find_empty()` - Find the next empty cell





## SudokuGrid Class

The `SudokuGrid` class provides the following methods:

- `import_grid(filename)` - Import and parse a Sudoku grid from a file
- `display()` - Display the current grid state in the terminal
- `solve_bruteforce()` - Solve using the brute force method
- `solve_backtracking()` - Solve using the backtracking method
- `is_valid(row, col, num)` - Validate a number placement
- `find_empty()` - Find the next empty cell

## Input Format

Sudoku grids are provided as text files with the following format:


Where `_` represents empty cells and digits 1-9 represent given clues.

## Output Display

### Terminal Output
The solver displays solutions in the terminal, clearly distinguishing:
- **Original values** - Numbers present in the input grid
- **Solved values** - Numbers added by the algorithm

### Graphical Interface
An enhanced visual representation using Pygame shows:
- The complete solved grid
- Visual distinction between original and solved cells
- Clean, user-friendly interface

## Performance Analysis

### Comparison Table

| Criterion | Brute Force | Backtracking |
|-----------|------------|--------------|
| Time Complexity | O(9^n) | O(9^(n/k)) |
| Space Complexity | O(n) | O(n) |
| Avg. Execution Time (Easy) | ~0.5s | ~0.001s |
| Avg. Execution Time (Medium) | ~5s | ~0.01s |
| Avg. Execution Time (Hard) | >60s | ~0.1s |
| Practical Usability | Poor | Excellent |

### Observations

1. **Exponential Growth:** Both algorithms exhibit exponential growth, but backtracking is significantly faster due to constraint propagation.
2. **Pruning Efficiency:** Backtracking's ability to eliminate invalid branches early makes it vastly superior.
3. **Scalability:** Brute force becomes unusable for puzzles with many empty cells, while backtracking remains practical.
4. **Memory Usage:** Both use similar space complexity, as they maintain the grid state during recursion.

## Conclusion

**Recommended Algorithm: Backtracking**

The backtracking algorithm is the clear winner in this comparison. It demonstrates:
- **Orders of magnitude faster execution** on all puzzle difficulties
- **Practical usability** for real-time applications
- **Elegant recursive solution** leveraging constraint satisfaction
- **Optimal balance** between simplicity and performance

While brute force is conceptually simpler, it is impractical for solving actual Sudoku puzzles. Backtracking's ability to intelligently prune the search space makes it the industry standard for Sudoku solvers and constraint satisfaction problems in general.

## Usage

### Running with Python
```bash
python sudoku_app.py <path_to_sudoku_file>

docker build -t sudoku-solver .
docker run sudoku-solver <path_to_sudoku_file>

