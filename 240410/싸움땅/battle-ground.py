# N = 격자의 크기
# M = 플레이어의 수
# K = 라운드의 수

class Player():
    def __init__(self, pos, d, s):
        self.idx = -1
        self.pos = pos
        self.direction = d
        self.hp = s
        self.gun = 0
        self.point = 0

    def print(self):
        print("---Player ", self.idx, " info---")
        print("pos: ", self.pos)
        print("direction: ", self.direction)
        print("hp: ", self.hp)
        print("gun: ", self.gun)
        print("point: ", self.point)

def func(num):
    if int(num)==0:
        return []
    return [int(num)]

# 1) Init
def init():
    global gun_board, players, player_board

    # gun_board 생성
    gun_board = [list(map(func, input().split())) for _ in range(N)]

    # player_board, players 생성
    players = []
    player_board = [[0]*N for _ in range(N)]

    for i in range(M):
        x, y, d, s = map(int, input().split())
        ## (1,1) 부터이므로, 보정
        x = x-1
        y = y-1
        tmp = Player((x, y), d, s)
        tmp.idx = i
        
        players.append(tmp)
        player_board[x][y] = tmp

    # print(*gun_board, sep='\n')
    # print()
    # print(*player_board, sep='\n')


# 2) 전체 이동
def all_move():
    for player in players:
        x, y = player.pos
        dx, dy = d_xy[player.direction]

        # 방향대로 이동
        nx = x + dx
        ny = y + dy

        # print(player.idx, "번 플레이어 -> ", (nx, ny), "로 이동")

        if nx<0 or nx>=N or ny<0 or ny>=N:
            # 범위 벗어나면 방향 반대로
            nx = x - dx
            ny = y - dy
            player.direction = (player.direction+2)%4

        if player_board[nx][ny]:
            # 다른 플레이어가 있으면
            winner, loser = fight(player, player_board[nx][ny]) # 싸우기

            lose_gun(loser, (nx, ny))   # loser 총 내려놓기
            get_gun(winner, (nx, ny))   # winner 총 획득

            player_board[x][y] = 0
            player_board[nx][ny] = 0 

            loser_move(loser, (nx, ny)) # loser 이동
            # winner 이동
            player_board[nx][ny] = winner 
            winner.pos = (nx, ny)

            # print("--싸운 후 이동 완료--")
            # for i in range(N):
            #     for j in range(N):
            #         if type(player_board[i][j]) == int:
            #             print('(-, -)', end=' ')
            #         else: print((player_board[i][j].idx, player_board[i][j].direction), end=' ')
            #     print()
            
        else:
            # 다른 플레이어 없으면
            ## 이동
            move(player, (nx, ny))

            ## 총 확인
            get_gun(player, (nx, ny))

    

# 일반적인 이동
def move(player, pos):
    global player_board
    nx, ny = pos
    x, y = player.pos

    if (nx, ny)==(x, y):
        # 같으면 이동 X
        return
    
    player_board[nx][ny] = player
    player_board[x][y] = 0
    player.pos = (nx, ny)


# 진 사람 이동
def loser_move(player, pos):
    x, y = pos
    dx, dy = d_xy[player.direction]

    nx = x + dx
    ny = y + dy
    # 방향대로 이동
    for t in range(3):
        dx, dy = d_xy[(player.direction + t)%4]
        nx = x + dx
        ny = y + dy

        if nx<0 or nx>=N or ny<0 or ny>=N or player_board[nx][ny]:
            # 범위 벗어남 or 다른 플레이어 있으면
            ## 오른쪽 90도 회전
            if t==3:
                # 불가능하면 이동 안 함
                return
            continue
        else:
            player.direction = (player.direction + t)%4
            break
        

    # print("진 사람 이동: ",player.idx,"번 플레이어 -> ", (nx, ny))
    move(player, (nx, ny))
    get_gun(player, (nx, ny))


# 총 획득
def get_gun(player, gun_pos):
    global gun_board
    nx, ny = gun_pos
    if len(gun_board[nx][ny]) == 0:  # 총 없으면 종료
        return
    else:
        # 총 있으면
        max_gun = max(gun_board[nx][ny])
        if player.gun < max_gun:
            gun_board[nx][ny].append(player.gun)
            player.gun = max_gun
            gun_board[nx][ny].remove(max_gun)

# 총 버리기
def lose_gun(player, pos):
    global gun_board
    x, y = pos
    gun_board[x][y].append(player.gun)  # 총 내려놓고
    player.gun = 0                      # 초기화
    

# 싸우기
def fight(A, B):
    A_ = A.hp + A.gun
    B_ = B.hp + B.gun

    winner, loser = A, B
    if A_ < B_:
        winner, loser = loser, winner
    elif A_ == B_ and A.hp < B.hp:
        winner, loser = loser, winner
    
    winner.point += abs(A_ - B_)
    # print("싸우기")
    # print("winner: ", winner.idx, winner.hp, winner.gun, winner.point)
    # print("loser: ", loser.idx, loser.hp, loser.gun, loser.point)
    
    return [winner, loser]
        


if __name__=='__main__':
    N, M, K = tuple(map(int, input().split()))
    d_xy = [(-1,0), (0,1), (1,0), (0,-1)]

    gun_board = []
    player_board, players = [], []


    init()

    # K라운드 진행
    for t in range(1, K+1):
        # print("-----시작-----")
        # for i in range(N):
        #     for j in range(N):
        #         if type(player_board[i][j]) == int:
        #             print('(-, -)', end=' ')
        #         else: print((player_board[i][j].idx, player_board[i][j].direction), end=' ')
        #     print()
        
        # print(*gun_board, sep='\n')
        # 이동
        all_move()

        # print("-----결과-----")
        # for player in players:
        #     player.print()
        
        # for i in range(N):
        #     for j in range(N):
        #         if type(player_board[i][j]) == int:
        #             print('(-, -)', end=' ')
        #         else: print((player_board[i][j].idx, player_board[i][j].direction), end=' ')
        #     print()

    for idx, player in enumerate(players):
        if idx == len(players)-1:
            print(player.point)
        else: print(player.point, end=' ')