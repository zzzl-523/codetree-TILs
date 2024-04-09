# N = 홀수, 격자 크기
# M = 도망자 수
# H = 나무 수
# K = 턴 수

def init():
    global runners, runner_board, tree_board, rail, catcher_pos, rail_reversed
    # 도망자 보드 생성
    runner_board = [[[] for _ in range(N)] for _ in range(N)]
    runners = {}
    for num in range(M):
        x, y, d = tuple(map(int, input().split()))
        x = x-1
        y = y-1
        if d==1:
            runners[num] = ((x, y, (0,1))) # 오른쪽 보고 시작
        else:
            runners[num] = ((x, y, (1,0))) # 아래 보고 시작
        runner_board[x][y].append(num)
    
    # 나무 보드 생성
    tree_board = [[0]*N for _ in range(N)]
    for _ in range(H):
        x, y = tuple(map(int, input().split()))
        x = x-1
        y = y-1
        tree_board[x][y] = 1

    # 술래 달팽이 길 생성
    rail = []
    rail_reversed = []
    catcher_pos = (N//2, N//2, (-1, 0)) # 정중앙에 위치
    rail.append(catcher_pos)
    dir = [(-1,0), (0,1), (1,0), (0,-1)]
    cnt = 0
    for i in range(N*2-1):
        if i%2==0 and i!=N*2-2:
            cnt += 1

        dx, dy = dir[i%4]
        for c in range(cnt):
            cx, cy = (rail[-1][0], rail[-1][1])          
            rail.append((cx + dx, cy + dy, (dx, dy)))
    
    for i in range(N*N-1, -1, -1):
        x, y, d = rail[i]
        rail_reversed.append((x, y, (-d[0], -d[1])))


def runners_move():
    global runners, runner_board
    for key in runners.keys():
        x, y, (dx, dy) = runners[key]
        cx, cy, X = catcher_pos

        if abs(x-cx) + abs(y-cy) > 3:
            # 술래와의 거리가 3 초과인 도망자는 이동 X
            continue

        nx, ny = x + dx, y + dy

        if 0<=nx<N and 0<=ny<N:
            # 범위 안에 있으면
            pass
        else:
            # 범위 안에 없으면
            # 방향 반대로 바꾸기
            nx, ny = x - dx, y - dy
            dx, dy = -dx, -dy
        
        # 술래 없으면 이동
        if (nx, ny) != catcher_pos[:2]:
            runners[key] = (nx, ny, (dx, dy))
            runner_board[x][y].remove(key)
            runner_board[nx][ny].append(key)


def catcher_move():
    global catcher_pos, is_reversed, catcher_move_idx
    target_rail = rail
    if is_reversed:
        # 방향 설정
        target_rail = rail_reversed
    
    next_idx = catcher_move_idx + 1
    nx = target_rail[next_idx][0]
    ny = target_rail[next_idx][1]
    dir = (0,0)
    # 방향 바로 바꾸기    
    if (nx, ny) == (0, 0):
        is_reversed = True
        next_idx = 0
        dir = rail_reversed[0][2]
    elif (nx, ny) == (N//2, N//2):
        is_reversed = False
        next_idx = 0
        dir = rail[0][2]
    else:
        if is_reversed:
            dir = target_rail[next_idx][2] 
        else: 
            dir = target_rail[next_idx+1][2] # 방향 바로 바꾸기

    catcher_pos = (nx, ny, dir)
    catcher_move_idx = next_idx


def catcher_check_caught():
    global ans, runner_board, runners
    # print("술래 pos: ", catcher_pos)
    x, y, (dx, dy) = catcher_pos
    
    cnt = 0
    for i in range(3):
        see_x, see_y = x + (dx*i), y + (dy*i)
        if see_x<0 or see_x>=N or see_y<0  or see_y>=N:
            continue

        if tree_board[see_x][see_y]:
            # 나무 있다면, 지나감
            continue

        if len(runner_board[see_x][see_y]) > 0:
            # 도망자가 있고, 나무도 없다면
            # 잡는다
            cnt += len(runner_board[see_x][see_y])
            keys = runner_board[see_x][see_y]
            for key in keys:
                del runners[key]
            runner_board[see_x][see_y] = []

    ans += t * cnt







if __name__ == '__main__':
    N, M, H, K = tuple(map(int, input().split()))
    ans = 0

    # 초기화
    runners, runner_board, tree_board = [], [], []
    rail, rail_reversed = [], []
    catcher_pos = []
    catcher_move_idx = 0
    is_reversed = False

    init()

    for t in range(1, K+1):
        # 도망자 이동
        runners_move()

        # 술래 이동
        catcher_move()
        # 술래 시야 확인
        catcher_check_caught()
    
    print(ans)