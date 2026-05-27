import pygame
import os
import sys

# 1. 파일 경로를 안전하게 찾아주는 함수
def resource_path(relative_path):
    """ 실행 파일(exe)로 만들었을 때도 이미지 경로를 정상적으로 찾게 해주는 함수 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 2. 게임창 및 초기 설정
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Walk Animation & Fence Collision")
clock = pygame.time.Clock()

# 3. 스프라이트 시트 자동 분할 함수
def load_sprite_frames(filename, columns, rows):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    current_w, current_h = sprite_sheet.get_size()
    sprite_sheet = pygame.transform.scale(sprite_sheet, (int(current_w * 2.7), int(current_h * 2.7)))
    sheet_width, sheet_height = sprite_sheet.get_size()
    
    frame_width = sheet_width // columns
    frame_height = sheet_height // rows
    
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)
                
    return frames, frame_width, frame_height

# ==========================================
# 4. 울타리 관리 클래스 (통합됨)
# ==========================================
class FenceManager:
    def __init__(self, screen_width, screen_height, image_path):
        # 1. 울타리 이미지 로드 및 3배 확대
        original_fence_image = pygame.image.load(image_path).convert_alpha()
        f_w, f_h = original_fence_image.get_size()
        self.fence_image = pygame.transform.scale(original_fence_image, (int(f_w * 3.0), int(f_h * 3.0)))
        
        self.fence_width = self.fence_image.get_width()
        
        # 2. 화면 가로 크기를 채우기 위해 필요한 울타리 개수 계산
        self.num_fences = (screen_width // self.fence_width) + 1 
        
        # 3. 세로 위치: 중앙보다 살짝 위 (-50 픽셀)
        self.fence_y_pos = (screen_height // 2) - 50 
        
        # 4. 충돌 상자(Rect) 리스트 생성
        self.fence_rects = []
        for i in range(self.num_fences):
            rect = pygame.Rect(i * self.fence_width, self.fence_y_pos, self.fence_width, self.fence_image.get_height())
            self.fence_rects.append(rect)

    def draw(self, surface):
        # 계산된 위치에 울타리들을 일렬로 그립니다.
        for i in range(self.num_fences):
            surface.blit(self.fence_image, (i * self.fence_width, self.fence_y_pos))


# ==========================================
# 5. 플레이어 클래스
# ==========================================
class Player:
    def __init__(self, sprite_filename):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.move_speed = 200.0 
        
        self.animator = {
            "LeftMove": False, "RightMove": False,
            "UpMove": False, "DownMove": False, "MoveVal": 0.0
        }
        
        self.frames, self.frame_width, self.frame_height = load_sprite_frames(sprite_filename, 3, 4)
    
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
        
        self.image = self.animations['down'][1]
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(self.x), int(self.y))

    def update(self, dt, fences): 
        keys = pygame.key.get_pressed()
        
        xx = 0
        yy = 0
        self.is_moving = False
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            yy = 1
            self.direction = 'down'
            self.is_moving = True
            self.animator["DownMove"] = True
        else:
            self.animator["DownMove"] = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            yy = -1
            self.direction = 'up'
            self.is_moving = True
            self.animator["UpMove"] = True
        else:
            self.animator["UpMove"] = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            xx = -1
            self.direction = 'left'
            self.is_moving = True
            self.animator["LeftMove"] = True
        else:
            self.animator["LeftMove"] = False

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            xx = 1
            self.direction = 'right'
            self.is_moving = True
            self.animator["RightMove"] = True
        else:
            self.animator["RightMove"] = False

        if self.is_moving:
            self.animator["MoveVal"] = 1.0
        else:
            self.animator["MoveVal"] = 0.0

        # 이동 전 좌표 기억
        old_x = self.x
        old_y = self.y

        # 이동 처리
        self.x += xx * self.move_speed * dt
        self.y += yy * self.move_speed * dt

        # 캐릭터 충돌 상자 갱신
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 울타리와의 충돌 검사
        for f_rect in fences:
            if self.rect.colliderect(f_rect):
                # 충돌 시 원래 위치로 복구 (못 지나가게 함)
                self.x = old_x
                self.y = old_y
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                break 
        
        # 애니메이션 프레임 업데이트
        if self.is_moving:
            self.frame_index += self.animation_speed * dt
            current_frame_count = len(self.animations[self.direction])
            self.frame_index %= current_frame_count
            self.image = self.animations[self.direction][int(self.frame_index)]
        else:
            self.frame_index = 0 
            self.image = self.animations[self.direction][1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ==========================================
# 6. 메인 게임 루프 및 객체 생성
# ==========================================
# 객체 생성 (이미지 경로를 자신의 환경에 맞게 확인하세요)
fence_manager = FenceManager(SCREEN_WIDTH, SCREEN_HEIGHT, resource_path("assets/sprites/Fense.png"))
player = Player(resource_path("assets/sprites/Player.png"))

running = True

while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 업데이트: 플레이어에게 울타리 충돌 상자 리스트를 넘겨줍니다.
    player.update(dt, fence_manager.fence_rects)
    
    screen.fill((200, 200, 200))
    
    # 그리기: 울타리를 먼저 그려야 캐릭터가 가려지지 않습니다.
    fence_manager.draw(screen)
    player.draw(screen)          
    
    pygame.display.flip()

pygame.quit()