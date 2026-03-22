import heapq
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

BLOCK_WIDTH = 8
TREE_LINE_SHIFT = 2


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def extract_digit(x: int, i: int) -> int:
    return x % 10 ** (9 - i) // 10 ** (8 - i)


def build_goal_pos(goal: int) -> dict:
    goal_pos = {}
    for i in range(9):
        goal_pos[extract_digit(goal, i)] = i
    return goal_pos

GOAL_POS = build_goal_pos(GOAL_STATE)

def swap_digits(x: int, i: int, j: int) -> int:
    di = extract_digit(x, i)
    dj = extract_digit(x, j)
    return x + (dj - di) * 10 ** (8 - i) + (di - dj) * 10 ** (8 - j)


def gen_children(x: int):
    zero_pos = 0
    for i in range(9):
        if extract_digit(x, i) == 0:
            zero_pos = i
            break
    ans = []
    for j in pos_from_pos[zero_pos]:
        ans.append(swap_digits(x, zero_pos, j))
    return ans


def state_row_text(state: int, row: int) -> str:
    return ''.join(f'{extract_digit(state, row * 3 + j)} ' for j in range(3)) + '  '


def grid_print(ans: list, step=-1):
    for i in range(3):
        for k in range(len(ans)):
            print(state_row_text(ans[k], i), end='')
        if step != -1 and i == 1:
            print(f'Шаг {step}')
        else:
            print()


def h1(state: int) -> int:
    cnt = 0
    for i in range(9):
        digit = extract_digit(state, i)
        if digit != 0 and GOAL_POS[digit] != i:
            cnt += 1
    return cnt


def h2(state: int) -> int:
    dist = 0
    for i in range(9):
        digit = extract_digit(state, i)
        if digit != 0:
            goal_pos = GOAL_POS[digit]
            dist += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
    return dist


def calc_h(state: int, heuristic: str) -> int:
    return h1(state) if heuristic == 'h1' else h2(state)


def score_lines_for_state(state: int, g: int, heuristic: str, alg: str):
    h = calc_h(state, heuristic)
    if alg == 'A*':
        return [f' g={g}', f' h={h}', f' f={g + h}']
    return [f' h={h}']


def print_root_with_scores(state: int, g: int, heuristic: str, alg: str):
    scores = score_lines_for_state(state, g, heuristic, alg)
    for i in range(3):
        right = scores[i] if i < len(scores) else ''
        print(state_row_text(state, i) + '   ' + right)


