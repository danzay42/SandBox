import numpy as np
import matplotlib.pyplot as plt


def change_state(x, y, old_space):
    neighbors = sum([sum(i[y-1: y+2]) for i in old_space[x-1:x+2]])
    if old_space[x][y] and (neighbors == 2 or neighbors == 3):
        return True
    elif neighbors == 3:
        return True
    else:
        return False


def cycle():
    space_0 = np.zeros((50,50), dtype=int)
    space_1 = space_0.copy()

    space_0[25][25] = 1
    # space_0[25][26] = 1
    space_0[25][27] = 1
    space_0[26][25] = 1
    space_0[27][25] = 1
    # space_0[27][27] = 1

    while sum([sum(ys) for ys in space_0]):
        plt.imshow(space_0)
        plt.show()
        print(sum([sum(ys) for ys in space_0]))
        for x, y_line in enumerate(space_0[1:-1]):
            for y, state in enumerate(y_line[1: -1]):
                space_1[x][y] = int(change_state(x, y, space_0))
        space_0 = space_1.copy()


if __name__ == '__main__':
    cycle()
