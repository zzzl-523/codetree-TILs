class Santa():
    def __init__(self, ID, pos):
        self.ID = ID
        self.pos = pos
        # status: 2=정상, 0=기절, -1=탈락
        self.status = 2
        self.direction = (0, 0)
        self.score = 0

    def print(self):
        print("---- 산타 출력 ----")
        print("ID: ", self.ID)
        print("pos: ", self.pos)
        print("status: ", self.status)
        print("directions: ", self.direction)
        print("score: ", self.score)

def init():
    global N, M, P, C, D, santas, board, rudolf_pos

    N, M, P, C, D = tuple(map(int, input().split()))
    rc, rr = tuple(map(int, input().split()))
    rudolf_pos = (rc-1, rr-1)

    # board 생성
    board = [[0] * N for _ in range(N)]
    # 루돌프 표시
    board[rudolf_pos[0]][rudolf_pos[1]] = -1

    # 산타 배열 생성
    santas = {}
    for _ in range(P):
        ID, r, c  = tuple(map(int, input().split()))
        x = r-1
        y = c-1
        # 산타 생성
        tmp = Santa(ID, (x, y))
        # 산타 배열에 추가
        santas[ID] = tmp
        # board에 추가
        board[x][y] = ID

    # 출력
    # print(*board, sep='\n')
    # print()
    # for i in range(1, P+1):
    #     santas[i].print()


# 산타 상태 갱신
def check_santa():
    for santa in santas.values():
        if 0<= santa.status < 2:
            santa.status += 1


## 범위 밖에 있는지 확인하는 함수
def is_out_board(nx, ny):
    return nx<0 or nx>=N or ny<0 or ny>=N

# 루돌프 이동
def  move_rudolf():
    global picked_ID, rudolf_pos, rudolf_direction, santas, out_santas
    # print("<<< 루돌프 이동 >>>")
    rx, ry = rudolf_pos

    # 산타 선택
    tmp = list(santas.values())
    arr = []
    for t in tmp:
        if t.status==-1:
            continue
        arr.append(t)

    arr.sort(key=lambda x:((calc_dist(rudolf_pos, x.pos)), -x.pos[0], -x.pos[1]))
    picked_id = arr[0].ID
    picked_santa = arr[0]
    # arr[0].print()

    # 돌진
    d_diag = [(1,1), (1,-1), (-1,-1), (-1,1)]
    d = d_xy + d_diag

    min_value = calc_dist(rudolf_pos, picked_santa.pos)
    for dx, dy in d:
        nx = rx + dx
        ny = ry + dy

        if is_out_board(nx, ny):
            continue

        # 선택한 산타와 가장 가까워지는 방향으로 이동
        dist = calc_dist((nx, ny), picked_santa.pos)
        if dist < min_value:
            min_value = dist
            # 바꿔주기
            rudolf_pos = (nx, ny)
            rudolf_direction = (dx, dy)

    # 충돌 확인
    check_collapse(picked_santa, rudolf_pos, rudolf_direction, C)

    # 루돌프 위치 바꿔주기
    board[rx][ry] = 0
    board[rudolf_pos[0]][rudolf_pos[1]] = -1
    # print(rudolf_pos, rudolf_direction)
    # print(*board, sep='\n')

def calc_dist(a_pos, b_pos):
    ax, ay = a_pos
    bx, by = b_pos
    return (ax - bx) ** 2 + (ay - by) ** 2


def change_pos(santa, new_pos, direction):
    nx, ny = new_pos
    sx, sy = santa.pos

    # 옮기려는 위치가 범위 밖이면 탈락
    if is_out_board(nx, ny):
        # 산타 탈락 처리
        santa.status = -1
        out_santas[santa.ID] = santa

        santa.pos = (-1, -1)
        board[sx][sy] = 0

    # 탈락 아니면 바꿔주기
    else:
        if board[nx][ny] > 0:
            # 이동하려는 칸에 산타가 있으면 밀어내고, 자리 차지
            # 원래 그 칸에 있던 산타가 1칸 이동
            # 상호작용
            interaction(santas[board[nx][ny]], new_pos, direction)

        santa.pos = new_pos
        board[nx][ny] = santa.ID
        board[sx][sy] = 0