def print_children_tree(children: list, g_costs: dict, parent_state: int, closed: set, heuristic: str, alg: str):
    count = len(children)
    if count == 0:
        return

    total_width = count * BLOCK_WIDTH
    centers = [max(0, i * BLOCK_WIDTH + BLOCK_WIDTH // 2 - TREE_LINE_SHIFT) for i in range(count)]
    first_center = centers[0]
    last_center = centers[-1]

    print('  |')

    horiz = [' '] * total_width
    for i in range(first_center, last_center + 1):
        horiz[i] = '-'
    print(''.join(horiz).rstrip())

    pipes = [' '] * total_width
    for c in centers:
        pipes[c] = '|'
    print(''.join(pipes).rstrip())

    for row in range(3):
        parts = [state_row_text(child, row).ljust(BLOCK_WIDTH) for child in children]
        print(''.join(parts).rstrip())

    status = [' '] * total_width
    for idx, child in enumerate(children):
        child_g = g_costs[parent_state] + 1
        repeated = child in closed or (child in g_costs and child_g >= g_costs[child])
        if repeated:
            status[centers[idx]] = '✔'
    print(''.join(status).rstrip())

    rows = 3 if alg == 'A*' else 1
    for row in range(rows):
        parts = []
        for child in children:
            child_g = g_costs[parent_state] + 1
            scores = score_lines_for_state(child, child_g, heuristic, alg)
            txt = scores[row] if row < len(scores) else ''
            parts.append(txt.ljust(BLOCK_WIDTH))
        print(''.join(parts).rstrip())


def print_state_with_scores(state: int, g: int, heuristic: str, alg: str, step: int):
    grid_print([state], step)
    h = calc_h(state, heuristic)
    if alg == 'A*':
        print(f'g={g}, h={h}, f={g + h}')
    else:
        print(f'h={h}')


def trek_print(ans: list, g_costs: dict, heuristic: str, alg: str):
    path = ans[::-1]
    for i in range(len(path)):
        print_state_with_scores(path[i], g_costs[path[i]], heuristic, alg, i)
        if i != len(path) - 1:
            print('  |\n  V')


def restore_path(parents: dict, start: int, goal: int):
    ans = []
    u = goal
    while u != start:
        ans.append(u)
        u = parents[u]
    ans.append(u)
    return ans


def is_solvable(start: int, goal: int) -> bool:
    start_digits = [extract_digit(start, i) for i in range(9) if extract_digit(start, i) != 0]
    goal_digits = [extract_digit(goal, i) for i in range(9) if extract_digit(goal, i) != 0]
    start_inv = 0
    goal_inv = 0
    for i in range(len(start_digits)):
        for j in range(i + 1, len(start_digits)):
            if start_digits[i] > start_digits[j]:
                start_inv += 1
    for i in range(len(goal_digits)):
        for j in range(i + 1, len(goal_digits)):
            if goal_digits[i] > goal_digits[j]:
                goal_inv += 1
    return start_inv % 2 == goal_inv % 2


def solve(start: int, goal: int, alg='A*', heuristic='h1', mode='auto'):
    if not is_solvable(start, goal):
        return None, 0, 0, 0

    open_heap = []
    history = {start: start}
    g_costs = {start: 0}
    closed = set()
    push_cnt = 0
    time_compl = 0

    start_h = calc_h(start, heuristic)
    heapq.heappush(open_heap, (start_h, push_cnt, start))

    while len(open_heap) > 0:
        _, _, state = heapq.heappop(open_heap)
        if state in closed:
            continue

        closed.add(state)
        time_compl += 1
        children = gen_children(state)

        if mode == 'manual':
            print_root_with_scores(state, g_costs[state], heuristic, alg)
            print_children_tree(children, g_costs, state, closed, heuristic, alg)
            print()
            if input() == '0':
                return None, 0, 0, 0

        if state == goal:
            ans = restore_path(history, start, state)
            return ans, g_costs, time_compl, len(history.keys())

        for child in children:
            if child in closed:
                continue
            new_g = g_costs[state] + 1
            if child not in g_costs or new_g < g_costs[child]:
                history[child] = state
                g_costs[child] = new_g
                push_cnt += 1
                child_h = calc_h(child, heuristic)
                priority = child_h if alg == 'Greedy' else new_g + child_h
                heapq.heappush(open_heap, (priority, push_cnt, child))

    return None, 0, 0, 0


while True:
    clear_console()
    print('Начальное состояние:')
    grid_print([START_STATE])
    print('Целевое состояние:')
    grid_print([GOAL_STATE])
    print('Выберите алгоритм решения:\n'
          '1. A*\n'
          '2. Жадный поиск\n\n'
          '0. Выйти')
    x = input()
    while x not in ['0', '1', '2']:
        clear_console()
        print('Некорректный ввод!')
        print('Выберите алгоритм решения:\n'
              '1. A*\n'
              '2. Жадный поиск\n\n'
              '0. Выйти')
        x = input()

    if x == '1':
        alg = 'A*'
    elif x == '2':
        alg = 'Greedy'
    else:
        break

    clear_console()
    print(f'Алгоритм "{alg}".')
    print('Выберите эвристическую функцию:\n'
          '1. h1 — число фишек не на своем месте\n'
          '2. h2 — манхэттенское расстояние\n\n'
          '0. Выйти')
    x = input()
    while x not in ['0', '1', '2']:
        clear_console()
        print('Некорректный ввод!')
        print(f'Алгоритм "{alg}".')
        print('Выберите эвристическую функцию:\n'
              '1. h1 — число фишек не на своем месте\n'
              '2. h2 — манхэттенское расстояние\n\n'
              '0. Выйти')
        x = input()

    if x == '1':
        heuristic = 'h1'
    elif x == '2':
        heuristic = 'h2'
    else:
        break

    clear_console()
    print(f'Алгоритм "{alg}", эвристика "{heuristic}".')
    print('Выберите режим работы:\n'
          '1. Пошаговый\n'
          '2. Автоматический\n\n'
          '0. Выйти')
    x = input()
    while x not in ['0', '1', '2']:
        clear_console()
        print('Некорректный ввод!')
        print(f'Алгоритм "{alg}", эвристика "{heuristic}".')
        print('Выберите режим работы:\n'
              '1. Пошаговый\n'
              '2. Автоматический\n\n'
              '0. Выйти')
        x = input()

    if x == '1':
        mode = 'manual'
    elif x == '2':
        mode = 'auto'
    else:
        break

    clear_console()
    if mode == 'manual':
        print(f'Алгоритм "{alg}", эвристика "{heuristic}", режим "Пошаговый".')
        print('Для следующего шага нажмите любую клавишу, кроме "0"')
        print('Чтобы вернуться в меню, нажмите "0".')
        input()
        solve(START_STATE, GOAL_STATE, alg, heuristic, mode)
    else:
        print(f'Алгоритм "{alg}", эвристика "{heuristic}", режим "Автоматический".\n')
        ans, g_costs, time_compl, space_compl = solve(START_STATE, GOAL_STATE, alg, heuristic, mode)
        if ans is None:
            print('Решение не найдено.')
        else:
            trek_print(ans, g_costs, heuristic, alg)
            print('----------------------------------------------')
            print(f'Ёмкостная сложность: {space_compl}')
            print(f'Временная сложность: {time_compl}')
            print(f'Стоимость пути: {len(ans) - 1}')
            print('----------------------------------------------')
        print('Чтобы вернуться в меню, нажмите любую клавишу.')
        input()
