import pygame
import sys
import os
import random  # 💡 코인이 3개의 차선 중 랜덤하게 나오게 하려고 추가!



# PyInstaller 에셋 경로 처리 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



# 1. 게임 초기화
pygame.init()
pygame.event.set_blocked(pygame.MOUSEMOTION)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Politician - Coin Collection")
clock = pygame.time.Clock()
FPS = 60

ROAD_H = 500

# --- 2. 에셋 로드 ---
try:
    ROAD_W = 470
    
    # 1. 파일 경로 설정
    paths = {
        "bg1": resource_path(os.path.join("assets", "sprites", "2nd_back1.png")),
        "bg2": resource_path(os.path.join("assets", "sprites", "2nd_back2.png")),
        "char1": resource_path(os.path.join("assets", "sprites", "char1.png")),
        "char2": resource_path(os.path.join("assets", "sprites", "char2.png")),
        "gd1": resource_path(os.path.join("assets", "sprites", "1st_gd.png")),
        "gd2": resource_path(os.path.join("assets", "sprites", "1st_gd2.png")),
        "gd3": resource_path(os.path.join("assets", "sprites", "2nd_gd2.png")),
        "gd4": resource_path(os.path.join("assets", "sprites", "3rd_gd2.png")),
        "coin": resource_path(os.path.join("assets", "sprites", "coin.png"))
    }

    # 2. 이미지 로드 및 크기 조정
    # 기존 fence_img 로드 부분을 이걸로 교체
    # [2. 에셋 로드] 섹션 안쪽, 기존 이미지 로드 코드 아래에 추가!
    start_scene_img = pygame.transform.scale(
    pygame.image.load(resource_path(os.path.join("assets", "sprites", "start_scene.png"))).convert_alpha(), 
    (WIDTH, HEIGHT)
    )

    camera1_img = pygame.image.load(resource_path(os.path.join("assets", "sprites", "camera1.png"))).convert_alpha()
    camera2_img = pygame.image.load(resource_path(os.path.join("assets", "sprites", "camera2.png"))).convert_alpha()
    
    # 🌟 [여기 추가!] 불러온 이미지의 가로/세로 길이를 각각 3으로 나눠서 다시 저장! (크기 1/3로 축소)
    camera1_img = pygame.transform.scale(camera1_img, (camera1_img.get_width() // 2, camera1_img.get_height() // 2))
    camera2_img = pygame.transform.scale(camera2_img, (camera2_img.get_width() // 2, camera2_img.get_height() // 2))
    
    # 🌟 사운드 로드 (exe 변환을 위해 resource_path 필수 적용)
    # 볼륨 조절이 필요하다면 snd_coin.set_volume(0.5) 처럼 0.0 ~ 1.0 사이로 설정 가능해.
    snd_coin = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "get.wav")))
    snd_loss = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "coin_loss.wav")))
    snd_get_big = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "coin_get.wav")))
    
    snd_coin.set_volume(0.3)      # 코인 소리는 중간 크기로
    snd_loss.set_volume(0.09)      # 감점 소리는 조금 크게 (경고 의미로!)
    snd_get_big.set_volume(0.5)   # 대박 점수 소리는 신나게 크게!
    
    # 🌟 사운드 로드 섹션에 추가
    snd_camera_get = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "camera_get.wav")))
    snd_redcarpet = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "redcarpet.wav")))
    
    snd_camera_get.set_volume(0.4)
    snd_redcarpet.set_volume(0.3)
    
    snd_shutter_loop = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "shutter1.wav")))
    snd_shutter_loop.set_volume(0.7) # 소리 크기 조절
    
    snd_cheer = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "cheer.wav")))
    snd_booing = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "booing.wav")))
    snd_soso = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "soso.wav")))
    
    # 볼륨 설정
    snd_cheer.set_volume(0.6)
    snd_booing.set_volume(0.3)
    snd_soso.set_volume(0.7)
    
    snd_start_game = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "start_game.wav")))
    snd_start_game.set_volume(0.5)
    
    # 엔딩곡 로드
    snd_ending1 = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "ending1.wav")))
    snd_ending2 = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "ending2.wav")))
    
    snd_ending1.set_volume(0.5)
    snd_ending2.set_volume(0.6)
    
# 🌟 배경음악 로드
    snd_start_back = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "start_back.wav")))
    snd_1_2_back = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "1_2_back.wav")))
    snd_3_back = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "3_back.wav")))
    
    # 볼륨 설정 (너무 크면 효과음이 묻히니 살짝 낮춰줍니다)
    snd_start_back.set_volume(0.3)
    snd_1_2_back.set_volume(0.3)
    snd_3_back.set_volume(0.4)

