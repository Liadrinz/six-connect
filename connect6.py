import pygame
import os
from chessboard import Chessboard 

WINDOW_WIDTH,WINDOW_HEIGHT = 720,720
GRID_WIDTH = WINDOW_WIDTH//20
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'image')

FPS = 60

pygame.init()
#设置窗口位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,100)
#创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.DOUBLEBUF,32)
#窗口标题
pygame.display.set_caption("Connect 6")
#加载图片
menu_bg = pygame.image.load(os.path.join(img_folder,'menu.jpg')).convert()
pve = pygame.image.load(os.path.join(img_folder,'PVE.png')).convert()
eve = pygame.image.load(os.path.join(img_folder,'EVE.png')).convert()
black_side = pygame.image.load(os.path.join(img_folder,'black.png')).convert()
white_side = pygame.image.load(os.path.join(img_folder,'white.png')).convert()
goback = pygame.image.load(os.path.join(img_folder,'goback.png')).convert()
title = pygame.image.load(os.path.join(img_folder,'title.png')).convert()

clock = pygame.time.Clock()
chessboard = Chessboard(WINDOW_WIDTH,WINDOW_HEIGHT)
ingame = True
while ingame:
    screen.fill(pygame.Color("WHITE"))
    screen.blit(menu_bg,(200,150))
    screen.blit(pve,(200,400))
    screen.blit(eve,(200,500))
    screen.blit(title,(180,40))

    in_menu = True
    pve_chosed = False
    running = False
    while in_menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ingame = False
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 200<pos[0]<408 and 400<pos[1]<450:
                    if pve_chosed == False:
                        pve_chosed = True
                        screen.fill(pygame.Color("WHITE"))
                        screen.blit(menu_bg,(200,150))
                        screen.blit(black_side,(200,400))
                        screen.blit(white_side,(200,500))
                        screen.blit(goback,(200,600))
                        screen.blit(title,(180,40))
                    else:
                        print("黑棋")
                        running = True
                        in_menu = False
                elif 200<pos[0]<408 and 500<pos[1]<550:
                    if pve_chosed == False:
                        print("AI对弈")
                        in_menu = False
                        running = True
                    else:
                        print("白棋")
                        running = True
                        in_menu = False
                if 200<pos[0]<408 and 600<pos[1]<650 and pve_chosed == True:
                    pve_chosed = False
                    screen.fill(pygame.Color("WHITE"))
                    screen.blit(menu_bg,(200,150))
                    screen.blit(pve,(200,400))
                    screen.blit(eve,(200,500))
                    screen.blit(title,(180,40))
                    
        pygame.display.update()


    if running == True:
        chessboard.draw_board(screen)

    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ingame = False
                running = False
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                grid = (int(round(event.pos[0] / (GRID_WIDTH + .0))-1),int(round(event.pos[1] / (GRID_WIDTH + .0))-1))
                chessboard.draw_coin("BLACK",grid,screen)

        

        pygame.display.update()
