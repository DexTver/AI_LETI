from collections import deque

pos_from_pos = {0: [1, 3],
                1: [0, 2, 4],
                2: [1, 5],
                3: [0, 4, 6],
                4: [1, 3, 5, 7],
                5: [2, 4, 8],
                6: [3, 7],
                7: [4, 6, 8],
                8: [5, 7]
                }


def extract_digit(x: int, i: int) -> int:
    return x % 10 ** (9 - i) // 10 ** (8 - i)


def swap_in_int(x: int, i: int, j: int) -> int:
    return x + extract_digit(x, j) * 10 ** (8 - i) - extract_digit(x, j) * 10 ** (8 - j)


def gen_children(x: int):
    for i in range(9):
        if extract_digit(x, i) == 0:
            ans = list()
            for j in pos_from_pos[i]:
                ans.append(swap_in_int(x, i, j))
            return ans
    return None


def grid_print(x: int, step=-1):
    for i in range(3):
        for j in range(3):
            print(extract_digit(x, i * 3 + j), end=" ")
        if step != -1 and i == 1:
            print(f" Шаг {step}")
        else:
            print()


def trek_print(ans: list):
    step = 0
    for u in ans[:0:-1]:
        grid_print(u, step)
        step += 1
        print("  |\n  V")
    grid_print(ans[0], step)


def bfs(x: int, y: int) -> list:
    history = dict()
    q = deque()
    q.append(x)
    ans = list()

    while len(q) > 0:
        u = q.popleft()
        if u == y:
            while u != x:
                ans.append(u)
                u = history[u]
            ans.append(u)
            break
        for v in gen_children(u):
            if v not in history.keys():
                history[v] = u
                q.append(v)
    return ans


def dfs(x: int, y: int) -> list:
    history = dict()
    q = deque()
    q.appendleft(x)
    ans = list()

    while len(q) > 0:
        u = q.popleft()
        if u == y:
            while u != x:
                ans.append(u)
                u = history[u]
            ans.append(u)
            break
        for v in gen_children(u):
            if v not in history.keys():
                history[v] = u
                q.appendleft(v)
    return ans

trek_print(bfs(583402761, 123456780))
trek_print(dfs(583402761, 123456780))