# 🌟 사운드 로드 섹션에 추가
    snd_giza = pygame.mixer.Sound(resource_path(os.path.join("assets", "sounds", "giza.wav")))
    snd_giza.set_volume(0.2) # 잔잔하게 깔리도록 볼륨을 낮게 설정 (필요시 조절)

    fence1_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "1st_fence.png"))).convert_alpha(), (30, HEIGHT))
    fence2_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "2nd_fence.png"))).convert_alpha(), (20, HEIGHT))
    fence3_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "3rd_fence.png"))).convert_alpha(), (44, HEIGHT))
    
    current_fence_img = fence1_img
    
    bg_image1 = pygame.transform.scale(pygame.image.load(paths["bg1"]).convert(), (WIDTH, HEIGHT))
    bg_image2 = pygame.transform.scale(pygame.image.load(paths["bg2"]).convert(), (WIDTH, HEIGHT))
    
    char1 = pygame.transform.scale(pygame.image.load(paths["char1"]).convert_alpha(), (120, 160))
    char2 = pygame.transform.scale(pygame.image.load(paths["char2"]).convert_alpha(), (120, 160))
    
    gd_image1 = pygame.transform.scale(pygame.image.load(paths["gd1"]).convert_alpha(), (ROAD_W, HEIGHT))
    gd_image2 = pygame.transform.scale(pygame.image.load(paths["gd2"]).convert_alpha(), (ROAD_W, ROAD_H))
    gd_image_2nd = pygame.transform.scale(pygame.image.load(paths["gd3"]).convert_alpha(), (ROAD_W, ROAD_H))
    gd_image_3rd = pygame.transform.scale(pygame.image.load(paths["gd4"]).convert_alpha(), (ROAD_W, ROAD_H))
    # 길 이미지 로드할 때 같이 불러와
    people_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "people.png"))).convert_alpha(), (350, 720))
    people_img_flipped = pygame.transform.flip(people_img, True, False) # 좌우 반전

    # 3. Rect 및 기타 설정
    gd_rect1 = gd_image1.get_rect(centerx=WIDTH // 2)
    gd_rect2 = gd_image2.get_rect(centerx=WIDTH // 2)

    # 4. 코인 로드
    coin_sheet = pygame.image.load(paths["coin"]).convert_alpha()
    coin_w = coin_sheet.get_width() // 6
    coin_h = coin_sheet.get_height()
    coin_frames = [pygame.transform.scale(coin_sheet.subsurface((i * coin_w, 0, coin_w, coin_h)), (int(coin_w * 3), int(coin_h * 3))) for i in range(6)]

    car_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "car.png"))).convert_alpha(), (700, 500))
    apple_img = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "sprites", "apple.png"))).convert_alpha(), (80, 80))
    # 기존 car_img, apple_img 등 로드하는 곳 근처에 추가
    press_bg_img = pygame.transform.scale(
        pygame.image.load(resource_path(os.path.join("assets", "sprites", "middle.png"))).convert_alpha(), 
        (WIDTH, HEIGHT)
    )
    

    # [2. 에셋 로드 섹션] 에 추가
    ending1_img = pygame.transform.scale(
        pygame.image.load(resource_path(os.path.join("assets", "sprites", "ending1.png"))).convert_alpha(), 
        (WIDTH, HEIGHT)
    )
    ending2_img = pygame.transform.scale(
        pygame.image.load(resource_path(os.path.join("assets", "sprites", "ending2.png"))).convert_alpha(), 
        (WIDTH, HEIGHT)
    )

    emer_img = pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("assets", "sprites", "emer.png"))).convert_alpha(), 
            (700, 350) # 크기는 상황에 맞게 조절하세요!
        )

    print("✅ 모든 에셋 로드 완료!")

except Exception as e:
    print(f"🚨 에셋 로드 오류: {e}")
    pygame.quit()
    sys.exit()



# --- 3. 게임 변수 설정 ---

is_ending = False  # 엔딩 중인지 확인
ending_timer = 0   # 엔딩 시간 측정

scroll_speed = 9
people_y = 0

current_road_image = gd_image2
flash_timer = 0  # 효과 유지 시간

fence_ys = [0, -720, -1440, -2160]

# [그리기]
screen.blit(people_img, (50, int(people_y)))
screen.blit(people_img, (50, int(people_y + 720))) # 이어지게 하려면 2장을 겹쳐서 그려

bg1_y = 0               
bg2_y1 = HEIGHT         
bg2_y2 = HEIGHT * 2     


gd_y1 = 0                       
gd_y2 = HEIGHT                  
gd_y3 = HEIGHT + ROAD_H         
current_gd_image1 = gd_image1 
current_h1 = HEIGHT             



LANE_LEFT = 490
LANE_CENTER = 640
LANE_RIGHT = 790
lanes = [LANE_LEFT, LANE_CENTER, LANE_RIGHT]
current_lane_idx = 1


player_target_x = lanes[current_lane_idx]
player_x = player_target_x
player_y = 300 


anim_timer = 0
current_frame = char1
anim_speed = 10 

running = True
start_ticks = pygame.time.get_ticks()
score = 0
is_ending = False
ending_timer = 0
    
# 🪙 코인 리셋
coins = []             
coin_spawn_timer = 0   
coin_anim_timer = 0
coin_anim_speed = 5
coin_frame_idx = 0
    
# 🍏 사과 리셋
apples = [] 
apple_spawn_timer = 0
    
# 📸 카메라 리셋 (이번에 추가된 것!)
cameras = []
current_camera_img = camera1_img
camera_anim_timer = 0
camera_score = 0
MAX_CAMERA_SCORE = 28

# 🌟 추가: 인게임 시작과 동시에 1~2단계 BGM 무한 반복 재생!
snd_1_2_back.play(loops=-1) 
is_3rd_bgm_playing = False  # 🌟 추가: 3단계 BGM이 켜졌는지 확인하는 변수

# 🌟 [오류 해결 포인트!] 시작 화면에서 쓸 폰트 변수들을 여기서 확실하게 선언해 줍니다.
# 변수 설정 섹션의 '가장 아래쪽'에 넣어주세요.
font_path_start = resource_path(os.path.join("assets", "TerrarumSans.ttf"))
font_title = pygame.font.Font(font_path_start, 80)
font_menu = pygame.font.Font(font_path_start, 34)
font_desc = pygame.font.Font(font_path_start, 30)

font_path_game = resource_path(os.path.join("assets", "Jersey10.ttf"))
font = pygame.font.Font(font_path_game, 30)


