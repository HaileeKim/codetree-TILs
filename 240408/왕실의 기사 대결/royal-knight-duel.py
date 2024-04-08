from collections import deque
import sys

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(nr, nc, h, w):
    return h<nr+h<=L+1 and w<nc+w<=L+1

def try_move(idx, ds):
    q= deque()

    # 초기화
    for pid in range(1, N+1):
        dmg[pid] = 0
        is_moved[pid] = False
        nr[pid] = r[pid]
        nc[pid] = c[pid]

    q.append(idx)
    is_moved[idx] = True

    while q:
        x = q.popleft()
        nr[x] += dx[ds]
        nc[x] += dy[ds]

        # 보드판 나갈 경우
        if not in_range(nr[x], nc[x], h[x], w[x]):
            return False

        # 대상 기사가 함정이나 벽을 만날 경우
        for r_ in range(nr[x], nr[x]+h[x]):
            for c_ in range(nc[x], nc[x]+w[x]):
                # 함정을 만날 경우
                if board[r_][c_] == 1:
                    dmg[x] += 1
                # 벽을 만날 경우
                elif board[r_][c_] == 2:
                    return False
        
        # 대상 기사가 다른 기사를 만날 경우
        for pid in range(1, N+1):
            # 이미 움직였거나 체력이 0 이하일 경우
            if is_moved[pid] or k[pid] <= 0:
                continue

            # 체스판 범위에 벗어나면 못 움직임
            if r[pid] > nr[x] + h[x] - 1 or nr[x] > r[pid] + h[pid] - 1:
                continue
            if c[pid] > nc[x] + w[x] - 1 or nc[x] > c[pid] + w[pid] - 1:
                continue

            is_moved[pid] = True
            q.append(pid)

    dmg[idx] = 0
    return True

def knights_move(idx, ds):
    if k[idx] <= 0:
        return
    
    if try_move(idx, ds):
        for pid in range(1, N+1):
            r[pid] = nr[pid]
            c[pid] = nc[pid]
            k[pid] -= dmg[pid]


if __name__=="__main__":
    # L:체스판의 크기, N:기사의 수, Q:명령의 수 
    L, N, Q = map(int, input().split())
    MAX_N = 31  # 최대 기사 수 
    MAX_L = 41  # 최대 체스판 크기 
    board = [[0 for _ in range(MAX_L)] for _ in range(MAX_L)]    # 최대크기 체스판
    bef_k = [0 for _ in range(MAX_N)]   # 최대 개수 기사들의 초기 체력  
    r = [0 for _ in range(MAX_N)]       # 처음 기사 위치 행 
    c = [0 for _ in range(MAX_N)]       # 처음 기사 위치 열 
    h = [0 for _ in range(MAX_N)]       # 기사의 범위 세로 h 
    w = [0 for _ in range(MAX_N)]       # 기사의 범위 가로 w 
    k = [0 for _ in range(MAX_N)]       # 기사의 체력 
    nr = [0 for _ in range(MAX_N)]      # 기사가 움직일 위치 행 
    nc = [0 for _ in range(MAX_N)]      # 기사가 움질일 위치 열 
    dmg = [0 for _ in range(MAX_N)]     # 기사가 받은 데미지 
    is_moved = [False for _ in range(MAX_N)]    # 움직임 체크 

    for i in range(1, L + 1):
        board[i][1:] = map(int, input().split())
    
    # 기사 번호에 따른 각각의 정보를 리스트에 담는다?
    for pid in range(1, N + 1):
        r[pid], c[pid], h[pid], w[pid], k[pid] = map(int, input().split())
        bef_k[pid] = k[pid]

    # Q개의 왕의 명령 
    for _ in range(Q):
        idx, d = map(int, input().split())  # i번의 기사에게 방향 d로 한칸 이동하라는 명령 
        knights_move(idx, d)
        # print(k)

    # 결과를 계산하고 출력합니다.
    ans = sum([bef_k[i] - k[i] for i in range(1, N + 1) if k[i] > 0])

    print(ans)