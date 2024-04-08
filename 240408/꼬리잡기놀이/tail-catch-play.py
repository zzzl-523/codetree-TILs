# N : 격자 크기
# M : 팀의 개수
# K : 라운드 수

N = 0
M = 0
K = 0
board = []
starter_list = []
score = 0
head_reverse = False
one_list = []
three_list = []

def solution(t):
    global score, head_reverse
    # 머리사람 따라서 이동
    dir = [(0,1), (-1,0), (0,-1), (1,0)]
    for idx, xy in enumerate(starter_list):
        q = deque([(xy[0], xy[1], (0, 0), 1)])
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
                    one_list[idx] = [nx, ny]
                    starter_list[idx] = [nx, ny]
                elif new == 2:
                    board[x][y] = [2, cnt+1]
                    q.append((nx, ny, (dx, dy), board[x][y][1]))  # 큐에 추가
                elif new == 3:
                    board[x][y] = [3, cnt+1]
                    board[nx][ny] = [4, 0]
                    three_list[idx] = [x, y]
                    break

                # print(*board, sep='\n')
    # 1회 이동 상태
    # print(*board, sep='\n')
    

    # 2) 공 던지기
    arrow = dir[t//N]
    garo, sero = -1, -1
    for i in range(N): 
        if arrow[1]: # 던지기 방향 왼, 오
            if arrow[1] < 0: # 왼쪽
                garo = -i-1
                sero = -(t%N)-1
                # print(t+1,"번째 라운드", " 방향: 왼쪽", garo,"번째 라인")
            else: # 오른쪽
                garo = i
                sero = t%N
                # print(t+1,"번째 라운드", " 방향: 오른쪽", garo,"번째 라인")
        
        elif arrow[0]:
            if arrow[0] < 0:
                sero = -i-1
                garo = t%N
                # print(t+1,"번째 라운드", " 방향: 위", sero,"번째 라인")
            else:
                sero = i
                garo = -(t%N)-1
                # print(t+1,"번째 라운드", " 방향: 아래", sero,"번째 라인")

        if 0<board[sero][garo][0]<4:    
            # 사람 마주침
            score += board[sero][garo][1]**2
            team_num = board_idx[sero][garo]
            
            # 머리-꼬리 바꾸기
            starter_list[team_num-1] = three_list[team_num-1]
            one_xy = one_list[team_num-1]
            three_xy = three_list[team_num-1]
            board[one_xy[0]][one_xy[1]], board[three_xy[0]][three_xy[1]]  = board[three_xy[0]][three_xy[1]], board[one_xy[0]][one_xy[1]]

            break


    # print("점수: ",score)

if __name__ == '__main__':
    from collections import deque

    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    score = 0
    head_reverse = False
    one_list = [(0,0) for _ in range(M)]
    three_list = [(0,0) for _ in range(M)]
    starter_list = [(0,0) for _ in range(M)]

    # 0) 팀별 레일 표시하기
    dir = [(0,1), (-1,0), (0,-1), (1,0)]
    visited = [[False]*N for _ in range(N)]
    board_idx = [[0]*N for _ in range(N)]
    q = deque([])
    number = 0
    for i in range(N):
        for j in range(N):
            if visited[i][j] or board[i][j]==0:
                continue

            q.append((i, j))
            visited[i][j] = True
            number += 1
            board_idx[i][j] = number

            while q:
                x, y = q.popleft()
                for dx, dy in dir:
                    nx = x + dx
                    ny = y + dy

                    if nx<0 or nx>=N or ny<0 or ny>=N:
                        continue
                    if board[nx][ny] == 0:
                        continue
                    if visited[nx][ny]:
                        continue

                    
                    q.append((nx, ny))
                    visited[nx][ny] = True
                    board_idx[nx][ny] = number

    # print(*board_idx, sep='\n')
    # 1) 이동
    # 전체 for문을 돌며 1의 위치 찾기
    for i in range(N):
        for j in range(N):
            board[i][j] = [board[i][j], 0]
            if board[i][j][0] == 1:
                team_num = board_idx[i][j]
                one_list[team_num-1] = [i,j]
                starter_list[team_num-1] = [i,j]
    
    for t in range(K):
        solution(t)
    
    print(score)