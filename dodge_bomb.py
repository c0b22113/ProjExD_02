import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

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
        screen.blit(kk_img, [900, 400])
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