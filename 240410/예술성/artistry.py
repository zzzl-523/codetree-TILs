class group:
    def __init__(self, idx, value, cnt, neighbor):
        self.idx = 0
        self.value = 0
        self.cnt = 0
        self.neighbor = {}


def init():
    global groups, group_board
    # 그룹 배열 생성
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
            cnt = 0
            idx += 1
            q.append((i,j))
            visited[i][j] = True
            group_board[i][j] = idx
            # 그룹 생성
            tmp = group(idx, board[i][j], cnt, {})

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
                    
    print(groups)
    print(*group_board, sep='\n')


    
if __name__ == '__main__':
    from collections import deque

    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    groups, group_board = [], []

    init()