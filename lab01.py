from collections import deque
import os

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

START_STATE = 583402761
GOAL_STATE = 123456780

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def count_inversions(x: int) -> int:
    arr = list()
    for i in range(9):
        d = extract_digit(x, i)
        if d != 0:
            arr.append(d)

    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv


def is_solvable(start: int, goal: int) -> bool:
    return count_inversions(start) % 2 == count_inversions(goal) % 2


def grid_print(ans: list, step=-1):
    for i in range(3):
        for k in range(len(ans)):
            for j in range(3):
                print(extract_digit(ans[k], i * 3 + j), end=" ")
            print("  ", end="")
        if step != -1 and i == 1:
            print(f"Шаг {step}")
        else:
            print()


def trek_print(ans: list):
    step = 0
    for u in ans[:0:-1]:
        grid_print([u], step)
        step += 1
        print("  |\n  V")
    grid_print([ans[0]], step)


def solve(x: int, y: int, alg="BFS", mode="auto"):
    history = dict()
    q = deque()
    ans = list()
    q.append(x)
    history[x] = x
    time_compl = 0

    while len(q) > 0:
        u = q.popleft()
        time_compl += 1
        if u == y:
            while u != x:
                ans.append(u)
                u = history[u]
            ans.append(u)
            break
        children = gen_children(u)
        if mode == "manual":
            grid_print([u])
            print("  |")
            print("  " + "-" * (len(children) * 8 - 7))
            print("  |     " * len(children))
            grid_print(children)
        for v in children:
            if v not in history.keys():
                history[v] = u
                if alg == "BFS":
                    q.append(v)
                else:
                    q.appendleft(v)
                if mode == "manual":
                    print("     ", end="   ")
            elif mode == "manual":
                print("  ✔  ", end="   ")
        if mode == "manual":
            print()
            if input() == "0":
                return None
    return ans, len(history.keys()), time_compl


while True:
    clear_console()
    print('Начальное состояние:')
    grid_print([START_STATE])
    print('Целевое состояние:')
    grid_print([GOAL_STATE])
    print("Выберите алгоритм решения:\n"
          "1. BFS\n"
          "2. DFS\n\n"
          "0. Выйти")
    x = input()
    while x != "0" and x != "1" and x != "2":
        clear_console()
        print("Некорректный ввод!")
        print("Выберите алгоритм решения:\n"
              "1. BFS\n"
              "2. DFS\n\n"
              "0. Выйти")
        x = input()
    if x == "1":
        alg = "BFS"
    elif x == "2":
        alg = "DFS"
    else:
        break

    clear_console()
    print(f"Алгоритм \"{alg}\".\n"
          "Выберите режим работы:\n"
          "1. Пошаговый\n"
          "2. Автоматический\n\n"
          "0. Выйти")
    x = input()
    while x != "0" and x != "1" and x != "2":
        clear_console()
        print("Некорректный ввод!")
        print(f"Алгоритм \"{alg}\".\n"
              "Выберите режим работы:\n"
              "1. Пошаговый\n"
              "2. Автоматический\n\n"
              "0. Выйти")
        x = input()
    if x == "1":
        mode = "manual"
        clear_console()
        print(f"Алгоритм \"{alg}\", режим \"Пошаговый\".\n"
              "Для следующего шага нажмите любую клавишу, кроме \"0\"\n"
              "Чтобы вернуться в меню, нажмите \"0\".")
    elif x == "2":
        mode = "auto"
        clear_console()
        print(f"Алгоритм \"{alg}\", режим \"Автоматический\".")
    else:
        break

    if not is_solvable(START_STATE, GOAL_STATE):
        print("Данное начальное состояние неразрешимо для выбранного целевого состояния.")
        print("Чтобы вернуться в меню, нажмите любую клавишу.")
        input()
        continue

    if mode == "manual":
        solve(START_STATE, GOAL_STATE, alg, mode)
    else:
        ans, space_compl, time_compl = solve(START_STATE, GOAL_STATE, alg, mode)
        trek_print(ans)
        print("----------------------------------------------")
        print(f"Ёмкостная сложность: {space_compl}")
        print(f"Временная сложность: {time_compl}")
        print(f"Стоимость пути: {len(ans) - 1}")
        print("----------------------------------------------")
        print("Чтобы вернуться в меню, нажмите любую клавишу.")
        input()
    continue
