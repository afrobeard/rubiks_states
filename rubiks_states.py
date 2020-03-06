from numpy import rot90, arange, cbrt
from enum import Enum


class Face(Enum):
    """
    Defined by Where normal points
    """

    INTO = 1
    HORIZONTAL = 2
    VERTICAL = 3


class Rotation(Enum):
    CLOCK = 1
    COUNTERCLOCK = 2


def get_matrix(cube_size=2):
    return arange(1, cube_size ** 3 + 1).reshape(cube_size, cube_size, cube_size)


def get_slice(matrix, index, face):
    if face == Face.INTO:
        return matrix[index]
    elif face == Face.HORIZONTAL:
        return matrix[:, index]
    elif face == Face.VERTICAL:
        return matrix[:, :, index]
    raise ValueError("Face")


def set_slice(matrix, index, face, slice):
    if face == Face.INTO:
        matrix[index] = slice
    elif face == Face.HORIZONTAL:
        matrix[:, index] = slice
    elif face == Face.VERTICAL:
        matrix[:, :, index] = slice
    else:
        raise ValueError("Face")


def rotate(matrix, direction):
    if direction == Rotation.CLOCK:
        return rot90(matrix, k=1, axes=(1, 0))
    elif direction == Rotation.COUNTERCLOCK:
        return rot90(matrix, k=1, axes=(0, 1))
    raise ValueError("Direction")


def get_hash(matrix, hash_algo=1):
    if hash_algo == 2:
        return hash(matrix.tostring())
    return "".join([str(x) for x in matrix.flatten()])


def add_to_hash_set(matrix, hash_set):
    initial_len = len(hash_set)
    hashed_value = get_hash(matrix)
    hash_set.update([hashed_value])
    is_added = bool(len(hash_set) - initial_len)
    return hashed_value, is_added


def solver(matrix, hash_set, cube_width):
    frontier = dict()
    for offset in range(1, cube_width):  # Ignoring 0th to hold edge block constant
        for face_type in Face:
            for rotation_type in Rotation:
                shadow_matrix = matrix.copy()
                slice = get_slice(shadow_matrix, offset, face_type)
                rotated_slice = rotate(slice, rotation_type)
                set_slice(shadow_matrix, offset, face_type, rotated_slice)
                hashed_value, is_unvisited = add_to_hash_set(shadow_matrix, hash_set)
                if is_unvisited:
                    is_stuck = False
                    msg = """From:
{}
To:
{}
{} {} {} {}""".format(matrix, shadow_matrix, face_type, offset, rotation_type, hashed_value)
                    #print(msg)
                    frontier[hashed_value] = shadow_matrix
                else:
                    pass  # print(len(hash_set), matrix)
    return frontier


class Solver(object):
    def solve(self):
        frontier_dict = {
            self.genesis_matrix_hash: self.genesis_matrix
        }

        print(len(frontier_dict))
        while len(frontier_dict.keys()):
            new_frontier_states = dict()
            for (hash_code, matrix) in frontier_dict.items():
                new_frontier_states_for_state = solver(matrix, self.hash_set, self.cube_size)
                new_frontier_states.update(new_frontier_states_for_state)
            frontier_dict = new_frontier_states
            print(len(frontier_dict))

    def __init__(self, cube_size=2):
        self.hash_set = set()
        self.cube_size = cube_size
        self.genesis_matrix = get_matrix(self.cube_size)
        self.genesis_matrix_hash = add_to_hash_set(self.genesis_matrix, self.hash_set)


if __name__ == "__main__":
    rubik = Solver(cube_size=2)
    rubik.solve()
    print(len(rubik.hash_set))


    """
    matrix = get_matrix(cube_size=2)
    slice = get_slice(matrix, 0, Face.INTO)
    clock_slice = rotate(slice, Rotation.CLOCK)
    print("Full", matrix)
    print(slice)
    print(clock_slice)
    set_slice(matrix, 0, Face.INTO, clock_slice)
    print("Full", matrix)
    import pdb
    pdb.set_trace()
    """


