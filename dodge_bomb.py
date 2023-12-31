import random
import time
import math
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(obj_rct: pg.Rect):
    """
    引数: こうかとんRect or 爆弾Rect
    戻り値: タプル(横方向の衝突判定, 縦方向の衝突判定)
    画面ないならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def load_and_convert_images():
    """
    戻り値: 背景画像, こうかとん画像
    """
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    return bg_img, kk_img


def create_bomb():
    """
    戻り値: 爆弾画像, 爆弾Rect
    """
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)
    return bd_img, bd_rct


def get_rotation_angle_and_flip(mv: tuple) -> tuple:
    """
    引数: 移動量 (mv)
    戻り値: 回転角度, 反転フラグ
    """
    angles = {
        (0, -5): (90, True),
        (-5, -5): (-45, False),
        (-5, 0): (0, False),
        (-5, +5): (45, False),
        (0, +5): (-90, True),
        (+5, +5): (-45, True),
        (+5, 0): (0, True),
        (+5, -5): (45, True)
    }
    return angles.get(mv, (0, False))


def move_character(kk_rct, delta):
    """
    引数: こうかとんRect, キー入力に対応した移動量
    戻り値: こうかとんの移動量, 回転角度, 反転フラグ
    """
    key_lst = pg.key.get_pressed()
    sum_mv = [0, 0]
    for key, mv in delta.items():
        if key_lst[key]:
            sum_mv[0] += mv[0]
            sum_mv[1] += mv[1]

    rotation_angle, flip = get_rotation_angle_and_flip(tuple(sum_mv)) # 回転角度と反転フラグを取得

    kk_rct.move_ip(sum_mv[0], sum_mv[1])
    if check_bound(kk_rct) != (True, True):
        kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

    return sum_mv, rotation_angle, flip


def move_bomb(bd_rct, vx, vy):
    """
    引数: 爆弾Rect, 爆弾の移動量
    戻り値: 爆弾の移動量
    """
    bd_rct.move_ip(vx, vy)
    yoko, tate = check_bound(bd_rct)
    if not yoko:
        vx *= -1
    if not tate:
        vy *= -1
    return vx, vy


def draw_images(screen, bg_img, kk_img, kk_rct, bd_img, bd_rct, rotation_angle, flip):
    """
    引数：スクリーン, 背景画像, こうかとん画像, こうかとんRect, 爆弾画像, 爆弾Rect, 回転角度, 反転フラグ
    """
    screen.blit(bg_img, [0, 0])

    kk_img_to_draw = kk_img
    if flip:
        kk_img_to_draw = pg.transform.flip(kk_img, True, False)
    kk_img_to_draw = pg.transform.rotozoom(kk_img_to_draw, rotation_angle, 1.0)

    screen.blit(kk_img_to_draw, kk_rct)
    screen.blit(bd_img, bd_rct)


def increase_speed(vx, vy, speed_multiplier):
    """
    速度を増加させつつ、方向を保持

    引数:
    vx, vy: 現在のx方向およびy方向の速度
    speed_multiplier: 速度を増加させる係数

    戻り値:
    vx, vy: x方向およびy方向の増加した速度
    """
    # 現在の速度の大きさを計算します。
    speed = math.sqrt(vx**2 + vy**2)

    # 現在の速度がゼロでない場合、正規化された方向を計算し、速度を更新します。
    if speed != 0:
        dir_x, dir_y = vx/speed, vy/speed
        vx = dir_x * speed * speed_multiplier
        vy = dir_y * speed * speed_multiplier

    return vx, vy


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img, kk_img = load_and_convert_images()

    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)

    kk_img_hit = pg.image.load("ex02/fig/8.png") # 爆弾接触時の画像
    kk_img_hit = pg.transform.rotozoom(kk_img_hit, 0, 2.0)

    bd_img, bd_rct = create_bomb()
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    initial_vx, initial_vy = +5, +5  # 初期速度を変数として定義
    vx, vy = initial_vx, initial_vy  # 初期速度を設定

    clock = pg.time.Clock()
    tmr = 0  # 時間経過をカウントする変数

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bd_rct):
            draw_images(screen, bg_img, kk_img_hit, kk_rct, bd_img, bd_rct, 0, False) # 爆弾接触時の画像を描画(角度、反転なし)
            pg.display.update()
            time.sleep(2) # 2秒間待ってから終了
            print("GAME OVER")
            return

        if tmr > 0 and tmr % 600 == 0:
            speed_multiplier = 1 + (tmr // 500) * 0.5 # 500フレームごとに速度を50%ずつ増やす
            speed_multiplier = min(speed_multiplier, 10) # 速度は最大で初期速度の10倍
            vx, vy = increase_speed(vx, vy, speed_multiplier) # 速度を増加


        sum_mv, rotation_angle, flip = move_character(kk_rct, delta) # こうかとんの移動量、回転角度、反転フラグを取得
        vx, vy = move_bomb(bd_rct, vx, vy) # 爆弾の移動量を取得
        draw_images(screen, bg_img, kk_img, kk_rct, bd_img, bd_rct, rotation_angle, flip) # 画像を描画

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
