import sys
import copy

ds = [[-1, 0], [1, 0], [0, -1], [0, 1]] # (r, c)

def print_board():
    for i in range(N+1):
        print(board[i])

def min_distance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)

def in_range(r, c):
    return 0<r<N+1 and 0<c<N+1

def try_movement(exit):
    
    # print(people_arr)
    global M, visited
    for pid in range(M):
        # 현재 칸과 출구까지의 최단 거리
        x1 = people_arr[pid][0]
        y1 = people_arr[pid][1]
        x2 = exit[0]
        y2 = exit[1]
        cur_dist = min_distance(x1,x2,y1,y2)    

        # 상하좌우 확인
        for dr, dc in ds:
            # 상하좌우 칸과 출구까지의 최단 거리
            n_r = people_arr[pid][0] + dr
            n_c = people_arr[pid][1] + dc
            distance = min_distance(n_r,x2,n_c,y2)
            # 현재 칸보다 출구까지의 최단 거리가 가깝고 벽이 아닐 경우 이동
            # print(x1, y1, n_r, n_c, cur_dist, distance)
            if cur_dist > distance and board[n_r][n_c] <= 0 and in_range(n_r, n_c):
                board[x1][y1] = 0           # 사람 있던 칸은 빈칸으로 변경
                people_arr[pid][0] = n_r
                people_arr[pid][1] = n_c
                dist[pid] += 1
                # print("이동 ", x1, y1)
                # 출구로 이동한 경우
                if board[n_r][n_c] == -2:
                    people_arr[pid] = [0, 0]
                    M -= 1
                    # print(people_arr)
                # 출구로 이동 못 한 경우
                else:
                    board[n_r][n_c] = -1        # 참가자가 있는 칸은 -1 로 표시
                    # print(x1, y1, n_r, n_c)
                    
                break

            # 이동 못한 경우
            else:
                board[x1][y1] = -1        # 참가자가 있는 칸은 -1 로 표시
                # print(x1, y1)
        visited.add((people_arr[pid][0], people_arr[pid][1]))

# 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기
# 1. r 좌표가 작은 것이 우선 
# 2. c 좌표가 작은 것이 차선
def find_square():
    flag = False
    global visited
    # print(people_arr)
    
    # print("visited : ", visited)
    # print("people : ", people_arr)
    for n in range(2, N):
        for s_r in range(1, N - n + 1):
            for s_c in range(1, N - n + 1):
                r = s_r + n - 1
                c = s_c + n - 1
                if s_r <= exit[0] <= r and s_c <= exit[1] <= c:
                    for pid_r, pid_c in visited:
                        if s_r <= pid_r <= r and s_c <= pid_c <= c:
                            start = [s_r, s_c]
                            end = [r, c]
                            flag = True

                if flag: 
                    break
            if flag: 
                break
        if flag: 
            break
    # print(s_r, s_c, n)
    return s_r, s_c, n

# 미로 90도 회전
def rotate_90(s_r, s_c, n):
    rotate = copy.deepcopy(board)
    global people_arr, exit
    # 90도 회전

    #r = 2, c= 1, n = 3
    for r in range(s_r, s_r + n):
        for c in range(s_c, s_c + n):
            o_r, o_c = r - s_r, c - s_c
            r_r, r_c = o_c, n - o_r - 1
            rotate[r_r + s_r][r_c + s_c] = board[r][c]
            if rotate[r_r + s_r][r_c + s_c] >= 1: # 벽 내구도 감소
                rotate[r_r + s_r][r_c + s_c] -= 1
            # print(r,c,r_r + s_r, r_c + s_c, rotate[r_r + s_r][r_c + s_c])

    people_arr = []

    for r in range(1, N + 1):
        for c in range(1, N + 1):
            if rotate[r][c] == -1: # 참가자 위치 재정의
                people_arr.append([r,c])
            if rotate[r][c] == -2: # exit 찾기
                exit = [r,c]

    # print(people_arr)

    # print("rotate ", " : ")
    # for i in range(N+1):
    #     print(rotate[i])
    # print("\n")

    return rotate

if __name__ == "__main__":
    max_N = 11
    max_M = 11
    mak_K = 100
    exit = [0, 0]
    board = [[0]*max_N for _ in range(max_N)]
    people_arr = [[0,0] for _ in range(max_M)]
    dist = [0] * max_M

    # 입력
    N, M, K = map(int, input().split())
    board = [[0]*(N+1) for _ in range(N+1)]
    for i in range(1, N+1):
        board[i][1:] = list(map(int, input().split()))
    for i in range(M):
        people_arr[i] = list(map(int, input().split()))
    exit = list(map(int, input().split()))

    # print(board)

    # 출구는 -2 로 표시
    board[exit[0]][exit[1]] = -2
    # print(people_arr)
    for i in range(K):
        # 참가자가 모두 미로 탈출했을 때 -> break
        # print(board)
        # print("k = ", i)
        
        visited = set()
        try_movement(exit)

        if len(people_arr) == 0:
            break

        # print("try move ", i, " : ")
        # print_board()
        # print("\n")

        sqr_r, sqr_c, n = find_square()

        board = rotate_90(sqr_r, sqr_c, n)

    print(sum(dist))
    
    print(exit[0], exit[1])