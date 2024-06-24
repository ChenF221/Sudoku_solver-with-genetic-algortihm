'''
Authors: Chen Yangfeng, Diaz Jimenez Jorge Arif, 5BM1, Escom IPN
26/jun/24  Algoritmos Bioinpirados, Proyecto Final
Sudoku_solver-with-genetic-algortihm
'''

import tkinter as tk
from tkinter import ttk
from sudokuGenerator import Sudoku
from sudokuSolver import algoritmo_genetico, obtener_fitness
import time

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm Sudoku Solver")
        self.initial_sudoku = None
        self.start_time = None

        self.sudoku_frame = ttk.Frame(root)
        self.sudoku_frame.grid(row=0, column=0, padx=10, pady=10)

        self.create_sudoku_board()

        self.parameters_frame = ttk.Frame(root)
        self.parameters_frame.grid(row=0, column=1, padx=10, pady=10)

        self.create_parameter_entries()
        self.create_difficulty_dropdown()
        self.create_buttons()

        self.create_status_labels()

    def create_sudoku_board(self):
        self.sudoku_canvas = tk.Canvas(self.sudoku_frame, width=360, height=360, bg="white")
        self.sudoku_canvas.pack()

    def create_parameter_entries(self):
        ttk.Label(self.parameters_frame, text="Tamaño de la población:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.population_entry = ttk.Entry(self.parameters_frame)
        self.population_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.parameters_frame, text="Número de generaciones:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.generations_entry = ttk.Entry(self.parameters_frame)
        self.generations_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.parameters_frame, text="Probabilidad de Mutación:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.mutation_prob_entry = ttk.Entry(self.parameters_frame)
        self.mutation_prob_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.parameters_frame, text="Probabilidad de Cruza:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.crossover_prob_entry = ttk.Entry(self.parameters_frame)
        self.crossover_prob_entry.grid(row=3, column=1, pady=5)

    def create_difficulty_dropdown(self):
        ttk.Label(self.parameters_frame, text="Dificultad:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.difficulty_var = tk.StringVar()
        difficulty_dropdown = ttk.Combobox(self.parameters_frame, textvariable=self.difficulty_var,
                                          values=["Fácil", "Intermedio", "Avanzado"])
        difficulty_dropdown.grid(row=4, column=1, pady=5)

    def create_buttons(self):
        ttk.Button(self.parameters_frame, text="Generar Sudoku", command=self.generate_sudoku).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.parameters_frame, text="Resolver Sudoku", command=self.solve_sudoku).grid(row=6, column=0, columnspan=2, pady=10)

    def create_status_labels(self):
        ttk.Label(self.parameters_frame, text="Generaciones:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.generations_label = ttk.Label(self.parameters_frame, text="")
        self.generations_label.grid(row=7, column=1, pady=5)

        ttk.Label(self.parameters_frame, text="Fitness:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.fitness_label = ttk.Label(self.parameters_frame, text="")
        self.fitness_label.grid(row=8, column=1, pady=5)

        ttk.Label(self.parameters_frame, text="Tiempo:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.time_label = ttk.Label(self.parameters_frame, text="")
        self.time_label.grid(row=9, column=1, pady=5)

    def generate_sudoku(self):
        difficulty_level = self.difficulty_var.get()
        sudoku_generator = Sudoku(9, difficulty_level)
        sudoku_generator.fillValues()
        self.initial_sudoku = sudoku_generator.mat
        self.display_sudoku(self.initial_sudoku)

    def solve_sudoku(self):
        if self.initial_sudoku is None:
            return

        # Validate the entered value for generations
        try:
            generations = int(self.generations_entry.get())
        except ValueError:
            # Show an error message or handle the invalid input appropriately
            print("Invalid input for the number of generations. Please enter a valid integer.")
            return

        population_size = int(self.population_entry.get())
        mutation_prob = float(self.mutation_prob_entry.get())
        crossover_prob = float(self.crossover_prob_entry.get())

        def update_gui_callback(iteration, sudoku):
            self.display_sudoku(sudoku, iteration=iteration)

            # Update status labels
            self.generations_label.config(text=f"Generaciones: {iteration}")
            self.fitness_label.config(text=f"Fitness: {obtener_fitness(sudoku)}")
            elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Tiempo: {elapsed_time:.2f} segundos")
            self.root.update_idletasks()

        self.start_time = time.time()
        sudoku_solver = algoritmo_genetico
        solution_found, solved_sudoku = sudoku_solver(
            self.initial_sudoku, population_size, generations,
            mutation_prob, crossover_prob, update_gui_callback
        )

        self.display_sudoku(solved_sudoku, solved=solution_found)

    def display_sudoku(self, sudoku, solved=False, iteration=None):
        self.sudoku_canvas.delete("all")
        cell_size = 40
        for i in range(9):
            for j in range(9):
                value = sudoku[i][j]
                x = j * cell_size
                y = i * cell_size

                if solved:
                    color = "green" if self.initial_sudoku and self.initial_sudoku[i][j] == 0 else "black"
                elif self.initial_sudoku and self.initial_sudoku[i][j] == 0:
                    color = "red" if not solved else "green"
                else:
                    color = "black"

                self.sudoku_canvas.create_text(x + cell_size // 2, y + cell_size // 2, text=value, font=("Arial", 12), fill=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
