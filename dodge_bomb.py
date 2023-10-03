import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = { # 練習3：キー入力に対する移動量
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


#  こうかとんと爆弾が画面の外に出ないようにせよ．
# • 画面内or画面外の判定をする関数を実装する
# • 引数：こうかとんRect or 爆弾Rect
# • 戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
# • Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
# • 更新後の座標が画面外になった場合の挙動
# • こうかとん：更新前の位置に戻す／爆弾：速度の符号を反転する
def check_bound(obj_rct: pg.Rect):
    """
    引数:こうかとんRect or 爆弾Rect
    戻り値:横方向・縦方向の真理値タプル（True:画面内/False:画面外）
    """
    status = [True, True]
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        status[0] = False
        return status
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        status[1] = False
        return status


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_rct = kk_img.get_rect()
    kk_img_rct.center = (900, 400) # こうかとんの初期位置

    """爆弾"""
    bomb = pg.Surface((20, 20))
    bomb.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb.get_rect()
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 画面サイズにランダムに配置
    bomb_rct.center = (x, y) # 画面中央に配置
    vx, vy = 5, 5 # 速度

    clock = pg.time.Clock()

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        total_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                total_mv[0] += mv[0]
                total_mv[1] += mv[1]

        screen.blit(kk_img, kk_img_rct)
        kk_img_rct.move_ip(total_mv[0], total_mv[1]) # こうかとんの移動

        """爆弾"""
        screen.blit(bomb, bomb_rct)
        bomb_rct.move_ip(vx, vy) # bombの移動

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()