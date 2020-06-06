import pygame
import os
from chessboard import Chessboard 

WINDOW_WIDTH,WINDOW_HEIGHT = 720,720
GRID_WIDTH = WINDOW_WIDTH//20

FPS = 60

pygame.init()
#设置窗口位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)
#创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.DOUBLEBUF,32)
#窗口标题
pygame.display.set_caption("Connect 6")

clock = pygame.time.Clock()
chessboard = Chessboard(WINDOW_WIDTH,WINDOW_HEIGHT)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type ==pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            grid = (int(round(event.pos[0] / (GRID_WIDTH + .0))),int(round(event.pos[1] / (GRID_WIDTH + .0))))

    chessboard.draw_board(screen)   

    pygame.display.flip()
