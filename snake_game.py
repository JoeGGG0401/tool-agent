import pygame
import random

# 初始化Pygame
pygame.init()

# 设置游戏窗口大小
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 设置游戏标题
pygame.display.set_caption('贪吃蛇游戏')

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 定义字体
FONT = pygame.font.SysFont(None, 30)

# 定义贪吃蛇的初始位置和大小
SNAKE_SIZE = 10
SNAKE_X = WINDOW_WIDTH / 2
SNAKE_Y = WINDOW_HEIGHT / 2

# 定义食物的初始位置和大小
FOOD_SIZE = 10
FOOD_X = random.randint(0, WINDOW_WIDTH - FOOD_SIZE)
FOOD_Y = random.randint(0, WINDOW_HEIGHT - FOOD_SIZE)

# 定义贪吃蛇的初始速度和方向
SNAKE_SPEED = 10
SNAKE_DIRECTION = 'right'

# 定义初始得分和最高得分
SCORE = 0
HIGH_SCORE = 0

# 定义游戏结束的函数
def game_over():
    global SCORE, HIGH_SCORE
    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE
    text = FONT.render('游戏结束！得分：{} 最高得分：{}'.format(SCORE, HIGH_SCORE), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    WINDOW.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    SCORE = 0
    reset()

# 定义重置游戏的函数
def reset():
    global SNAKE_X, SNAKE_Y, FOOD_X, FOOD_Y, SNAKE_DIRECTION
    SNAKE_X = WINDOW_WIDTH / 2
    SNAKE_Y = WINDOW_HEIGHT / 2
    FOOD_X = random.randint(0, WINDOW_WIDTH - FOOD_SIZE)
    FOOD_Y = random.randint(0, WINDOW_HEIGHT - FOOD_SIZE)
    SNAKE_DIRECTION = 'right'

# 游戏循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and SNAKE_DIRECTION != 'down':
                SNAKE_DIRECTION = 'up'
            elif event.key == pygame.K_DOWN and SNAKE_DIRECTION != 'up':
                SNAKE_DIRECTION = 'down'
            elif event.key == pygame.K_LEFT and SNAKE_DIRECTION != 'right':
                SNAKE_DIRECTION = 'left'
            elif event.key == pygame.K_RIGHT and SNAKE_DIRECTION != 'left':
                SNAKE_DIRECTION = 'right'

    # 移动贪吃蛇
    if SNAKE_DIRECTION == 'up':
        SNAKE_Y -= SNAKE_SPEED
    elif SNAKE_DIRECTION == 'down':
        SNAKE_Y += SNAKE_SPEED
    elif SNAKE_DIRECTION == 'left':
        SNAKE_X -= SNAKE_SPEED
    elif SNAKE_DIRECTION == 'right':
        SNAKE_X += SNAKE_SPEED

    # 判断贪吃蛇是否撞到墙壁
    if SNAKE_X < 0 or SNAKE_X > WINDOW_WIDTH - SNAKE_SIZE or SNAKE_Y < 0 or SNAKE_Y > WINDOW_HEIGHT - SNAKE_SIZE:
        game_over()

    # 判断贪吃蛇是否吃到食物
    if SNAKE_X < FOOD_X + FOOD_SIZE and SNAKE_X + SNAKE_SIZE > FOOD_X and SNAKE_Y < FOOD_Y + FOOD_SIZE and SNAKE_Y + SNAKE_SIZE > FOOD_Y:
        FOOD_X = random.randint(0, WINDOW_WIDTH - FOOD_SIZE)
        FOOD_Y = random.randint(0, WINDOW_HEIGHT - FOOD_SIZE)
        SCORE += 10

    # 绘制游戏界面
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, GREEN, [FOOD_X, FOOD_Y, FOOD_SIZE, FOOD_SIZE])
    pygame.draw.rect(WINDOW, WHITE, [SNAKE_X, SNAKE_Y, SNAKE_SIZE, SNAKE_SIZE])
    score_text = FONT.render('得分：{}'.format(SCORE), True, WHITE)
    high_score_text = FONT.render('最高得分：{}'.format(HIGH_SCORE), True, WHITE)
    WINDOW.blit(score_text, (10, 10))
    WINDOW.blit(high_score_text, (WINDOW_WIDTH - high_score_text.get_width() - 10, 10))
    pygame.display.update()

    # 判断贪吃蛇是否撞到自己的身体
    snake_head = [SNAKE_X, SNAKE_Y]
    snake_body = []
    for i in range(0, SCORE, 10):
        snake_body.append([SNAKE_X - i, SNAKE_Y])
    for body_part in snake_body:
        if snake_head == body_part:
            game_over()

    # 控制游戏帧率
    pygame.time.Clock().tick(30)