# Sudoku Solver with Genetic Algorithm

This project consists of a Sudoku solver that utilizes a genetic algorithm to find solutions for Sudoku puzzles. The solver is integrated with a graphical user interface (GUI) for easy interaction.

## Files in the Project

### Interfaz.py
This file defines a graphical user interface (GUI) using Tkinter. The main features of the GUI include:
- **Parameter Inputs**: Users can input parameters for the genetic algorithm:
  - Population size
  - Number of generations
  - Mutation probability
  - Crossover probability
- **Difficulty Selection**: A dropdown menu to select the difficulty of the Sudoku puzzle.
- **Buttons**:
  - Generate Sudoku: Generates a new Sudoku puzzle based on the selected difficulty.
  - Solve Sudoku: Solves the generated Sudoku puzzle using the genetic algorithm.
- **Status Display**: Labels to display the status and timing of the generation and solving process.

### sudokuGenerator.py
This file contains the logic to generate Sudoku puzzles. Key functions include:
- **Sudoku Class**: Handles the creation of a valid Sudoku grid.
- **remove_cells Function**: Removes cells from the grid according to the selected difficulty while ensuring the puzzle remains solvable.

### sudokuSolver.py
This file implements a genetic algorithm to solve Sudoku puzzles. Key components include:
- **Population Initialization**: Functions to generate an initial population of possible solutions.
- **Crossover and Mutation**: Functions to perform genetic operations on the population.
- **Fitness Evaluation**: Functions to evaluate how close a solution is to being a valid Sudoku.
- **Main Genetic Algorithm**: Runs the genetic algorithm iterating through generations to find a solution. Includes a callback function to update the GUI with the current iteration and solution.

## How to Use

1. Run the `Interfaz.py` file to launch the GUI.
2. Input the desired parameters for the genetic algorithm.
3. Select the difficulty level of the Sudoku puzzle.
4. Click on "Generate Sudoku" to create a new puzzle.
5. Click on "Solve Sudoku" to solve the generated puzzle using the genetic algorithm.
6. The status and time taken for each process will be displayed in the GUI.

## Dependencies

- Python 3.x
- Tkinter (for GUI)
- Standard Python libraries (random, time, etc.)

## Example Usage

1. **Generating a Sudoku**:
   - Select "Medium" difficulty.
   - Click "Generate Sudoku".
   - A Sudoku puzzle will be displayed on the board.

2. **Solving the Sudoku**:
   - Input population size: 400
   - Input number of generations: 1000
   - Input mutation probability: 0.1
   - Input crossover probability: 0.85
   - Click "Solve Sudoku".
   - The GUI will display the progress and the time taken to find a solution.

## Notes

- The genetic algorithm may not always find a solution, especially for higher difficulties or insufficient generations.
- Adjusting parameters like population size, mutation probability, and crossover probability can improve the chances of finding a solution.