# 산타 이동
def move_santa():
    # print("<<< 산타 이동 >>>")
    # 기절한 상태에서는 움직이지 않음
    arr = sorted(list(santas.values()), key=lambda x:x.ID)
    for santa in arr:
        # print("ID:", santa.ID, "상태: ", santa.status)
        if santa.status < 2:
            continue

        sx, sy = santa.pos
        will_move_pos = (-1,-1)
        will_move_direction = (0,0)
        min_value = calc_dist(santa.pos, rudolf_pos)
        for dx, dy in d_xy:
            nx = sx + dx
            ny = sy + dy

            # 범위 밖으로 나가거나, 해당 위치에 이미 산타 있으면 이동 불가
            if is_out_board(nx, ny):
                continue

            if board[nx][ny] > 0:
                continue
            # 루돌프와 가까워지는지 체크
            dist_after = calc_dist((nx, ny), rudolf_pos)

            if dist_after == min_value and dist_after!=calc_dist(santa.pos, rudolf_pos):
                if will_move_pos == (-1, -1) and board[nx][ny] <= 0:
                    # 같은 크기지만, 이전 값이 불가능한 경우
                    # 이동
                    will_move_pos = (nx, ny)
                    will_move_direction = (dx, dy)

            if dist_after < min_value:
                min_value = dist_after

                # 더 가까워진다면 && 가능하다면
                if board[nx][ny] <= 0:
                    # 이동
                    will_move_pos = (nx, ny)
                    will_move_direction = (dx, dy)
                else:
                    will_move_pos = (-1, -1)
                    will_move_direction = (0, 0)


        # 일단 이동
        ## 이동 불가능한 경우, 이동 X
        if will_move_pos == (-1, -1):
            # print("이동 X", will_move_pos)
            continue
        ## 없으면 이동
        # print("이동 O", will_move_pos)
        change_pos(santa, will_move_pos, will_move_direction)

        # 충돌 확인
        check_collapse(santa, rudolf_pos, (-will_move_direction[0], -will_move_direction[1]), D)

    # print(*board, sep='\n')


# 충돌
def check_collapse(santa, rudolf_pos, direction, num):
    if board[rudolf_pos[0]][rudolf_pos[1]] > 0:
        # 산타가 있으면, (충돌)
        # print("< 충돌 >")
        # santa.print()
        # 산타 점수 + num
        santa.score += num
        sx, sy = santa.pos

        # 산타는 direction 방향으로 num 만큼 밀려남
        will_move_pos = (sx + direction[0]*num, sy + direction[1]*num)
        change_pos(santa, will_move_pos, direction)

        # 기절
        if santa.status >= 0:
            santa.status = 0

        # print("< 산타 결과 >")
        # santa.print()

        if num==D:
            board[rudolf_pos[0]][rudolf_pos[1]] = -1


# 상호작용
def interaction(santa, new_pos, direction):
    nx = new_pos[0] + direction[0]
    ny = new_pos[1] + direction[1]
    change_pos(santa, (nx, ny), direction)


if __name__ == '__main__':
    ## 파일 입출력
    # f = open("input.txt", "r")
    # input = f.readline


    N, M, P, C, D = 0, 0, 0, 0, 0
    santas, out_santas = {}, {}
    picked_ID = 0
    board = []
    rudolf_pos, rudolf_direction = (0, 0), (0, 0)
    d_xy = [(-1,0), (0,1), (1,0), (0,-1)] # 상우하좌 순서

    init()

    for m in range(M):
        # print("=========", m+1, "번 턴 ========")
        # 종료 조건
        if len(out_santas) >= P:
            break

        # 산타 기절 상태 갱신
        check_santa()

        # 루돌프 이동
        move_rudolf()

        # 산타 이동
        move_santa()

        # print("< 일단 결과 출력 >")
        arr = sorted(list(santas.values()), key=lambda x: x.ID)
        for santa in arr:
            if santa.status >= 0:
                santa.score += 1
            # print(santa.score, end=' ')

        # print()
    # print("-- 최종 결과")
    arr = sorted(list(santas.values()), key=lambda x: x.ID)
    for santa in arr:
        print(santa.score, end=' ')