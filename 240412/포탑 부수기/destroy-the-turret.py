class Potab():
    def __init__(self, ID, hp, attack_time, x, y):
        self.ID = ID
        self.hp = hp
        self.attack_time = attack_time
        self.x = x
        self.y = y


def init():
    global N, M, K, hp_board, potabs, potab_board

    # 입력 받기
    N, M, K = tuple(map(int, input().split()))

    p_id = 0    # 1부터 시작
    hp_board = [[0]*M for _ in range(N)]
    potab_board = [[0]*M for _ in range(N)]
    for r in range(N):
        tmp = list(map(int, input().split()))
        for c in range(M):
            # 공격력 보드 생성
            hp_board[r][c] = tmp[c]

            # 부서지지 않은 포탑일 경우,
            if hp_board[r][c] > 0:
                # 포탑 보드 생성
                p_id += 1
                potab_board[r][c] = p_id

                # 포탑 생성 & 포탑 배열에 추가
                new = Potab(p_id, hp_board[r][c], 0, r, c)
                potabs[p_id] = new


# 1) 공격자 선정
def set_attacker():
    global attacker_id, hp_board

    # 공격자 찾기 & 선정
    tmp = sorted(list(potabs.values()), key=lambda x:(x.hp, -x.attack_time, -(x.x + x.y), -x.y ))
    attacker = tmp[0]
    attacker_id = attacker.ID

    # 공격자 핸디캡
    change_hp(attacker, N+M)


# 해당 포탑의 공격력 바꿔주는 함수
def change_hp(potab, value):
    global hp_board
    r, c = potab.x, potab.y
    hp_board[r][c] += value
    potab.hp += value


# 2) 공격자 공격
def attack():
    global target_id
    # 타깃 찾기 & 선정
    tmp = sorted(list(potabs.values()), key=lambda x:(-x.hp, x.attack_time, (x.x + x.y), x.y ))
    target = tmp[0]
    
    if target.ID == attacker_id:
        # 공격자는 타깃이 될 수 없음
        target = tmp[1]

    target_id = target.ID
    attacker = potabs[attacker_id]

    # 공격
    ## 레이저 공격부터 시도 
    ck = rasor_attack()
    if not ck:
        # 불가능하면 포탄 어택
        potan_attack()
    
    ## 공격 적용
    apply_attack(target, sub_targets, attacker.hp)
    attacker.attack_time  = now_attack_time


# 공격 내용 적용 함수
def apply_attack(target, sub_targets, value):
    # 적용
    ## 메인 타깃은 공격자의 공격력 만큼 감소
    change_hp(target, -(value))

    # 서브 타깃은 절반 만큼 감소
    for sub_id in sub_targets:
        if sub_id == attacker_id: # 공격자는 영향 X
            continue
        sub_target = potabs[sub_id]
        change_hp(sub_target, -(value//2))

# 레이저 어택 함수
def rasor_attack():
    global sub_targets

    # 상하좌우 움직이면서 경로 찾기
    attacker = potabs[attacker_id]
    target = potabs[target_id]

    sub_targets = []                     # 경로에 위치한 sub_target ID 배열
    visited = [[False]*M for _ in range(N)] # 방문 저장 배열
    q = deque([(attacker.x, attacker.y, [])])
    while q:
        x, y, tmp_subs = q.popleft()

        # 타깃에 도달하면 즉시 종료 (최단거리)
        if potab_board[x][y] == target_id:
            # 서브 타깃 설정
            sub_targets = tmp_subs
            break

        for dx, dy in d_xy:
            nx = x + dx
            ny = y + dy

            # 범위를 벗어나면 반대로 나오기
            if nx<0 or nx>=N or ny<M or ny>=M:
                nx = nx % N
                ny = ny % M
            # 부서진 포탑이면 못 지나감
            if hp_board[nx][ny] <= 0:
                continue
            # 이미 방문했으면 제외            
            if visited[nx][ny]:
                continue
            
            visited[nx][ny] = True
            q.append((nx, ny, tmp_subs + [potab_board[nx][ny]]))

    # 공격 적용
    if sub_targets: # 경로 있으면 레이저 어택 적용
        sub_targets = sub_targets[:-1]
        return(True)
    else:           # 없으면 포탄 어택
        return(False)

# 포탄 어택 함수
def potan_attack():
    global sub_targets

    target = potabs[target_id]
    sub_targets = []
    d_diag = [(1,1), (1,-1), (-1,-1), (-1,1)] # 대각선 방향벡터
    d = d_xy + d_diag

    # 서브 타깃 설정
    for dx, dy in d:
        nx = target.x + dx
        ny = target.y + dy

        # 범위 벗어나면 반대쪽으로
        if nx<0 or nx>=N or ny<0 or ny>=M:
            nx = nx % N
            ny = ny % M
        
        # 포탑 부서지지 않은 경우
        if potab_board[nx][ny] > 0:
            sub_targets.append(potab_board[nx][ny])

    


# 3) 포탑 부서짐
def destroy_potab():
    global potab_board, hp_board
    # 공격력 0 이하인 포탑 부수기
    
    potab_arr = list(potabs.values())
    for potab in potab_arr:
        if potab.hp <= 0:
            # 포탑 제거
            change_hp(potab, 0)
            del potabs[potab.ID]
            x, y = potab.x, potab.y
            potab_board[x][y] = 0
            hp_board[x][y] = 0
    


# 4) 포탑 정비
def rearrange_potab():
    for ID in potabs:
        # 공격과 관련 없으면        
        if ID != attacker_id and ID != target_id and ID not in sub_targets:
            potab = potabs[ID]
            change_hp(potab, 1)


if __name__ == '__main__':
    from collections import deque

    N, M, K = 0, 0, 0
    hp_board = []       # 공격력 보드
    attacker_id = 0     # 공격자 ID
    target_id = 0       # 타깃 ID
    sub_targets = []    # 서브 타깃 ID
    potabs = {}         # 포탑 목록 (딕셔너리)
    potab_board = []    # 포탑 보드
    d_xy = [(0,1), (1,0), (0,-1), (-1,0)] # 우->하->좌->상
    now_attack_time = 0

    init()

    answer = 0
    for k in range(1, K+1):
        now_attack_time = k
        if len(potabs)==1:
            # 부서지지 않은 포탑이 하나 남은 경우
            break

        # 공격자 선정
        set_attacker()

        # 공격자 공격
        attack()
    
        # 포탑 부서짐
        destroy_potab()
        
        # 포탑 정비    
        rearrange_potab()


    # 최종 결과 출력
    tmp_arr = list(potabs.values())
    tmp_arr.sort(key=lambda x:-x.hp)
    answer = tmp_arr[0].hp
    print(answer)