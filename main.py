#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,too-few-public-methods
# pylint: disable=invalid-name,unused-argument,unused-variable
# pylint: disable=bare-except

from __future__ import print_function

class Dirs(object):
    up = "up"
    down = "down"
    left = "left"
    right = "right"
    backward = "backward"
    forward = "forward"


dirs = {
    "up": (0, -1, 0),
    "down": (0, 1, 0),
    "left": (-1, 0, 0),
    "right": (1, 0, 0),
    "backward": (0, 0, -1),
    "forward": (0, 0, 1),
}
def dir_to_delta(name):
    return dirs[name]

def allowed_dirs_from(name):
    if name == Dirs.up or name == Dirs.down:
        return [Dirs.left, Dirs.right, Dirs.backward, Dirs.forward]
    elif name == Dirs.left or name == Dirs.right:
        return [Dirs.up, Dirs.down, Dirs.backward, Dirs.forward]
    elif name == Dirs.backward or name == Dirs.forward:
        return [Dirs.up, Dirs.down, Dirs.left, Dirs.right]


def is_valid_coord(coord):
    x, y, z = coord
    if x < 0 or x >= 3 or y < 0 or y >= 3 or z < 0 or z >= 3:
        return False
    return True

def index_to_coord(index):
    z = index / 9
    i = index - (9 * z)
    y = i / 3
    x = i % 3
    return (x, y, z)

def coord_to_index(coord):
    x, y, z = coord
    return (z * 9) + ((y * 3) + x)

def add_coords(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return (x1 + x2, y1 + y2, z1 + z2)

def cube_complete(cube):
    return all(cube)

def print_cube(cube):
    c = cube
    print('[%d,%d,%d]  [%d,%d,%d]  [%d,%d,%d]' %
          (c[0], c[1], c[2], c[9], c[10], c[11], c[18], c[19], c[20]))
    print('[%d,%d,%d]  [%d,%d,%d]  [%d,%d,%d]' %
          (c[3], c[4], c[5], c[12], c[13], c[14], c[21], c[22], c[23]))
    print('[%d,%d,%d]  [%d,%d,%d]  [%d,%d,%d]' %
          (c[6], c[7], c[8], c[15], c[16], c[17], c[24], c[25], c[26]))
    print()

def recursive_solve(blocks, cube, coord, direction, answer):
    #print(direction, coord, answer)
    #print_cube(cube)

    if cube_complete(cube):
        return answer

    new_blocks = blocks[:]
    new_cube = cube[:]

    try:
        first_blocks = new_blocks.pop(0)
    except:
        print("ERROR")
        print_cube(cube)
        return answer

    index = coord_to_index(coord)
    if new_cube[index] == 0:
        first_blocks -= 1
        new_cube[index] = 1

    current_coord = coord
    while first_blocks > 0:
        current_coord = add_coords(current_coord, dirs[direction])
        #print("current_coord", current_coord)
        if not is_valid_coord(current_coord):
            return None

        try:
            current_index = coord_to_index(current_coord)
        except:
            print("ERROR current_index", current_index)
            raise

        if new_cube[current_index] == 1:
            return None

        new_cube[current_index] = 1
        first_blocks -= 1

    allowed_dirs = allowed_dirs_from(direction)
    for d in allowed_dirs:
        ans = recursive_solve(new_blocks, new_cube,
                              current_coord, d, answer + [d])
        if ans is not None:
            return ans

    return None

def solve(blocks):
    for i in xrange(27):
        for d in dirs.keys():
            cube = [0] * 27
            ans = recursive_solve(blocks, cube, index_to_coord(i), d, [d])
            if ans is not None:
                return ans

    return "No Answer"

def main():
    blocks = [3, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2]
    print("answer")
    print(solve(blocks))

    blocks_reverse = blocks[::-1]
    blocks_reverse[0] += 1
    blocks_reverse[len(blocks_reverse)-1] -= 1
    print("answer reverse")
    print(solve(blocks_reverse))

if __name__ == "__main__":
    main()


