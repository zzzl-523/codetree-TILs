# N : 격자 크기
# M : 팀의 개수
# K : 라운드 수

N = 0
M = 0
K = 0
board = []
starter_list = []
score = 0

def solution(t):
    global score
    # 머리사람 따라서 이동
    dir = [(0,1), (-1,0), (0,-1), (1,0)]
    for dx, dy in starter_list:
        q = deque([(dx, dy, (0, 0), 1)])
        while q:
            x, y, prev_dir, cnt = q.popleft()
            for dx, dy in dir:
                nx = x + dx
                ny = y + dy
    
                if nx<0 or nx>=N or ny<0 or ny>=N:
                    continue
                if board[nx][ny][0] == 0:
                    continue
                if (-prev_dir[0], -prev_dir[1]) == (dx, dy):
                    continue

                
                new = board[nx][ny][0]
                if new == 4:
                    board[x][y] = [2, 2]    # 맨 처음 1
                    board[nx][ny] = [1, 1]  # 2번
                elif new == 2:
                    board[x][y] = [2, cnt+1]
                    q.append((nx, ny, (dx, dy), board[x][y][1]))  # 큐에 추가
                elif new == 3:
                    board[x][y] = [3, cnt+1]
                    board[nx][ny] = [4, 0]
                    break

                # print(*board, sep='\n')
    # 1회 이동 상태
    # print(*board, sep='\n')

    # 2) 공 던지기
    arrow = dir[t//K]
    for i in range(N):
        if arrow[1] and 0<board[t%N][i][0]<4:    # 던지기 방향 왼, 오
            # 사람 마주침
            score += board[t%N][i][1]**2
            break
        
        if arrow[0] and 0<board[i][t%N][0]<4:    # 던지기 방향 왼, 오
            score += board[i][t%N][1]**2
            break


    print(score)
                

if __name__ == '__main__':
    from collections import deque

    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    score = 0

    # 1) 이동
    # 전체 for문을 돌며 1의 위치 찾기
    for i in range(N):
        for j in range(N):
            board[i][j] = [board[i][j], 0]
            if board[i][j][0] == 1:
                starter_list.append((i,j))

    for t in range(K):
        solution(t)