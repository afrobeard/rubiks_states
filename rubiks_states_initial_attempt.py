
def fresh_cube():
    cube = {
        (1, 1, 1): 1,
        (2, 1, 1): 2,
        (1, 2, 1): 3,
        (2, 2, 1): 4,
        (1, 1, 2): 5,
        (2, 1, 2): 6,
        (1, 2, 2): 7,
        (2, 2, 2): 8,
    }
    return cube


def hash_cube(cube):
    return tuple(cube.items())


def front_clock(cube):
    cube_clone = dict(cube)
    cube[(1, 1, 2)] = cube_clone[(1, 2, 2)]
    cube[(2, 1, 2)] = cube_clone[(1, 1, 2)]
    cube[(1, 2, 2)] = cube_clone[(2, 2, 2)]
    cube[(2, 2, 2)] = cube_clone[(2, 1, 2)]
    return cube

def backrub(fun, cube):
    cube = fun(cube)
    cube = fun(cube)
    cube = fun(cube)
    return cube

def right_clock(cube):
    cube_clone = dict(cube)
    cube[(2, 1, 2)] = cube_clone[(2, 2, 2)]
    cube[(2, 1, 1)] = cube_clone[(2, 1, 2)]
    cube[(2, 2, 2)] = cube_clone[(2, 2, 1)]
    cube[(2, 2, 1)] = cube_clone[(2, 1, 1)]
    return cube

def bottom_clock(cube):
    cube_clone = dict(cube)
    cube[(1, 2, 1)] = cube_clone[(1, 2, 2)]
    cube[(2, 2, 1)] = cube_clone[(1, 2, 1)]
    cube[(1, 2, 2)] = cube_clone[(2, 2, 2)]
    cube[(2, 2, 2)] = cube_clone[(2, 2, 1)]
    return cube

def front_anticlock(cube):
    return backrub(front_clock, cube)

def bottom_anticlock(cube):
    return backrub(bottom_clock, cube)

def right_anticlock(cube):
    return backrub(right_clock, cube)


def solver(cube, acc_set=set(), op_list=None):
    front_clock_cube = front_clock(cube)
    bottom_clock_cube = bottom_clock(cube)
    right_clock_cube = right_clock(cube)
    front_anticlock_cube = front_anticlock(cube)
    bottom_anticlock_cube = bottom_anticlock(cube)
    right_anticlock_cube = right_anticlock(cube)

    for (label, transmuted_cube) in [
        ("fc", front_clock_cube),
        ("bc", bottom_clock_cube),
        ("rc", right_clock_cube),
        ("fa'", front_anticlock_cube),
        ("ba", bottom_anticlock_cube),
        ("ra", right_anticlock_cube),
    ]:
        hash_code = hash_cube(transmuted_cube)
        if op_list:
            op_list.append(label)
        else:
            op_list = [label]
        if hash_code not in acc_set:
            print(repr(op_list))
            acc_set.update([hash_code])
            solver(transmuted_cube, acc_set=acc_set, op_list=op_list)
            print(len(hash_code))

genesis_cube = fresh_cube()
genesis_code = hash_cube(genesis_cube)
acc_set = set([genesis_code])
solver(genesis_cube, acc_set=acc_set)