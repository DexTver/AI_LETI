from collections import deque


def platon(a):  # find zero
    for i in range(3):
        for j in range(3):
            if a[i][j] == 0:
                return i, j
    return -1, -1


def vika(a):  # int from list
    x = 0
    for i in range(9):
        x = x * 10 + a[i // 3][i % 3]
    return x


def akiv(x):  # list from int
    a = [[0, 0, 0] for _ in range(3)]
    for i in range(9):
        a[i // 3][i % 3] = x % 10 ** (9 - i) // 10 ** (8 - i)
    return a


def nastya(ans):  # print steps
    step = 0
    for u in ans[::-1]:
        print(*akiv(u)[0])
        print(*akiv(u)[1], end="\tШаг ")
        print(step)
        step += 1
        print(*akiv(u)[2])
        if step < len(ans):
            print("  |")
            print("  v")


def ignat(x):  # find children
    a = akiv(x)
    i, j = platon(a)
    ans = list()
    if i - 1 >= 0:
        a[i - 1][j], a[i][j] = a[i][j], a[i - 1][j]
        ans.append(vika(a))
        a[i - 1][j], a[i][j] = a[i][j], a[i - 1][j]
    if j - 1 >= 0:
        a[i][j - 1], a[i][j] = a[i][j], a[i][j - 1]
        ans.append(vika(a))
        a[i][j - 1], a[i][j] = a[i][j], a[i][j - 1]
    if j + 1 < 3:
        a[i][j + 1], a[i][j] = a[i][j], a[i][j + 1]
        ans.append(vika(a))
        a[i][j + 1], a[i][j] = a[i][j], a[i][j + 1]
    if i + 1 < 3:
        a[i + 1][j], a[i][j] = a[i][j], a[i + 1][j]
        ans.append(vika(a))
        a[i + 1][j], a[i][j] = a[i][j], a[i + 1][j]
    return ans


def old_bfs(x, y):
    bfs_his = dict()
    q = deque()
    q.append(x)
    bfs_ans = list()

    while len(q) > 0:
        u = q.popleft()
        if u == y:
            while u != x:
                bfs_ans.append(u)
                u = bfs_his[u]
            bfs_ans.append(u)
            break
        for v in ignat(u):
            if v not in bfs_his.keys():
                bfs_his[v] = u
                q.append(v)

    print("Поиск в ширину:")
    nastya(bfs_ans)


def old_dfs(x, y):
    dfs_his = dict()
    d = deque()
    d.appendleft(x)
    dfs_ans = list()
    while len(d) > 0:
        u = d.popleft()
        if u == y:
            while u != x:
                dfs_ans.append(u)
                u = dfs_his[u]
            dfs_ans.append(u)
            break
        for v in ignat(u):
            if v not in dfs_his.keys():
                dfs_his[v] = u
                d.appendleft(v)

    print("\n\nПоиск в глубину:")
    nastya(dfs_ans)


old_bfs(583402761, 123456780)
old_dfs(583402761, 123456780)