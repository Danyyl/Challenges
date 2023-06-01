"""
Your task is to help Tempter - write a function

height :: Integer -> Integer -> Integer
height n m = -- see text
that takes 2 arguments - the number of eggs n and the number of trys m - you should calculate maximum scyscrapper height (in floors), in which it is guaranteed to find an exactly maximal floor from which that an egg won't crack it.

Which means,

You can throw an egg from a specific floor every try
Every egg has the same, certain durability - if they're thrown from a certain floor or below, they won't crack. Otherwise they crack.
You have n eggs and m tries
What is the maxmimum height, such that you can always determine which floor the target floor is when the target floor can be any floor between 1 to this maximum height?
Examples
height 0 14 = 0
height 2 0  = 0
height 2 14 = 105
height 7 20 = 137979



First impl (time out)

def height(n, m):
    if 0 in [n, m]:
        return 0
    arr = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0:
                arr[i][j] = j+i+1
            elif j == 0:
                arr[i][j] = 1
            elif i > j:
                arr[i][j] = arr[i-1][j]
            else:
                arr[i][j] = arr[i][j-1] + arr[i-1][j-1] + 1
    return arr[n-1][m-1]
"""

tests = {
    (0, 14): 0,
    (2, 0): 0,
    (2, 14): 105,
    (7, 20): 137979,
}


def height(n, m):
    h, bk = 0, 1
    for i in range(1, n+1):
        bk = bk * m // i
        h += bk
        m -= 1
    return h


if __name__ == "__main__":
    for key, value in tests.items():
        out = height(*key)
        print(f"data - {key}, result - {value == out}\n"
              f"Output - {out}")

