from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

L, N, Q = map(int, input().split())

board = [[0] * ( L + 1) for _ in range(L+1)]

r = [0] * (N+1)
c = [0] * (N+1)
h = [0] * (N+1)
w = [0] * (N+1)
k = [0] * (N+1)

nr = [0] * (N+1)
nc = [0] * (N+1)
dmg = [0] * (N+1)
init_k = [0] * (N+1)
is_moved = [False] * (N+1)

for i in range(1, L + 1):
    board[i][1:] = map(int, input().split())

for i in range(1, N + 1):
    r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    init_k[i] = k[i]

def try_movement(idx, d):
    q = deque()

    for i in range(1, N+1):
        nr[i] = r[i]
        nc[i] = c[i]
        dmg[i] = 0
        is_moved[i] = False

    q.append(idx)
    is_moved[idx] = True

    while q:
        x = q.popleft()
        
        nr[x] += dr[d]
        nc[x] += dc[d]

        if nr[x] < 1 or nc[x] < 1 or nr[x] > L - h[x] + 1 or nc[x] > L - w[x] + 1:
            return False
        
        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                if board[i][j] == 1:
                    dmg[x] += 1
                if board[i][j] == 2:
                    return False
        
        for i in range(1, N + 1):
            if is_moved[i] or k[i] <= 0:
                continue
            if r[i] > nr[x] + h[x] - 1 or nr[x] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] - 1 or nc[x] > c[i] + w[i] - 1:
                continue
            q.append(i)
            is_moved[i] = True

    dmg[idx] = 0
    return True

def move_knights(idx, d):
    if k[idx] <= 0:
        return
    if try_movement(idx, d):
        for i in range(1, N+1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

for _ in range(Q):
    idx, d = map(int, input().split())
    move_knights(idx, d)

# 결과를 계산하고 출력합니다.
ans = sum([init_k[i] - k[i] for i in range(1, N + 1) if k[i] > 0])
print(ans)