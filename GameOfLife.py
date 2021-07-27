
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Live = 255
Dead = 0
vals = [Live, Dead]


def randomSeed(N):
    """returns a seed of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)


def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255],
                       [255,  0, 255],
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider


def addGlidertick(i, j, grid):
    """adds a Glider tick with top left cell at (i, j)"""
    tick = np.zeros(11*38).reshape(11, 38)

    tick[5][1] = tick[5][2] = 255
    tick[6][1] = tick[6][2] = 255

    tick[3][13] = tick[3][14] = 255
    tick[4][12] = tick[4][16] = 255
    tick[5][11] = tick[5][17] = 255
    tick[6][11] = tick[6][15] = tick[6][17] = tick[6][18] = 255
    tick[7][11] = tick[7][17] = 255
    tick[8][12] = tick[8][16] = 255
    tick[9][13] = tick[9][14] = 255

    tick[1][25] = 255
    tick[2][23] = tick[2][25] = 255
    tick[3][21] = tick[3][22] = 255
    tick[4][21] = tick[4][22] = 255
    tick[5][21] = tick[5][22] = 255
    tick[6][23] = tick[6][25] = 255
    tick[7][25] = 255

    tick[3][35] = tick[3][36] = 255
    tick[4][35] = tick[4][36] = 255

    grid[i:i+11, j:j+38] = tick


def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j-1) % N] + grid[i, (j+1) % N] +
                         grid[(i-1) % N, j] + grid[(i+1) % N, j] +
                         grid[(i-1) % N, (j-1) % N] + grid[(i-1) % N, (j+1) % N] +
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N])/255)
            # apply Conway's rules
            if grid[i, j] == Live:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = Dead
            else:
                if total == 3:
                    newGrid[i, j] = Live
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function


def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Run Game of Life")
  # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N*N).reshape(N, N)
        addGlidertick(10, 10, grid)
    else:
        # populate grid with random on/off - more off than on
        grid = randomSeed(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()