page = 0 
def show_start_screen():
    waiting = True
    start_transition = False
    show_explanation = False  
    transition_start_ticks = 0
    
    # 🌟 여기에 추가하세요!

    pages = [
        ["[ 스토리 ]", "80초 안에 돈 없는 길바닥 인생에서 100만 원을 모아", "당당히 국회의원에 당선되어라!", "과연 당신은 국회의원이 될 수 있을까?"],
        ["[ 조작법 ]", "A / 왼쪽 화살표 : 왼쪽 이동", "D / 오른쪽 화살표 : 오른쪽 이동"],
        ["[ 아이템 ]", "코인 : +10,000점", "사과 박스 : 80% 확률로 -20000점 / 20% 확률로 +50000점!", "카메라 : 게이지를 모으면 기자회견 가능"],
        ["[추가 설명 룰]", "기자회견은 게이지가 차지 않으면 진행하지 않습니다", "당신은 과연 기자회견을 잘 넘어갈 수 있을까요?"]
    ]
    
    
    start_btn_rect = pygame.Rect(WIDTH // 2 - 220, 560, 200, 60)
    desc_btn_rect = pygame.Rect(WIDTH // 2 + 20, 560, 200, 60)
    
    pygame.event.clear()
    
    while waiting:
        screen.blit(start_scene_img, (0, 0))
        
        # 1. 화면 그리기
        title_surf = font_title.render("길바닥에서 국회까지", True, (255, 255, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 120)))
        
        if not show_explanation:
            mouse_pos = pygame.mouse.get_pos()
            start_color = (255, 255, 255) if start_btn_rect.collidepoint(mouse_pos) else (180, 180, 180)
            desc_color = (255, 255, 255) if desc_btn_rect.collidepoint(mouse_pos) else (180, 180, 180)
            
            pygame.draw.rect(screen, (0, 0, 0, 150), start_btn_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0, 150), desc_btn_rect, border_radius=10)
            screen.blit(font_menu.render("게임 시작", True, start_color), font_menu.render("게임 시작", True, start_color).get_rect(center=start_btn_rect.center))
            screen.blit(font_menu.render("게임 설명", True, desc_color), font_menu.render("게임 설명", True, desc_color).get_rect(center=desc_btn_rect.center))
        else:
            popup_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400)
            pygame.draw.rect(screen, (15, 15, 25), popup_rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2, border_radius=15)
            
            # 🌟 핵심: 현재 page 변수에 맞는 데이터만 가져와서 그립니다!
            y = popup_rect.top + 80
            for line in pages[page]:  # page가 0이면 스토리, 1이면 조작법...
                color = (255, 215, 0) if "[" in line else (230, 230, 230)
                txt = font_desc.render(line, True, color)
                # 텍스트 위치를 팝업 중앙으로 정렬
                screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))
                y += 50
            
            # 🌟 3. 페이지 번호는 여기(for 루프 바로 아래)에 넣으세요!
            page_text = font_desc.render(f"{page + 1} / {len(pages)}", True, (200, 200, 200))
            screen.blit(page_text, page_text.get_rect(center=(WIDTH // 2, y + 20)))
            
            # 🌟 버튼 위치를 팝업 내부 중앙 쪽으로 조정
            btn_prev = pygame.Rect(WIDTH // 2 - 100, popup_rect.bottom - 80, 60, 40)
            btn_next = pygame.Rect(WIDTH // 2 + 40, popup_rect.bottom - 80, 60, 40)
            
            pygame.draw.rect(screen, (70, 70, 100), btn_prev, border_radius=5)
            pygame.draw.rect(screen, (70, 70, 100), btn_next, border_radius=5)
            # 🌟 [수정] 텍스트가 네모 칸 중앙에 딱 맞게 좌표 직접 미세 조정
            prev_txt = font_desc.render("<", True, (255, 255, 255))
            next_txt = font_desc.render(">", True, (255, 255, 255))
            
            # center는 중심점인데, 거기서 글자 크기의 절반만큼 빼서 위치를 보정합니다.
            # 숫자를 조금씩 바꿔보면서 자기 눈에 가장 예쁜 위치를 찾으세요!
            screen.blit(prev_txt, (btn_prev.centerx - prev_txt.get_width()//2, btn_prev.centery - prev_txt.get_height()//2 - 2))
            screen.blit(next_txt, (btn_next.centerx - next_txt.get_width()//2, btn_next.centery - next_txt.get_height()//2 - 2))
                
                

# ... (이벤트 루프 시작)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 팝업이 열려있을 때 버튼 클릭 감지
                if show_explanation:
                    # [이전] 버튼
                    if btn_prev.collidepoint(event.pos):
                        page = max(0, page - 1)
                    # [다음] 버튼
                    elif btn_next.collidepoint(event.pos):
                        page = min(len(pages)-1, page + 1)
                    # 팝업 외부를 눌렀을 때만 닫기 (팝업 영역 밖인 경우)
                    elif not popup_rect.collidepoint(event.pos):
                        show_explanation = False
                
                # 메인 버튼 클릭
                elif start_btn_rect.collidepoint(event.pos) and not start_transition:
                    snd_start_back.stop()
                    snd_start_game.play()
                    start_transition = True
                    transition_start_ticks = pygame.time.get_ticks()
                elif desc_btn_rect.collidepoint(event.pos) and not start_transition:
                    show_explanation = True
                    page = 0

        # 3. 2초 전환 연출
        if start_transition:
            elapsed = pygame.time.get_ticks() - transition_start_ticks
            alpha = min(255, int((elapsed / 2000) * 255))
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
            if elapsed >= 2000:
                waiting = False
        
        pygame.display.flip()


# 🌟 2위치: 메인 루프에 진입하기 '직전'에 함수를 딱 한 번 실행시킵니다!
#show_start_screen()
#pygame.event.clear() # 🌟 시작 화면 탈출 직후 모든 클릭 신호 삭제!

# 🌟 3위치: 시작 화면을 다 보고 게임이 딱 시작하는 순간의 시간을 초기화합니다!
start_ticks = pygame.time.get_ticks()
limit_time = 80

# 🌟 로딩 화면 함수 (3초 동안 검은 화면 유지)
def show_loading_screen():
    loading_start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - loading_start < 3000: # 3000ms = 3초
        screen.fill((0, 0, 0)) # 검은 화면
        
        # Loading... 텍스트
        loading_text = font_title.render("Loading...", True, (255, 255, 255))
        screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        
        pygame.display.flip()
        
        # 로딩 중에도 창을 닫을 수 있게 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 🌟 엔딩 화면 함수 (점수에 따라 이미지 결정, ENTER 키로 복귀)
def show_ending_screen(final_score):
    waiting = True
    
    # 1. 엔딩 곡 재생 (한 번만!)
    if final_score >= 1000000:
        snd_ending1.play(loops=0) # 🌟 loops=0은 딱 한 번 재생!
    else:
        snd_ending2.play(loops=0)
    
    # 목표 점수(100만원) 달성 여부에 따라 엔딩 이미지 선택
    if final_score >= 1000000:
        current_ending = ending1_img # 성공 엔딩
    else:
        current_ending = ending2_img # 실패/노멀 엔딩
        
    while waiting:
        screen.blit(current_ending, (0, 0))
        pygame.display.flip()
        
        # 엔터키 대기 이벤트
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # 🌟 ENTER 키를 누르면
                    # 🌟 엔딩 종료 시 노래 끄기
                    snd_ending1.stop()
                    snd_ending2.stop()
                    waiting = False              # 엔딩 루프 탈출!

# [게임 전체 무한 루프 시작!] 메뉴 -> 인게임 -> 로딩 -> 엔딩 -> 다시 메뉴 반복
# ====================================================
while True:
    
    # 1. 시작 화면 (메뉴) 띄우기
    show_start_screen()
    
    # 2. 확실하게 이벤트를 비워줍니다!
    pygame.event.clear()
    
    # 2. 🌟 인게임 진입 직전, 게임 변수 초기화!
    start_ticks = pygame.time.get_ticks()
    score = 0
    is_ending = False
    ending_timer = 0
    coins = []
    apples = []
    current_lane_idx = 1
    player_x = lanes[current_lane_idx]
    player_y = 300
    
    # 🎤 기자회견 이벤트 전용 변수 (새로 추가!)
    is_press_conference = False    # 현재 기자회견 중인지 여부
    press_event_done = False       # 이번 판에 기자회견을 했는지 여부 (중복 실행 방지)
    total_paused_time = 0          # 일시정지되었던 총 시간
    pause_start_ticks = 0          # 일시정지가 시작된 순간의 시간
    press_delay_start = 0  # 🌟 기자회견 2초 딜레이 타이머
    floating_texts = []    # 🌟 클릭한 곳에서 떠오르는 점수 텍스트 리스트
    # 🎤 기자회견 이벤트 전용 변수 (기존 변수에 아래 것 추가)
    emer_x = WIDTH # 화면 오른쪽 끝에서 시작
    
    # 🌟 추가된 연출용 변수 (복사해서 아래에 붙여넣으세요)
    press_transition_timer = 0  # 화면 빨려들어가는 효과 타이머
    selected_btn_idx = -1       # 선택한 답변 인덱스 저장
    post_select_timer = 0       # 선택 후 1초(60프레임) 대기 타이머
    press_question_step = 1     # 🌟 현재 몇 번째 질문인지 체크하는 변수 추가!

    # --- 4. 메인 루프 ---
    running = True
    while running:
        
        
# [1. 시간 계산 및 상태 업데이트]
        if is_press_conference:
            current_pause_duration = pygame.time.get_ticks() - pause_start_ticks
            
            if press_transition_timer > 0:
                press_transition_timer -= 1
                if press_transition_timer == 0:
                    press_delay_start = pygame.time.get_ticks() 
                    
            if post_select_timer > 0:
                post_select_timer -= 1
                if post_select_timer == 0:
                    
                    if press_question_step == 1:
                        press_question_step = 2        
                        selected_btn_idx = -1          
                        press_delay_start = pygame.time.get_ticks() 
                    else:
                        is_press_conference = False
                        # 🌟 기자회견이 끝났으니 셔터 소리 멈추고 게임 복귀!
                        snd_shutter_loop.stop()
                        snd_giza.stop()
                        
                        total_paused_time += pygame.time.get_ticks() - pause_start_ticks
                        
                        # 🌟 추가: 기자회견 끝나고 돌아올 때 남은 시간에 맞춰 BGM 다시 재생!
                        if remaining_time <= 20:
                            snd_3_back.play(loops=-1)
                            is_3rd_bgm_playing = True
                        else:
                            snd_1_2_back.play(loops=-1)
                        
        else:
            elapsed_time = (pygame.time.get_ticks() - start_ticks - total_paused_time) / 1000
            remaining_time = max(0, limit_time - elapsed_time)
            
            # 🌟 20초 남았을 때 기자회견 발동 조건 체크!
            if remaining_time <= 20 and not press_event_done and not is_ending:
                press_event_done = True # 조건 달성 실패해도 다시 검사하지 않도록 무조건 True로 막음
                
                # 🌟 카메라 게이지가 100% (MAX_CAMERA_SCORE 이상) 찼을 때만 기자회견 실행!
                if camera_score >= MAX_CAMERA_SCORE:
                    is_press_conference = True
                    # 🌟 기자회견 시작 시 셔터 소리 무한 루프 재생!
                    snd_shutter_loop.play(loops=-1)
                    
                    # 🌟 추가: 기자회견 시작 시 기존 BGM 강제 종료!
                    snd_1_2_back.stop()
                    snd_3_back.stop()
                    
                    # 🌟 기자회견 브금 잔잔하게 무한 반복 재생!
                    snd_giza.play(loops=-1)
                    
                    pause_start_ticks = pygame.time.get_ticks() 
                    press_transition_timer = 30 
                    selected_btn_idx = -1
                    post_select_timer = 0
                    press_question_step = 1 
                # 게이지가 덜 찼다면? -> is_press_conference가 켜지지 않으므로 그냥 일반 게임 계속 진행됨!
                
        if remaining_time <= 0 and not is_ending and not is_press_conference: 
            is_ending = True
            
            # 🌟 다른 소리들을 모두 멈추고 엔딩곡만 나오게 합니다.
            pygame.mixer.stop()
            
        # 충돌 판정을 위한 플레이어 Rect (매 프레임 최신화)
        player_rect = char1.get_rect(center=(int(player_x), int(player_y)))      
        
        
        
# 🌟 [기자회견 선택지 버튼 영역 설정]
        btn_w, btn_h = 1150, 60
        btn_start_y = 350
        btn_gap = 75
        btn_A_rect = pygame.Rect(WIDTH//2 - btn_w//2, btn_start_y, btn_w, btn_h)
        btn_B_rect = pygame.Rect(WIDTH//2 - btn_w//2, btn_start_y + btn_gap, btn_w, btn_h)
        btn_C_rect = pygame.Rect(WIDTH//2 - btn_w//2, btn_start_y + btn_gap*2, btn_w, btn_h)
        btn_D_rect = pygame.Rect(WIDTH//2 - btn_w//2, btn_start_y + btn_gap*3, btn_w, btn_h)



        # [2. 이벤트 처리]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                
# 🌟 마우스 클릭 이벤트 (기자회견 중일 때 정답 고르기)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_press_conference and press_transition_timer == 0 and post_select_timer == 0:
                    delay_time = 2000 if press_question_step == 1 else 1000 # 1번 질문은 2초, 2번은 1초 대기
                    if pygame.time.get_ticks() - press_delay_start >= delay_time:
                        
                        if btn_A_rect.collidepoint(event.pos):
                            selected_btn_idx = 0
                            if press_question_step == 1:
                                score += 100000
                                snd_cheer.play()
                                floating_texts.append(["+100,000", (255, 50, 50), list(event.pos), 60])
                            else:
                                score += 20000 # 사과상자 해명 성공
                                snd_cheer.play()
                                floating_texts.append(["+20,000", (255, 50, 50), list(event.pos), 60])
                            post_select_timer = 60
                            
                        elif btn_B_rect.collidepoint(event.pos):
                            selected_btn_idx = 1
                            snd_soso.play() # 둘 다 변동 없음
                            floating_texts.append(["+0", (255, 255, 255), list(event.pos), 60])
                            post_select_timer = 60
                            
                        elif btn_C_rect.collidepoint(event.pos):
                            selected_btn_idx = 2
                            if press_question_step == 1:
                                snd_soso.play()
                                floating_texts.append(["+0", (255, 255, 255), list(event.pos), 60])
                            else:
                                score -= 50000 # 기자 농락 감점
                                snd_booing.play()
                                floating_texts.append(["-50,000", (50, 100, 255), list(event.pos), 60])
                            post_select_timer = 60
                            
                        elif btn_D_rect.collidepoint(event.pos):
                            selected_btn_idx = 3
                            if press_question_step == 1:
                                score -= 100000
                                snd_booing.play()
                                floating_texts.append(["-100,000", (50, 100, 255), list(event.pos), 60])
                            else:
                                score -= 200000 # 최악의 자백 감점
                                snd_booing.play()
                                floating_texts.append(["-200,000", (50, 100, 255), list(event.pos), 60])
                            post_select_timer = 60                            
                            
                            
            # 키보드 이벤트
            if event.type == pygame.KEYDOWN:
                # 일반 게임 중일 때만 좌우 이동 타겟 변경
                if not is_ending and not is_press_conference:
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and current_lane_idx > 0:
                        current_lane_idx -= 1
                        player_target_x = lanes[current_lane_idx]
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and current_lane_idx < 2:
                        current_lane_idx += 1
                        player_target_x = lanes[current_lane_idx]
                
                # 'n' 키로 시간 점프 및 가운데 복귀
                if event.key == pygame.K_n:
                    # 🌟 여기 들여쓰기가 모두 똑같이 20칸(혹은 탭 5번)인지 확인하세요!
                    start_ticks = pygame.time.get_ticks() - (limit_time - 10) * 1000
                    flash_timer = 20 
                    current_lane_idx = 1 
                    player_target_x = lanes[current_lane_idx]
                    
                    # 🌟 'm' 키로 20초 남은 시점으로 점프 (새로 추가! 기자회견 직전  테스트용)
                if event.key == pygame.K_m:
                    start_ticks = pygame.time.get_ticks() - total_paused_time - (limit_time - 20) * 1000
                    flash_timer = 20 
                    current_lane_idx = 1 
                    player_target_x = lanes[current_lane_idx]
                    

        # [3. 환경 업데이트 (엔딩이 아닐 때만!)]
        if not is_ending and not is_press_conference:
            # 1. 배경 및 길 스크롤
            bg1_y -= scroll_speed
            bg2_y1 -= scroll_speed
            bg2_y2 -= scroll_speed
            if bg2_y1 <= -HEIGHT: bg2_y1 = bg2_y2 + HEIGHT
            if bg2_y2 <= -HEIGHT: bg2_y2 = bg2_y1 + HEIGHT
                
            gd_y1 -= scroll_speed
            gd_y2 -= scroll_speed
            gd_y3 -= scroll_speed
            if gd_y1 <= -current_h1: 
                gd_y1 = gd_y3 + ROAD_H
                current_gd_image1 = gd_image2  
                current_h1 = ROAD_H  
            if gd_y2 <= -ROAD_H: gd_y2 = gd_y1 + ROAD_H
            if gd_y3 <= -ROAD_H: gd_y3 = gd_y2 + ROAD_H

            for i in range(len(fence_ys)):
                fence_ys[i] -= scroll_speed
                if fence_ys[i] <= -720: fence_ys[i] += 2880
                    
            # 2. 시간대별 길 교체 및 사람 스크롤
            if remaining_time <= 20: # 3rd 단계
                # 3단계 진입 순간 딱 한 번 실행
                if current_road_image != gd_image_3rd:
                    snd_redcarpet.play() # 진입하자마자 셔터음 1번
                    flash_timer = 10
                    
                    # 🌟 추가: 3단계 진입 시 1_2 BGM 끄고 3_back 재생 (중복 재생 방지)
                    if not is_3rd_bgm_playing:
                        snd_1_2_back.stop()
                        snd_3_back.play(loops=-1)
                        is_3rd_bgm_playing = True
                    
                    
                current_road_image = gd_image_3rd
                current_fence_img = fence3_img
                
                
                # 🌟 [수정 완료] 플래시가 터지는 랜덤한 순간마다 셔터음과 함께 반짝!
                if random.randint(0, 30) == 0: 
                    flash_timer = 5
                    snd_redcarpet.play() # 반짝일 때마다 셔터음 추가 재생!
                
                people_y -= scroll_speed
                if people_y <= -720: people_y = 0
                
            elif remaining_time <= 50: # 2nd 단계
                if current_road_image != gd_image_2nd: flash_timer = 10
                current_road_image = gd_image_2nd
                current_fence_img = fence2_img
            else: # 1st 단계
                current_road_image = gd_image2
                current_fence_img = fence1_img

            # 3. 코인 애니메이션 및 생성/이동 로직
            coin_anim_timer += 1
            if coin_anim_timer >= coin_anim_speed:
                coin_anim_timer = 0
                coin_frame_idx = (coin_frame_idx + 1) % 6
            current_coin_img = coin_frames[coin_frame_idx]

            if random.randint(0, 200) < 5: 
                coins.append([random.choice(lanes), HEIGHT + 50])
                
            next_coins = []
            for c in coins:
                c[1] -= scroll_speed
                if c[1] < -50: continue
                coin_rect = current_coin_img.get_rect(center=(c[0], int(c[1])))
                
                if player_rect.colliderect(coin_rect):
                    snd_coin.play() 
                    score += 10000
                    continue
                next_coins.append(c)
            coins = next_coins
            
            # 🌟 [카메라 애니메이션 및 생성 로직]
            # 1. 플래시 애니메이션 (camera1 <-> camera2 깜빡임)
            camera_anim_timer += 1
            if camera_anim_timer >= 10: # 깜빡이는 속도 (숫자가 작을수록 빠름)
                camera_anim_timer = 0
                current_camera_img = camera2_img if current_camera_img == camera1_img else camera1_img

            # 2. 카메라 생성 (🌟 남은 시간이 40초 초과일 때만 등장!)
            if remaining_time > 20:
                if random.randint(0, 300) < 3: 
                    spawn_lane = random.choice(lanes)
                    
                    #겹침 방지 
                    is_overlapping = False
                    for item in coins + apples + cameras:
                        if item[0] == spawn_lane and abs(item[1] - (HEIGHT + 50)) < 100:
                            is_overlapping = True
                            break
                    
                    if not is_overlapping:
                        cameras.append([spawn_lane, HEIGHT + 50])
                        
                        
            # 3. 카메라 이동 및 충돌 처리
            next_cameras = []
            for cam in cameras:
                cam[1] -= scroll_speed
                if cam[1] < -50: continue
                cam_rect = current_camera_img.get_rect(center=(cam[0], int(cam[1])))
                
                if player_rect.colliderect(cam_rect):
                    snd_camera_get.play() # 📸 카메라 획득 소리!
                    camera_score = min(camera_score + 1, MAX_CAMERA_SCORE) # 최대치까지만 증가
                    continue
                next_cameras.append(cam)
            cameras = next_cameras

            # 4. 애플 생성 및 이동
            apple_spawn_timer += 1
            if apple_spawn_timer >= 300: 
                apple_spawn_timer = 0
                apples.append([random.choice(lanes), HEIGHT + 50])

            next_apples = []
            for a in apples:
                a[1] -= scroll_speed
                if a[1] < -50: continue
                apple_rect = apple_img.get_rect(center=(a[0], int(a[1])))
                if player_rect.colliderect(apple_rect):
                    if random.randint(1, 100) <= 80: 
                        snd_loss.play()  
                        score -= 20000
                    else: 
                        snd_get_big.play()  
                        score += 50000
                    continue
                next_apples.append(a)
            apples = next_apples

            # 5. 일반 게임 중 좌우 이동
            player_x += (player_target_x - player_x) * 0.4


        # [4. 엔딩 연출 (엔딩일 때만!)]
        if is_ending:
            ending_timer += 1
            if player_y < 500:
                player_y += 4  
                player_x += (LANE_CENTER - player_x) * 0.1 
            elif ending_timer < 200:
                player_y = 500
            else:
                player_y -= 10
                if ending_timer > 250: running = False


        # [5. 공통 처리 (항상 실행)]
        if remaining_time > 79:
            current_gd_image1 = gd_image1
        else:
            current_gd_image1 = current_road_image

        anim_timer += 1
        if anim_timer >= anim_speed:
            anim_timer = 0
            current_frame = char2 if current_frame == char1 else char1


        # --- 5. 화면 그리기 ---
        
        # [1] 배경 
        if bg1_y > -HEIGHT: screen.blit(bg_image1, (0, int(bg1_y)))
        screen.blit(bg_image2, (0, int(bg2_y1)))
        screen.blit(bg_image2, (0, int(bg2_y2)))

        # [2] 울타리 
        for y in fence_ys:
            screen.blit(current_fence_img, (360, int(y)))
            screen.blit(current_fence_img, (890, int(y)))

        # [3] 길 
        screen.blit(current_gd_image1, (gd_rect1.x, int(gd_y1)))
        screen.blit(current_road_image, (gd_rect2.x, int(gd_y2)))
        screen.blit(current_road_image, (gd_rect2.x, int(gd_y3)))

        # [4] 사람들
        if remaining_time <= 20:
            screen.blit(people_img, (50, int(people_y)))
            screen.blit(people_img, (50, int(people_y + 720)))
            screen.blit(people_img_flipped, (900, int(people_y)))
            screen.blit(people_img_flipped, (900, int(people_y + 720)))

        # [5] 코인
        current_coin_img = coin_frames[coin_frame_idx]
        for c in coins:
            rect = current_coin_img.get_rect(center=(c[0], int(c[1])))
            screen.blit(current_coin_img, rect.topleft)
            
        #[5.5] 뇌물 그리기 
        for a in apples:
            screen.blit(apple_img, (a[0] - 40, int(a[1]) - 40))
            
        # 🌟 [5.7] 카메라 아이템 그리기 (도로 위)
        for cam in cameras:
            rect = current_camera_img.get_rect(center=(cam[0], int(cam[1])))
            screen.blit(current_camera_img, rect.topleft)

        # [6] 캐릭터 그리기 
        if not (is_ending and ending_timer >= 100):
            screen.blit(current_frame, player_rect.topleft)

        # [7] 자동차 그리기 
        if is_ending and ending_timer >= 3:
            car_rect = car_img.get_rect(center=(680, 600))
            screen.blit(car_img, car_rect.topleft)

        # [8] UI 그리기
        funding_text = font.render(f"FUNDING: {score:,} / 1,000,000", True, (255, 255, 0))
        time_text = font.render(f"TIME: {int(remaining_time)}s", True, (255, 255, 255))
        
        screen.blit(funding_text, (40, 40))
        screen.blit(time_text, (1100, 20))

        # --- 기존 펀딩 점수 게이지 ---
        GOAL_SCORE = 1000000
        gauge_width = 300 
        gauge_height = 20 
        gauge_x = 40      
        gauge_y = 80      
        progress = min(score / GOAL_SCORE, 1.0)
        pygame.draw.rect(screen, (50, 50, 50), (gauge_x, gauge_y, gauge_width, gauge_height))
        bar_color = (255, 215, 0) if progress >= 1.0 else (0, 255, 0)
        pygame.draw.rect(screen, bar_color, (gauge_x, gauge_y, int(gauge_width * progress), gauge_height))
        pygame.draw.rect(screen, (255, 255, 255), (gauge_x, gauge_y, gauge_width, gauge_height), 2)


        # 🌟 --- 신규: 카메라 UI 및 게이지 ---
        cam_ui_x = 40
        cam_ui_y = 115
        
        # 1. 왼쪽 게이지 옆에 조그맣게 카메라 아이콘 띄우기 (고정 이미지로 camera1 사용)
        ui_cam_img = pygame.transform.scale(camera1_img, (30, 30))
        screen.blit(ui_cam_img, (cam_ui_x, cam_ui_y))
        
        # 2. 카메라 주목도 게이지 그리기
        cam_gauge_x = cam_ui_x + 40 # 아이콘 오른쪽에 배치
        cam_gauge_y = cam_ui_y + 5
        cam_gauge_w = 260
        cam_gauge_h = 20
        cam_progress = camera_score / MAX_CAMERA_SCORE # 0.0 ~ 1.0 비율
        
        # 배경색 (어두운 회색)
        pygame.draw.rect(screen, (50, 50, 50), (cam_gauge_x, cam_gauge_y, cam_gauge_w, cam_gauge_h))
        # 채워지는 색 (눈에 띄는 하늘색/플래시 색)
        pygame.draw.rect(screen, (0, 200, 255), (cam_gauge_x, cam_gauge_y, int(cam_gauge_w * cam_progress), cam_gauge_h))
        # 테두리
        pygame.draw.rect(screen, (255, 255, 255), (cam_gauge_x, cam_gauge_y, cam_gauge_w, cam_gauge_h), 2)


# # 🌟 [10] 기자회견 팝업 화면 그리기
        if is_press_conference:
            if press_transition_timer > 0:
                # 🌀 화면 빨려들어가는(줌인) 효과!
                progress = 1.0 - (press_transition_timer / 30.0)
                curr_w = int(WIDTH * progress)
                curr_h = int(HEIGHT * progress)
                if curr_w > 0 and curr_h > 0:
                    zoomed_bg = pygame.transform.scale(press_bg_img, (curr_w, curr_h))
                    screen.blit(zoomed_bg, (WIDTH//2 - curr_w//2, HEIGHT//2 - curr_h//2))
            else:
                # 배경 띄우기
                screen.blit(press_bg_img, (0, 0))
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                time_passed = pygame.time.get_ticks() - press_delay_start
                
                # 🌟 2초 대기 구간: emer 이미지가 머리 위로 슝~
                if time_passed < 2000:
                    emer_x -= 15 
                    screen.blit(emer_img, (emer_x, player_y - 150))
                    if time_passed >= 1900:
                        emer_x = WIDTH
                
                # 🌟 질문 표시 구간 (2초가 지났을 때)
                else:
                    if press_question_step == 1:
                        question = [
                            "Q. 후보님, 최근 청소년 모방 범죄가 늘어나면서 폭력성과 선정성이 높은 비디오",
                            "게임에 대한 국가 주도의 사전 심의 규제를 대폭 강화해야 한다는 목소리가 높습니다.",
                            "후보님께서는 이 규제안에 찬성하십니까?"
                        ]
                        choices = [
                            ("A. 국가 주도의 일방적 규제는 문화 산업을 위축시킵니다. 업계의 자율적 정화와 성숙한 게임 문화를 믿어야 합니다.", btn_A_rect),
                            ("B. 청소년 보호도 중요하고 산업 발전도 중요합니다. 취임 즉시 전문가 위원회를 꾸려 검토하겠습니다.", btn_B_rect),
                            ("C. 문제의 본질은 게임이 아니라 아이들이 처한 현실입니다. 아이들이 맘껏 뛰어놀 인프라부터 확충하겠습니다!", btn_C_rect),
                            ("D. 맞습니다! 우리 아이들을 망치는 불량 게임들은 모조리 법으로 금지하고 개발자들을 엄벌에 처해야 합니다!", btn_D_rect)
                        ]
                    else:
                        question = [
                            "Q. 후보님, 선거 자금이 0원에서 순식간에 엄청난 액수로 불어났습니다. 항간에는 지역",
                            "유지들로부터 출처를 알 수 없는 '프리미엄 사과 박스'를 은밀히 받았다는 의혹이 제기되고",
                            "있는데, 해명 부탁드립니다."
                        ]
                        choices = [
                            ("A. 그 '사과'들은 땀 흘리는 서민들의 붉은 응원의 결실입니다! 제게 씌워진 적폐 프레임에 굴하지 않겠습니다!", btn_A_rect),
                            ("B. 명백한 가짜 뉴스입니다. 1원 한 푼까지 투명하게 보고하고 있으며, 악의적 보도에는 법적 대응하겠습니다.", btn_B_rect),
                            ("C. 기자님, 요즘 사과값이 금값인데 저도 구경 좀 해보고 싶네요. 그 박스 어디 가면 받을 수 있습니까? 하하!", btn_C_rect),
                            ("D. 아니, 그 사과 박스는 제가 먼저 달라고 한 게 아니라… 그분들이 자발적으로 성의를 표시한 것뿐입니다!", btn_D_rect)
                        ]
                    
                    q_y = 120
                    for line in question:
                        q_surf = font_menu.render(line, True, (255, 255, 255))
                        screen.blit(q_surf, q_surf.get_rect(center=(WIDTH // 2, q_y)))
                        q_y += 45
                    
                    mouse_pos = pygame.mouse.get_pos()
                    for i, (text, rect) in enumerate(choices):
                        # 선택 후 반짝임 연출
                        if post_select_timer > 0:
                            if i == selected_btn_idx:
                                color_bg, color_text = ((255, 215, 0), (0, 0, 0)) if (post_select_timer // 10) % 2 == 0 else ((50, 50, 70), (255, 215, 0))
                            else:
                                color_bg, color_text = (10, 10, 15), (100, 100, 100)
                        else:
                            if rect.collidepoint(mouse_pos):
                                color_bg, color_text = (50, 50, 70), (255, 215, 0)
                            else:
                                color_bg, color_text = (20, 20, 30), (200, 200, 200)
                        
                        pygame.draw.rect(screen, color_bg, rect, border_radius=15)
                        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=15)
                        txt_surf = font_desc.render(text, True, color_text)
                        screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))
         
         
         
        # 🌟 [11] 떠오르는 점수 피드백 그리기 (마우스 누른 곳에서 발생!)
        next_floating = []
        for ft in floating_texts:
            text, color, pos, timer = ft
            
            # 검은색 얇은 테두리를 줘서 글씨가 더 잘 보이게 연출
            ft_surf = font_title.render(text, True, color)
            
            # 텍스트 위치를 위로 살짝씩 올리기
            pos[1] -= 2
            timer -= 1
            
            # 화면에 그리기
            screen.blit(ft_surf, ft_surf.get_rect(center=(pos[0], pos[1])))
            
            # 타이머가 남아있으면 다음 프레임에도 그리기 위해 리스트에 유지
            if timer > 0:
                next_floating.append([text, color, pos, timer])
        floating_texts = next_floating

        # [9] 화면 전환 효과
        if flash_timer > 0:
            flash_timer -= 1
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((255, 255, 255))
            screen.blit(overlay, (0, 0))   
        
        pygame.display.flip()
        clock.tick(FPS)

    # =====================================================================
    # 🌟 [수정 포인트] while running 루프가 끝나면 무조건 여기로 옵니다!
    # 들여쓰기를 딱 4칸(while running과 같은 세로줄)으로 맞췄습니다!
    # =====================================================================
    show_loading_screen()          # 1. 검은 화면에 Loading... 3초 띄우기
    show_ending_screen(score)      # 2. 점수를 넘겨줘서 100만 원 여부에 따라 엔딩 띄우기

pygame.quit()

sys.exit()

