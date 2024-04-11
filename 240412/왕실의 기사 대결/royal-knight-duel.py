from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

def in_range(r,c,h,w):
    return 0< r <= L - h + 1 and 0 < c <= L - w + 1

# 기사 이동
def try_movement(idx, d):
    q = deque()

    # 초기화
    for i in range(1, N + 1):
        is_moved[i] = False
        nr[i] = r[i]
        nc[i] = c[i]
        dmg[i] = 0

    q.append(idx)
    is_moved[idx] = True

    while q:
        x = q.popleft()

        nr[x] += dr[d]
        nc[x] += dc[d]

        # 이동하려는 지역이 체스판을 벗어나는 가
        if not in_range(nr[x], nc[x], h[x], w[x]):
            return False

        for r_ in range(nr[x], nr[x] + h[x]):
            for c_ in range(nc[x], nc[x] + w[x]):
                # 이동하려는 지역에 함정이 있는가
                if board[r_][c_] == 1:
                    dmg[x] += 1
                # 이동하려는 지역에 벽이 있는가
                if board[r_][c_] == 2:
                    return False
                    
        # 이동하려는 지역에 기사가 있는가
        for i in range(1, N+1):
            if is_moved[i] or k[i] <= 0:
                continue
            if r[i] > nr[x] + h[x] - 1 or nr[x] > r[i] + h[i] - 1:
                continue
            if c[i] > nc[x] + w[x] - 1 or nc[x] > c[i] + w[i] - 1:
                continue

            is_moved[i] = True
            q.append(i)
        
    dmg[idx] = 0
    return True

def move_knights(idx, d):
    if k[idx] <= 0:
        return
    
    if try_movement(idx, d):
        for i in range(1, N + 1):
            r[i] = nr[i]
            c[i] = nc[i]
            k[i] -= dmg[i]

if __name__ == "__main__":
    L, N, Q = map(int, input().split())

    board = [[0] * (L + 1) for _ in range(L + 1)]

    r = [0] * (N + 1)
    c = [0] * (N + 1)
    h = [0] * (N + 1)
    w = [0] * (N + 1)
    k = [0] * (N + 1)
    nr = [0] * (N + 1)
    nc = [0] * (N + 1)
    dmg = [0] * (N + 1)
    init_k = [0] * (N + 1)
    is_moved = [False for _ in range(N + 1)]

    for i in range(1, L + 1):
        board[i][1:] = list(map(int, input().split()))

    for i in range(1, N+1):
        r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
        init_k[i] = k[i]

    for q in range(Q):
        idx, d = map(int, input().split())
        move_knights(idx, d)

    ans = sum([init_k[i] - k[i] for i in range(1, N + 1) if k[i] > 0])
    print(ans)