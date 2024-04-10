class group:
    def __init__(self, idx, value, cnt, neighbor, start_pos):
        self.idx = idx
        self.value = value
        self.cnt = cnt
        self.neighbor = neighbor
        self.start_pos = start_pos
    
    def print(self):
        print("idx: ",self.idx, end=' / ')
        print("value: ",self.value, end=' / ')
        print("cnt: ",self.cnt, end=' / ')
        print("neighbor: ",self.neighbor)
        print("start_pos: ", self.start_pos)


def init():
    global groups, group_board
    # 1) 그룹 배열 생성
    # 그룹 번호는 0번부터
    groups = []
    group_board = [[-1]*N for _ in range(N)]
    visited = [[False]*N for _ in range(N)]
    d_xy = [(0,1), (1,0), (0,-1), (-1,0)]
    idx = -1
    q = deque()
    for i in range(N):
        for j in range(N):
            # 이미 방문했으면 건너뛰기
            if visited[i][j]:
                continue
            
            # 최초 방문이면 그룹 배열에 추가 & 방문 표시
            cnt = 1
            idx += 1
            q.append((i,j))
            visited[i][j] = True
            group_board[i][j] = idx
            # 그룹 생성
            tmp = group(idx, board[i][j], cnt, {}, (i, j))

            while q:
                x, y = q.popleft()
                for dx, dy in d_xy:
                    nx = x + dx
                    ny = y + dy

                    if nx<0 or nx>=N or ny<0 or ny>=N:
                        continue
                    if board[x][y] != board[nx][ny]:
                        # 다른 숫자 만나면 이웃 추가해야하지만, 아직 번호 모르므로 넘어감
                        continue
                    if visited[nx][ny]:
                        continue
                    
                    # 같은 그룹이면 추가
                    q.append((nx, ny))
                    cnt += 1
                    visited[nx][ny] = True
                    group_board[nx][ny] = idx
            
            tmp.cnt = cnt
            groups.append(tmp)
    
    # for item in groups:
    #     print(item.print())
    # print(*group_board, sep='\n')

    # print("<이웃 추가>")
    # 2) 그룹 조합 & 맞닿는 변 개수 구하기
    visited = [[False]*N for _ in range(N)]
    q = deque()
    for item in groups:
        gx, gy = item.start_pos
        
        q.append((gx, gy))
        visited[gx][gy] = True
        while q:
            x, y = q.popleft()
            
            for dx, dy in d_xy:
                nx = x + dx
                ny = y + dy

                if nx<0 or nx>=N or ny<0 or ny>=N:
                    continue
                
                if group_board[x][y]!=group_board[nx][ny]:
                    # 다른 그룹을 만나면 => 이웃에 추가
                    neighbor_idx = group_board[nx][ny]
                    
                    if neighbor_idx not in item.neighbor.keys():
                        ## 아직 이웃에 없으면 추가
                        item.neighbor[neighbor_idx] = 1
                    else:
                        ## 있으면 증가
                        item.neighbor[neighbor_idx] += 1

                    continue

                if visited[nx][ny]:
                    continue


                # print("현재 idx: ", item.idx, "추가되는 것: ", (nx, ny))
                # 같은 그룹만 큐에 추가
                q.append((nx, ny))
                visited[nx][ny] = True
        

    # for item in groups:
    #     item.print()            
    #     print("================")


# 예술점수 계산 함수
def calc_score():
    score = 0
    for item in groups:
        # 그룹 조합
        for key in item.neighbor.keys():
            # 조화로움 값 합 구하기
            A = item
            B = groups[key]

            # print("조합")
            # print("A, B", A.idx, B.idx)
            # print("A: ", A.cnt, A.value, A.neighbor)
            # print("B: ", B.cnt, B.value, B.neighbor)
            # print((A.cnt + B.cnt) * (A.value * B.value) * A.neighbor[key])
            score += (A.cnt + B.cnt) * (A.value * B.value) * A.neighbor[key]
            B.neighbor[item.idx] = 0    # 중복 방지

    return score


# 그림 회전 함수
# board만 바꿔주고 다시 init하기
def rotate():
    global board
    # 1) 십자로 구역 나누기
    new_board = [[0]*N for _ in range(N)]
    # print("MINI: ")
    # print(*mini_board1, sep='\n')
    # print()
    # print(*mini_board2, sep='\n')
    # print()
    # print(*mini_board3, sep='\n')
    # print()
    # print(*mini_board4, sep='\n')
    # print("----------------------")
    
    (cx, cy) = (N//2, N//2) # center_pos
    ## 십자 부분
    for i in range(N):
        new_board[i][cy] = board[i][cy]
        new_board[cx][i] = board[cx][i]

    # 2) board를 전체 90도 회전 (시계)
    # mini_board1 = [board[i][:N//2] for i in range(N//2)]
    mini_board1 = rotate_clock([board[i][:N//2] for i in range(N//2)])
    # mini_board1 = rotate_clock(mini_board1)
    mini_board2 = rotate_clock([board[i][(N//2)+1:] for i in range(N//2)])
    mini_board3 = rotate_clock([board[i][:N//2] for i in range((N//2)+1, N)])
    mini_board4 = rotate_clock([board[i][(N//2)+1:] for i in range((N//2)+1, N)])

    # 3) 십자 부분을 전체 -90도 회전 (반시계)
    new_board = rotate_counter_clock(new_board)

    # 4) 합치기
    for i in range(N):
        for j in range(N):
            if j!=N//2:
                if i<N//2:
                    if j<N//2:
                        new_board[i][j] = mini_board1[i][j]
                    else:
                        new_board[i][j] = mini_board2[i][(N//2+1)-j]
                elif i>N//2:
                    if j<N//2:
                        new_board[i][j] = mini_board3[(N//2+1) - i][j]
                    else:
                        new_board[i][j] = mini_board4[(N//2+1) - i][(N//2+1)-j]
                    
    board = new_board
    # print()
    # print(*new_board, sep='\n')

# 시계방향회전
def rotate_clock(mat):
    size = len(mat)
    tmp = [[0]*size for _ in range(size)]

    # 복제
    for i in range(size):
        for j in range(size):
            tmp[i][j] = mat[i][j]
    
    # 회전
    for i in range(size):
        for j in range(size):
            max_size = size-1
            tmp[j][max_size-i] = mat[i][j]
            tmp[max_size-i][max_size-j] = mat[j][max_size-i]
            tmp[max_size-j][i] = mat[max_size-i][max_size-j] 
            tmp[i][j] = mat[max_size-j][i]
    
    return tmp
    

# 반시계방향회전
def rotate_counter_clock(mat):
    size = len(mat)
    tmp = [[0]*size for _ in range(size)]

    # 복제
    for i in range(size):
        for j in range(size):
            tmp[i][j] = mat[i][j]
    
    # 회전
    for i in range(size):
        for j in range(size):
            max_size = size-1
            tmp[i][j] = mat[j][max_size-i]
            tmp[j][max_size-i] = mat[max_size-i][max_size-j]
            tmp[max_size-i][max_size-j] = mat[max_size-j][i]
            tmp[max_size-j][i] = mat[i][j]
    
    return tmp

    
if __name__ == '__main__':
    from collections import deque

    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    groups, group_board = [], []
    ans = 0

    # 초기화
    init()

    # 초기 예술 점수
    ans += calc_score()

    # 회전 3번
    for t in range(3):
        rotate()
        init()
        ans += calc_score()

    print(ans)