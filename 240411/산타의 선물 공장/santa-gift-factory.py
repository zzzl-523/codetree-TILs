class Present():
    def __init__(self, ID, w):
        self.ID = ID
        self.weight = w
    
    def print(self):
        print("----- 선물 출력 -----")
        print("ID: ", self.ID)
        print("weight: ", self.weight)

def init():
    global Q, commands

    # 1) 명령 정리
    ## 명령 개수
    Q = int(input())

    ## 명령 입력받기
    commands = [[] for _ in range(Q)]
    for t in range(Q):
        command = list(map(int, input().split()))
        cmd = command[0]
        contents = command[1:]
        
        commands[t] = (cmd, contents)


# 1. 공장 설립
def build_factory(contents):
    # print("공장 설립")
    global belts, presents, N, M

    # 명령 정리
    N, M = contents[0], contents[1]
    ID_list = contents[2:2+N]
    weight_list = contents[2+N:]

    # 벨트 생성 & 선물 생성
    # 벨트 배열은 딕셔너리로 생성
    belts = {}  

    for m in range(1, M+1):
        belts[m] = {}
        for n in range((N//M)*(m-1), (N//M)*(m-1)+(N//M)):
            present = Present(ID_list[n], weight_list[n])

            ## 벨트에는 ID만 저장
            ## 선물은 presents 배열에 저장
            if n == (N//M)*(m-1):
                belts[m]['head'] = present.ID
                belts[m][present.ID] = {"prev": "head", "next": ID_list[1]}
            if n == (N//M)*(m-1)+(N//M)-1:
                belts[m][present.ID] = {"prev": ID_list[n-1], "next": "tail"}
                belts[m]['tail'] = present.ID
            else: belts[m][present.ID] = {"prev": ID_list[n-1], "next": ID_list[n+1]}
            
            presents[present.ID] = present
    
    # print("belts: ", belts)
    # print("presents: ", presents)


# 2. 물건 하차
def unload_presents(contents):
    # print("[하차]")
    w_max = contents[0]     # max
    total_unload_weight = 0 # 하차된 무게

    for key in belts.keys():
        # 맨 첫 선물 꺼내기
        belt = belts[key]
        top = belt['head'] # ID

        ## 새로운 head
        belt['head'] = belt[top]['next']
        belt[belt['head']]['prev'] = 'head'

        if presents[top].weight <= w_max:
            # 선물의 무게 <= w_max 라면,
            # 하차
            # 하차된 무게 추가
            total_unload_weight += presents[top].weight
            del belt[top]
            
        else:
            # 맨 뒤에 다시 추가
            
            ## 기존 tail을 새로운 tail의 앞으로
            belt[belt['tail']]['next'] = top
            ## 새로운 tail == top
            belt[top]['next'] = 'tail'
            belt[top]['prev'] = belt['tail']
            belt['tail'] = top 
    
        # print(belt)
    print(total_unload_weight)


# ID로 선물 존재하는지 확인하는 함수
def check(ID):
    for key in belts.keys():
        belt = belts[key]
        if ID in belt.keys():
            return [True, key] # 벨트 번호
    return [False]


# 3. 물건 제거
def remove_presents(contents):
    r_id = contents[0]
    # print("[제거]", r_id)

    # 물건 있는지 확인
    ck = check(r_id)
    if ck[0]: # 있으면
        b_num = ck[1]
        now_belt = belts[b_num]
        now = now_belt[r_id]

        # 링크 갱신    
        if now_belt['head'] == r_id:
            now_belt['head'] = now['next']
            now_belt[now['next']]['prev'] = 'head'
        elif now_belt['tail'] == r_id:
            now_belt['tail'] = now['prev']
            now_belt[now['prev']]['next'] = 'tail'
        else:
            now_belt[now['prev']]['next'] = now['next']
            now_belt[now['next']]['prev'] = now['prev']

        del now_belt[r_id]     # 제거
        # print(now_belt)
        print(r_id) # 출력
    else:      # 없으면
        print(-1)


# 4. 물건 확인
def check_presents(contents):
    f_id = contents[0]
    # print("[확인]", f_id)
    
    ck = check(f_id)
    if ck[0]:   # 있으면
        b_num = ck[1]
        now_belt = belts[b_num]
        now = now_belt[f_id]

        # 링크 갱신
        # now(f_id)를 head로
        if now_belt['head'] == f_id:
            print(b_num)
            return

        now_belt[now_belt['head']]['prev'] = f_id
        now_belt[now['prev']]['next'] = 'tail'
        now_belt['tail'] = now['prev']

        now['prev'] = 'head'
        now['next'] = now_belt['head']
        now_belt['head'] = f_id
            
        print(b_num) # 벨트 번호 출력

        # print(belts[b_num])
    else:
        print(-1)


# 5. 벨트 고장
def belt_error(contents):
    b_num = contents[0]
    # print("[벨트 고장]", b_num)
    
    # 1) 고장 처리
    ## 이미 고장인지 확인
    if b_num not in belts.keys():
        print(-1)
        return

    # print(belts)

    # 2) 고장나지 않은 벨트 찾기 (오른쪽)
    key_arr = list(belts.keys())
    idx = key_arr.index(b_num) # 고장난 벨트의 index -> 오른쪽 index 될 예정
    n_idx = (idx+1) % len(belts)

    target = belts[key_arr[n_idx]]
    now = (belts[b_num])

    target_tail = target['tail']
    now_head = now['head']
    now_tail = now['tail']

    target[target_tail]['next'] = now_head
    now[now_head]['prev'] = target_tail
    target['tail'] = now_tail
    
    now.update(target)
    belts[key_arr[n_idx]] = now
    
    # 고장난 벨트 제거
    del belts[b_num] 
    print(b_num)
    # print("결과: ", belts)

if __name__ == '__main__':
    from collections import deque

    Q = 0
    belts = []
    presents = {}
    commands = []
    N, M = 0, 0

    # 명령 정리
    init()

    # 명령 실행
    for cmd, contents in commands:
        if cmd == 100: build_factory(contents)
        elif cmd == 200: unload_presents(contents)
        elif cmd == 300: remove_presents(contents)
        elif cmd == 400: check_presents(contents)
        elif cmd == 500: belt_error(contents)