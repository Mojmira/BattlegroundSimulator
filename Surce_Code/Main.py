from Model import *
from Data import *
from ArmyCreation import *
import time
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

if __name__ == '__main__':

    in_line(0, 19, 7, "#00AAB2", "I")
    in_line(0, 19, 6, "#00AAB2", "A")
    in_line(0, 19, 15, "red", "A")
    in_line(0, 19, 14, "red", "I")
    '''
    battle = Battlefield(20, 20)
    matrix = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]

    grid = Grid(matrix=np.transpose(battle.help_grid))
    print(grid.nodes)
    a = battle.schedule.agents[0]
    b = battle.schedule.agents[5]
    start = grid.node(a.pos[0], a.pos[1])
    end = grid.node(b.pos[0], b.pos[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    print(grid.node(0, 3))
    '''
