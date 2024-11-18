'''
这是注释：
左上是起点，右下是终点，玩家通过ASDW移动，注意提前调整键盘至 “英文模式 ”。
迷宫为 15 行，20 列，注意编程默认从 “0” 开始计数。每个格子均有对应坐标，注释在迷宫数组的右侧。
蓝色小点为缩小药水的位置，玩家碰撞到药水会变小。
(11, 9) 和 (13, 9) 为特殊格子，检测到玩家变小后才允许通过。添加图片素材时这两个格子需要和正常道路的格子区分开，显示出这里是需要喝药水变小才能通过的窄路。
    例如正常格子是草地素材，这里就是藤蔓素材。

11.14更新内容：
增加了绿色的引导小球（即兔子先生），引导玩家走到迷宫终点。
增加了玩家走过的格子的变白效果（后期可以替换成花朵生长的动画）。
增加了游戏开始时的对话框，方便添加故事情节和新手引导。
格子大小标准为40像素*40像素，尝试铺了草地素材，素材名称为grass2.gif。

11.18更新内容：
合并了素材图片。
增加了背景音乐。
尝试增加了游戏开始的文本框，停留4秒会消失。（后期可以按你的代码来我又做多余的东西了orz）
'''

import pygame
import sys
import os

# 初始化Pygame
pygame.init()

# 常量
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
PLAYER_RADIUS = 15
FPS = 30
PLAYER_SPEED = TILE_SIZE

# 文件夹路径
IMAGE_FOLDER = r"E:\programming\FINAL Project\final-project\images"
MUSIC_FOLDER = r"E:\programming\FINAL Project\final-project\music & soundscape"
MUSIC_FILE = "A-very-happy-christmas.mp3"

# 背景颜色定义
BACKGROUND_COLOR = "white"
# 文本框颜色定义
TEXTBOX_COLOR = (255, 255, 224)  # 浅黄色

# 迷宫布局（1表示墙壁，0表示路径）
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 对象位置
player_pos = [1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2]
exit_pos = (18, 13)
item_pos = [9 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2]
narrow_path_pos = [(11, 9), (13, 9)]

# 加载图片
def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            name = os.path.splitext(filename)[0]
            img = pygame.image.load(os.path.join(folder_path, filename))
            images[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return images

# Call the function to load images
images = load_images(IMAGE_FOLDER)

# 加载音乐
def load_music(music_file):
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_file))
    pygame.mixer.music.play(-1)

# 加载音乐
load_music(MUSIC_FILE)

# 防止中文输入法打字使游戏无法运行！！
pygame.key.stop_text_input()

# 游戏状态
player_shrunk = False
last_move_time = 0
move_cooldown = 100
textbox_visible = True  # Initialize textbox_visible to True
textbox_start_time = pygame.time.get_ticks()  # Initialize the start time for the textbox

# 设置显示窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# 绘制迷宫
def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:  # 墙壁
                if 'wall' in images:
                    screen.blit(images['wall'], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    pygame.draw.rect(screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 0:  # 路径
                if 'path' in images:
                    screen.blit(images['path'], (x * TILE_SIZE, y * TILE_SIZE))

def can_move(new_pos):
    grid_x = new_pos[0] // TILE_SIZE
    grid_y = new_pos[1] // TILE_SIZE
    if 0 <= grid_x < len(MAZE[0]) and 0 <= grid_y < len(MAZE):
        if MAZE[grid_y][grid_x] == 0:
            if (grid_x, grid_y) in narrow_path_pos and not player_shrunk:
                return False
            return True
    return False

# 绘制文本框
def draw_textbox():
    if textbox_visible:
        # 创建文本框的矩形
        textbox_rect = pygame.Rect((WIDTH - 700) // 2, HEIGHT - 100, 700, 100)

        # 创建一个带有圆角的文本框
        rounded_rect = pygame.Surface(textbox_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect, TEXTBOX_COLOR, (0, 0, textbox_rect.width, textbox_rect.height), border_radius=10)

        # 绘制描边
        pygame.draw.rect(rounded_rect, (229, 202, 96), (0, 0, textbox_rect.width, textbox_rect.height), width=5, border_radius=10)

        # 绘制带描边的圆角矩形
        screen.blit(rounded_rect, textbox_rect.topleft)

        font = pygame.font.Font(None, 24)
        speaker_text = font.render("Alice", True, (191, 155, 11))  # 黑色字体
        message_text = font.render("Yawn~ The air is so fresh in the forest!", True, (0, 0, 0))

        # 绘制文本
        screen.blit(speaker_text, (textbox_rect.x + 20, textbox_rect.y + 18))
        screen.blit(message_text, (textbox_rect.x + 20, textbox_rect.y + 46))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and textbox_visible:  # 按下任意键隐藏文本框
            textbox_visible = False

    # 检查文本框显示时间
    if textbox_visible and pygame.time.get_ticks() - textbox_start_time >= 4000:
        textbox_visible = False

    # 检查按键并更新位置
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    new_pos = player_pos[:]

    if current_time - last_move_time >= move_cooldown:
        if keys[pygame.K_w]:
            new_pos[1] -= PLAYER_SPEED
        elif keys[pygame.K_s]:
            new_pos[1] += PLAYER_SPEED
        elif keys[pygame.K_a]:
            new_pos[0] -= PLAYER_SPEED
        elif keys[pygame.K_d]:
            new_pos[0] += PLAYER_SPEED

        if can_move(new_pos):
            player_pos = new_pos
            last_move_time = current_time

        if abs(player_pos[0] - item_pos[0]) < TILE_SIZE // 2 and abs(player_pos[1] - item_pos[1]) < TILE_SIZE // 2:
            player_shrunk = True

    # 绘制游戏元素
    screen.fill(BACKGROUND_COLOR)
    draw_maze()

    # 绘制玩家
    if player_shrunk:
        if 'player_small' in images:
            screen.blit(images['player_small'], (player_pos[0] - TILE_SIZE // 2, player_pos[1] - TILE_SIZE // 2))
        else:
            pygame.draw.circle(screen, 'red', player_pos, PLAYER_RADIUS // 2)
    else:
        if 'player' in images:
            screen.blit(images['player'], (player_pos[0] - TILE_SIZE // 2, player_pos[1] - TILE_SIZE // 2))
        else:
            pygame.draw.circle(screen, 'red', player_pos, TILE_SIZE // 2)

    # 绘制缩小药水
    if 'shrinking_potion' in images:
        screen.blit(images['shrinking_potion'], (item_pos[0] - TILE_SIZE // 2, item_pos[1] - TILE_SIZE // 2))
    else:
        pygame.draw.circle(screen, "blue", item_pos, TILE_SIZE // 4)

    # 绘制出口
    if 'exit' in images:
        screen.blit(images['exit'], (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))
    else:
        pygame.draw.rect(screen, 'green', (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # 绘制狭窄路径
    if 'narrow_path' in images:
        for pos in narrow_path_pos:
            screen.blit(images['narrow_path'], (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
    else:
        for pos in narrow_path_pos:
            pygame.draw.rect(screen, 'grey', (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # 绘制文本框
    draw_textbox()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
