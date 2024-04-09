import sys
from collections import deque
import copy

# 상하좌우
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def in_range(r, c, h, w):
    return 0<r<=L-h+1 and 0<c<=L-w+1

# def try_movement(idx, d):
    
#     q = deque()

#     # 초기화
#     for pid in range(1, N+1):
#         nr[pid] = r[pid]
#         nc[pid] = c[pid]
#         dmg[pid] = 0
#         is_moved[pid] = False

#     q.append(idx)
#     is_moved[idx] = True

#     while q:
#         x = q.popleft()

#         nr[x] += dx[d]
#         nr[x] += dy[d]

#         # 범위를 나갔다면 -> 이동 불가
#         if not inrange(nr[x], nc[x], h[x], w[x]):
#             return False

#         # 함정이 있다면 -> 데미지 입음
#         # 벽이 있다면 -> 이동 불가
#         for sr in range(nr[x], nr[x] + h[x]):
#             for sc in range(nc[x], nc[x] + w[x]):
#                 if board[sr][sc] == 1:
#                     dmg[x] += 1
#                 if board[sr][sc] == 2:
#                     return False

#         # 밀려나는 칸에 기사가 있다면 -> 그 기사도 움직여야 함 (재귀함수)
#         for pid in range(1, N+1):
#             # 이미 이동했거나 체력이 0일 경우 이동 불가
#             if is_moved[pid] or k[pid] <= 0:
#                 continue
#             # 체스판 범위에 벗어나면 이동 불가
#             if r[pid] > nr[x] + h[x] - 1 or nr[x] > r[pid] + h[pid] - 1:
#                 continue
#             if c[pid] > nc[x] + w[x] - 1 or nc[x] > c[pid] + w[pid] - 1:
#                 continue

#             is_moved[pid] = True
#             q.append(pid)

#     dmg[idx] = 0
#     return True

# 움직임을 시도해봅니다.
def try_movement(idx, dir):
    q = deque()

    # 초기화 작업입니다.
    for pid in range(1, N + 1):     # 1번 기사부터 N번 기사까지 
        dmg[pid] = 0                # 받은 데미지 0으로 초기화 
        is_moved[pid] = False       # 움직임 False로 초기화 
        nr[pid] = r[pid]            # temporal r을 일단 현재 위치 r로 초기화
        nc[pid] = c[pid]            # temporal r을 일단 현재 위치 r로 초기화

    q.append(idx)
    is_moved[idx] = True            # 모체 기사를 기준으로 움직임 시작 

    while q:                        # 현재 시작 기사를 시작으로 딸려오는 연쇄작용이 일어나는 다음 기사들이 append로 쌓음
        x = q.popleft()

        nr[x] += dx[dir]            # 새로운, 움직일 위치 
        nc[x] += dy[dir]

        # 경계를 벗어나는지 체크합니다.
        if not in_range(nr[x],nc[x],h[x],w[x]):
            return False        # 범위를 벗어나는 움직임이면 못 움직임

        # 대상 기사가 함정이나 벽과 충돌하는지 검사합니다.
        for i in range(nr[x], nr[x] + h[x]):
            for j in range(nc[x], nc[x] + w[x]):
                if board[i][j] == 1:     # 함정이면 
                    dmg[x] += 1         # 데미지 축적 
                if board[i][j] == 2:     # 벽이 하나라도 있으면 
                    return False        # 못 움직임 

        # 대상 기사가 다른 기사와 충돌하는 경우, 해당 조각도 같이 이동합니다.
        for pid in range(1, N + 1):
            if is_moved[pid] or k[pid] <= 0:    # 이미 움직였거나, 체력이 0이하라 체스판에 없는 경우 
                continue                        # 안움직임 
            # 체스판 범위에 벗어나면 못 움직임
            if r[pid] > nr[x] + h[x] - 1 or nr[x] > r[pid] + h[pid] - 1:
                continue
            if c[pid] > nc[x] + w[x] - 1 or nc[x] > c[pid] + w[pid] - 1:
                continue

            is_moved[pid] = True
            # 연쇄적으로 움직이게 하기 위해 큐를 사용 
            q.append(pid)       # 그 다음 움직여야 할 기사 pid         

    # return False 없이 여기까지 무사히 도달했으면 
    dmg[idx] = 0        
    return True

def move_knights(idx, d):

    # 기사의 체력이 0이하 일 경우 이동 불가
    if k[idx] <= 0:
        return 

    # 이동이 가능한 경우
    if try_movement(idx, d):
        for pid in range(1, N+1):
            r[pid] = nr[pid]
            c[pid] = nc[pid]
            k[pid] -= dmg[pid]
            print(pid, dmg[pid])


if __name__ == "__main__":
    max_L = 41
    max_N = 31
    max_Q = 100
    max_k = 100

    board = [[0]*max_L for _ in range(max_L)]
    Q_order = [[0, 0] for _ in range(max_Q)]
    r = [0] * max_N
    c = [0] * max_N
    nr = [0] * max_N
    nc = [0] * max_N
    h = [0] * max_N
    w = [0] * max_N
    k = [0] * max_N
    init_k = [0] * max_N
    dmg = [0] * max_N
    is_moved = [0] * max_N

    L,N,Q = map(int, input().split())
    for i in range(1, L+1):
        board[i][1:] = list(map(int, input().split()))
    for i in range(1, N+1):
        r[i], c[i], h[i], w[i], k[i] = map(int, input().split())
    
    init_k = copy.deepcopy(k)

    for _ in range(Q):
        idx, direction = map(int, input().split())
        move_knights(idx, direction)

    ans = 0

    print(init_k, k)
    for i in range(1, N+1):
        if k[i] > 0:
            ans += init_k[i] - k[i]

    print(ans)