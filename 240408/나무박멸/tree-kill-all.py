# N = 격자의 크기
# M = 박멸 진행 년 수
# K = 제초제 확산 범위
# C = 제초제 남아있는 년 수


def init():
    # 나무 위치 배열
    for i in range(N):
        for j in range(N):
            if board[i][j] > 0:
                trees.append((i, j))


def grow_and_breed():
    global trees
    blank_list = []
    for x, y in trees:
        # 1) 성장
        cnt = 0     # 인접한 나무 개수 = 성장할 나무 개수
        blanks = [] # 빈칸 개수 = 번식할 나무 개수 

        for dx, dy in dir:
            nx = x + dx
            ny = y + dy

            # 벗어나거나
            if nx<0 or nx>=N or ny<0 or ny>=N:
                continue
            # 벽 or 제초제인 경우
            if board[nx][ny] < 0 or remove_map[nx][ny] < 0:
                continue
            
            # 빈칸인 경우
            if board[nx][ny] == 0:
                blanks.append((nx, ny))
                continue
            
            # 나무 있는 경우
            cnt += 1    # 인접한 나무 개수 == 성장하는 나무 개수
    
        board[x][y] += cnt
        blank_list.append(blanks)

    # print("성장: ")
    # print(*board, sep='\n')


    # 2) 번식
    for idx, blanks in enumerate(blank_list):
        blanks = set(blanks)
        tx, ty = trees[idx]
        for bx, by in blanks:
            board[bx][by] += board[tx][ty] // len(blanks)
            trees.append((bx, by))
    
    trees = list(set(trees))
    trees.sort()
    # print(trees)

    # print("번식: ")
    # print(*board, sep='\n')
    # print("=======================")
    
    # print(*board, sep='\n')
    # print("=======================")


def remove():
    global ans

    max_value = 0
    max_pos = (-1, -1)

    # 제초제 뿌릴 나무 찾기
    for x, y in trees:
        # 대각선 확인
        cnt = board[x][y]
        ck = [True, True, True, True]

        for k in range(1, K+1):
            arr = [(x+k, y+k), (x-k, y-k), (x+k, y-k), (x-k, y+k)]
            for idx, (nx, ny) in enumerate(arr):
                if ck[idx] == False:
                    continue

                ck[idx] = find_remove_tree(nx, ny, ck[idx])
                if ck[idx] and ((nx, ny) in trees):
                    cnt += board[nx][ny]

        # 박멸 최대 개수인 위치 찾기
        if cnt > max_value:
            max_pos = (x, y)
            max_value = cnt
    
    # print("제초제: ", max_pos, max_value)
    # 제초제 뿌리기
    if max_pos == (-1, -1):
        # 더이상 나무 없음
        return

    else:
        ans += max_value
        x, y = max_pos
        expire_year = -C-1

        # 제초제 뿌린 곳
        remove_map[x][y] = expire_year
        board[x][y] = 0
        trees.remove((x, y))

        # 전파
        ck = [True, True, True, True]
        for k in range(1, K+1):
            arr = [(x+k, y+k), (x-k, y-k), (x+k, y-k), (x-k, y+k)]
            for i, (nx, ny) in enumerate(arr):
                if ck[i]==False:
                    continue
                ck[i] = spread_remove_map(nx, ny, ck[i])

def find_remove_tree(x, y, ck):
    if 0<=x<N and 0<=y<N and ck:
        if board[x][y] == -1:
            return False
        if board[x][y] == 0:
            return False
    else:
        ck = False
    
    return ck

def spread_remove_map(x, y, ck):
    expire_year = -C-1
    if 0<=x<N and 0<=y<N and ck:
        if board[x][y] == -1:
            return False
        if board[x][y] == 0:
            remove_map[x][y] = expire_year
            return False


        remove_map[x][y] = expire_year
        board[x][y] = 0
        if (x, y) in trees:
            trees.remove((x, y))
    else:
        ck = False
    
    return ck

def update_remove_map():
    for i in range(N):
        for j in range(N):
            if remove_map[i][j] < 0:
                remove_map[i][j] += 1



if __name__ == '__main__':
    N, M, K, C = tuple(map(int, input().split()))
    board = [list(map(int, input().split())) for _ in range(N)]

    trees = []
    dir = [(0,1), (1,0), (-1,0), (0,-1)]

    remove_map = [[0]*N for _ in range(N)]
    ans = 0

    init()
    for t in range(1, M+1):
        # 제초제 갱신   
        update_remove_map()

        # 성장 & 번식
        grow_and_breed()

        # 제초제 뿌리기
        remove()

        # print("BOARD")
        # print(*board, sep='\n')
        # print("REMOVE_MAP")
        # print(*remove_map, sep='\n')
        # print("TREES")
        # print(trees, sep='\n')
    
    print(ans)