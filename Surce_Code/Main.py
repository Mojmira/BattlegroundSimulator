from Model import *
from Data import *
from ArmyCreation import *
import time
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

if __name__ == '__main__':
    '''
    in_line(0, 19, 7, "#00AAB2", "I")
    in_line(0, 19, 6, "#00AAB2", "A")
    in_line(0, 19, 5, "#00AAB2", "I")
    in_line(0, 19, 3, "#00AAB2", "A")
    in_line(0, 19, 4, "#00AAB2", "I")
    in_line(0, 19, 15, "red", "A")
    in_line(0, 19, 14, "red", "I")
    in_line(0, 19, 13, "red", "I")
    in_line(0, 19, 17, "red", "A")
    in_line(0, 19, 16, "red", "I")
    '''
    battle = Battlefield(20, 20)
    matrix = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]

    grid = Grid(matrix=np.transpose(battle.help_grid))

    start = grid.node(0, 7)
    end = grid.node(0, 9)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    print(path)
