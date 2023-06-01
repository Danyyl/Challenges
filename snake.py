def switch_direction(current):
    if current == 3:
        return 0
    else:
        return current+1


def spiralize(size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    spiral = [[0 for _ in range(size)]for _ in range(size)]
    i_size = j_size = [0, size-1]
    i = j = 0
    direction = 0
    while ((i_size[0] >= i+directions[direction][0] and i+directions[direction][0] <= i_size[1])
           or (j_size[0] >= j+directions[direction][1] and j+directions[direction][1] <= j_size[1])):

    return spiral


if __name__ == "__main__":
    print(spiralize(8), [[1, 1, 1, 1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 0, 1],
                                      [1, 0, 0, 0, 0, 1, 0, 1],
                                      [1, 0, 1, 0, 0, 1, 0, 1],
                                      [1, 0, 1, 1, 1, 1, 0, 1],
                                      [1, 0, 0, 0, 0, 0, 0, 1],
                                      [1, 1, 1, 1, 1, 1, 1, 1]])
