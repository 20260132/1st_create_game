import pygame
import os
import sys

# 1. [최상단] 파일 경로를 안전하게 찾아주는 함수
def resource_path(relative_path):
    """ 실행 파일(exe)로 만들었을 때도 이미지 경로를 정상적으로 찾게 해주는 함수 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 2. 게임창 및 초기 설정 (유니티의 Start 역할 일부)
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Walk Animation Test")
clock = pygame.time.Clock()

# 3. 스프라이트 시트 자동 분할 함수 (가로/세로 칸 수 기준)
def load_sprite_frames(filename, columns, rows):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    current_w, current_h = sprite_sheet.get_size()
    sprite_sheet = pygame.transform.scale(sprite_sheet, (current_w * 2.7, current_h * 2.7))
    sheet_width, sheet_height = sprite_sheet.get_size()
    
    # 이미지 원본 크기를 바탕으로 프레임 1개의 크기를 자동으로 계산합니다.
    frame_width = sheet_width // columns
    frame_height = sheet_height // rows
    
    frames = []
    
    # [핵심 수정] 픽셀 단위가 아닌 '칸 수(row, col)' 기준으로 정확히 잘라냅니다.
    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            
            # 자르려는 영역이 원본 이미지를 삐져나가지 않도록 안전장치 추가!
            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)
                
    return frames, frame_width, frame_height

# 4. 플레이어 클래스 정의
class Player:
    def __init__(self, sprite_filename):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.move_speed = 200.0 
        
        # 유니티 Animator와 호환되는 상태 딕셔너리
        self.animator = {
            "LeftMove": False, "RightMove": False,
            "UpMove": False, "DownMove": False, "MoveVal": 0.0
        }
        
        # 올려주신 Player.png 이미지에 맞춰 가로 3칸, 세로 4칸으로 정확히 쪼갭니다.
        self.frames, self.frame_width, self.frame_height = load_sprite_frames(sprite_filename, 3, 4)
        
        # 자른 프레임을 방향별로 배정 (위에서부터 아래, 왼쪽, 오른쪽, 위 순서)
        self.animations = {
            'down': self.frames[0:3],
            'left': self.frames[3:6],
            'right': self.frames[6:9],
            'up': self.frames[9:12]
        }
        
        self.direction = 'down'
        self.is_moving = False
        self.frame_index = 0
        self.animation_speed = 8 
        
        self.image = self.animations['down'][1] # 처음엔 앞모습으로 서 있기
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(self.x), int(self.y))

    # 유니티의 Move1() 함수 역할 (이동 및 애니메이션 처리)
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        xx = 0
        yy = 0
        self.is_moving = False
        
        # 아래쪽 (S 또는 DownArrow)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            yy = 1
            self.direction = 'down'
            self.is_moving = True
            self.animator["DownMove"] = True
        else:
            self.animator["DownMove"] = False

        # 위쪽 (W 또는 UpArrow)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            yy = -1
            self.direction = 'up'
            self.is_moving = True
            self.animator["UpMove"] = True
        else:
            self.animator["UpMove"] = False

        # 왼쪽 (A 또는 LeftArrow)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            xx = -1
            self.direction = 'left'
            self.is_moving = True
            self.animator["LeftMove"] = True
        else:
            self.animator["LeftMove"] = False

        # 오른쪽 (D 또는 RightArrow)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            xx = 1
            self.direction = 'right'
            self.is_moving = True
            self.animator["RightMove"] = True
        else:
            self.animator["RightMove"] = False

        # 움직임 여부 값 갱신
        if self.is_moving:
            self.animator["MoveVal"] = 1.0
        else:
            self.animator["MoveVal"] = 0.0

        # 좌표 계산 (유니티의 Time.deltaTime 적용)
        self.x += xx * self.move_speed * dt
        self.y += yy * self.move_speed * dt

        # 실제 화면 위치 업데이트
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # --- 애니메이션 프레임 업데이트 ---
        if self.is_moving:
            self.frame_index += self.animation_speed * dt
            current_frame_count = len(self.animations[self.direction])
            self.frame_index %= current_frame_count
            self.image = self.animations[self.direction][int(self.frame_index)]
        else:
            self.frame_index = 0 
            self.image = self.animations[self.direction][1] # 서 있는 프레임 고정

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# 5. [중요] 플레이어 객체 생성 및 이미지 경로 설정
# 올려주신 이미지 경로 규칙에 맞게 'assets/sprite/Player.png'로 넣어두었습니다.
# 만약 파일 이름이 Spaceship.png라면 아래 파일명만 원하는 대로 바꾸시면 됩니다!
player = Player(resource_path("assets/sprites/Player.png"))

running = True

# 6. 메인 게임 루프 (유니티의 Update() 역할)
while running:
    dt = clock.tick(60) / 1000.0  # 델타 타임 계산
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    player.update(dt)  # 이동 및 애니메이션 업데이트
    
    screen.fill((200, 200, 200)) # 연한 회색 배경으로 채우기
    player.draw(screen)          # 캐릭터 그리기
    pygame.display.flip()        # 화면 갱신

pygame.quit()