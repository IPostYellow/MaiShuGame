import pygame
import random
import math

# 初始化界面
pygame.init()  # 游戏初始化
screen = pygame.display.set_mode((800, 600))  # 屏幕大小
pygame.display.set_caption('太空飞机')  # 标题
icon = pygame.image.load('ufo.png')  # 读取图片
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.png')  # 背景图片
playerImg = pygame.image.load('player.png')  # 玩家飞机
playerX = 385  # 飞机X坐标，不能大过800-64.64是玩家飞机的宽
playerY = 500  # 飞机Y坐标
playerStep = 0  # 玩家移动的速度
# 得分
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
# 游戏结束
game_over = False
Game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def check_game_ouver():
    if game_over:
        text = 'Game Over!'
        render = Game_over_font.render(text, True, (255, 0, 0))
        screen.blit(render, (230, 250))
        pygame.mixer.music.stop()


def show_score():
    text = f'Score:{score}'  # 要显示的字
    score_render = font.render(text, True, (0, 255, 0))  # 渲染text.TRUE表示24色，然后三原色表示颜色
    screen.blit(score_render, (10, 10))  # 显示字体


running = True
pygame.mixer.music.load('bg.wav')  # 读取音乐
pygame.mixer.music.play(-1)  # 播放BGM -1表示循环播放

# 通过mixer创建了一个音效
burst_sound = pygame.mixer.Sound('exp.wav')  # 击中敌人的音效

number_of_enemies = 6  # 敌人数量


# 敌人类
class Enemy():
    def __init__(self, x, y, step):
        self.enemyImg = pygame.image.load('enemy.png')  # 敌人
        self.enemyX = x
        self.enemyY = y
        self.enemyStep = step

    # 刷新敌人
    def reset(self):
        self.enemyX = random.randint(200, 600)
        self.enemyY = random.randint(50, 250)


enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy(random.randint(200, 600), random.randint(50, 250), random.randint(2, 6)))


# 子弹类
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.bulletX = playerX + 16  # 子弹发射的X坐标应该在玩家飞机中间,飞机大小是64，子弹大小32.64-32除以2
        self.bulletY = playerY + 10
        self.step = 10  # 子弹的移动速度

    # 判断是否打中敌人
    def hit(self):
        global score
        for e in enemies:
            if (distance(self.bulletX, self.bulletY, e.enemyX, e.enemyY) < 30):
                burst_sound.play()
                if self in bullets:
                    bullets.remove(self)
                e.reset()
                score += 10
                # print(score)


bullets = []  # 保存现有子弹


def show_enemy():  # 刷新敌人
    global game_over
    for i in enemies:
        screen.blit(i.enemyImg, (i.enemyX, i.enemyY))
        i.enemyX += i.enemyStep
        # 防止敌人出界
        if (i.enemyX > 736) | (i.enemyX < 0):  # 敌人移动到边界就掉头
            i.enemyStep *= -1
            i.enemyY += 40
            if i.enemyY > 500 - 64:
                game_over = True
                print('游戏结束')
                enemies.clear()


def process_event():  # 事件控制
    global running, playerStep

    for event in pygame.event.get():  # 获取界面上的操作事件
        if event.type == pygame.QUIT:  # 如果界面上的操作是关闭,则关闭游戏
            running = False
        # 键盘按下任何一个键
        if event.type == pygame.KEYDOWN:
            # 键盘按下向左右方向键空格键
            if event.key == pygame.K_RIGHT:
                playerStep = 5
            if event.key == pygame.K_LEFT:
                playerStep = -5
            if event.key == pygame.K_SPACE:
                print('发射子弹')
                # 创建一颗子弹
                bullets.append(Bullet())

        # 键盘抬起任何键
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_LEFT):
                playerStep = 0


def move_player():  # 玩家移动
    global playerX, playerStep

    playerX += playerStep  # 玩家飞机移动
    # 防止飞机出界
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0


def show_bullets():  # 显示子弹
    for b in bullets:
        screen.blit(b.img, (b.bulletX, b.bulletY))
        b.bulletY -= b.step  # 移动子弹
        if b.bulletY < 0:  # 出界的子弹直接取消
            bullets.remove(b)
        b.hit()  # 是否击中了敌人


def distance(bx, by, ex, ey):  # 获取两点距离
    a = bx - ex
    b = by - ey
    return math.sqrt(a * a + b * b)


# 游戏主循环

while running:
    screen.blit(bgImg, (0, 0))  # 画出图片，以及它的左上角坐标（但是还不显示，你做完的所有事最后都必须要pygame.display.update()）
    show_score()  # 显示分数
    process_event()  # 事件处理
    move_player()  # 控制飞机
    screen.blit(playerImg, (playerX, playerY))  # 飞机位置
    show_enemy()  # 敌人出现
    show_bullets()  # 子弹出现
    check_game_ouver()  # 检测游戏是否结束
    pygame.display.update()  # 更新界面
