import pygame
import os
from chessboard import Chessboard 
from robot import Robot
import time

WINDOW_WIDTH,WINDOW_HEIGHT = 720,720
GRID_WIDTH = WINDOW_WIDTH//20
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'image')

FPS = 30

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
ingame = True
while ingame:
    screen.fill(pygame.Color("white"))
    screen.blit(menu_bg,(200,150))
    screen.blit(pve,(200,400))
    screen.blit(eve,(200,500))
    screen.blit(title,(180,40))

    in_menu = True
    pve_chosed = False
    running = False
    player_side = ""
    robot_side = ""
    robot1_side = "black"
    robot2_side = "white"
    first_step = True
    tie = False
    gameover = False
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
                        screen.fill(pygame.Color("white"))
                        screen.blit(menu_bg,(200,150))
                        screen.blit(black_side,(200,400))
                        screen.blit(white_side,(200,500))
                        screen.blit(goback,(200,600))
                        screen.blit(title,(180,40))
                    else:
                        print("黑棋")
                        running = True
                        in_menu = False
                        player_side = "black"
                        robot_side = "white"
                elif 200<pos[0]<408 and 500<pos[1]<550:
                    if pve_chosed == False:
                        print("AI对弈")
                        in_menu = False
                        running = True
                    else:
                        print("白棋")
                        running = True
                        in_menu = False
                        player_side = "white"
                        robot_side = "black"
                        first_step = False
                if 200<pos[0]<408 and 600<pos[1]<650 and pve_chosed == True:
                    pve_chosed = False
                    screen.fill(pygame.Color("white"))
                    screen.blit(menu_bg,(200,150))
                    screen.blit(pve,(200,400))
                    screen.blit(eve,(200,500))
                    screen.blit(title,(180,40))
                    
        pygame.display.update()


    if running == True:
        chessboard = Chessboard(WINDOW_WIDTH,WINDOW_HEIGHT)
        chessboard.draw_board(screen)
        robot = Robot()
        robot.start()
        if pve_chosed == True: 
            robot.set_param()
            if robot_side == "black":
                robot_step = robot.query(robot.model.board,robot_side)
                robot.make_move(robot_step,robot_side)
                chessboard.draw_coin(robot_side,(robot_step[1],robot_step[0]),screen)
        else:
            robot.set_param()
            robot_step = robot.query(robot.model.board,robot1_side)
            robot.make_move(robot_step,robot1_side)
            chessboard.draw_coin(robot1_side,(robot_step[1],robot_step[0]),screen)
        pygame.display.update()
        
    step = 0
    #人机对弈游戏循环
    while running and pve_chosed:
        clock.tick(FPS)
        if step == 2 and gameover == False:
            tie = chessboard.robot_move(robot,robot_side,screen)
            tie = chessboard.robot_move(robot,robot_side,screen)
            step=0
        if tie == True:
            chessboard.draw_text(screen,"和棋！",50,360,300)
            gameover = True
        if robot.judge(robot.model.board)!=None:
            result = robot.judge(robot.model.board)
            gameover =True
            if result=="black":
                chessboard.draw_text(screen,"黑棋胜！",50,360,300)
            else:
                chessboard.draw_text(screen,"白棋胜！",50,360,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type ==pygame.MOUSEBUTTONDOWN and first_step==True:
                first_step = False
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pos = event.pos
                if GRID_WIDTH<=pos[0]<=WINDOW_WIDTH-GRID_WIDTH and GRID_WIDTH<=pos[1]<=WINDOW_HEIGHT-GRID_WIDTH:
                    chessboard.make_move(pos,robot,step,player_side,screen)
                    chessboard.robot_move(robot,robot_side,screen)
                    chessboard.robot_move(robot,robot_side,screen)
                pygame.event.set_allowed(None)
            elif event.type ==pygame.MOUSEBUTTONDOWN and step!=2 and gameover == False:
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pos = event.pos
                if GRID_WIDTH<=pos[0]<=WINDOW_WIDTH-GRID_WIDTH and GRID_WIDTH<=pos[1]<=WINDOW_HEIGHT-GRID_WIDTH:
                    step = chessboard.make_move(pos,robot,step,player_side,screen)
                pygame.event.set_allowed(None)
    #AI对弈游戏循环   
    while running and pve_chosed == False:
        clock.tick(FPS)
        if tie == True:
            gameover = True
            chessboard.draw_text(screen,"和棋！",50,360,300)
        if robot.judge(robot.model.board)!=None:
            gameover = True
            result = robot.judge(robot.model.board)
            if result=="black":
                chessboard.draw_text(screen,"黑棋胜！",50,360,300)
            else:
                chessboard.draw_text(screen,"白棋胜！",50,360,300)
        if gameover == False:
            tie = chessboard.robot_move(robot,robot2_side,screen)
            time.sleep(0.5)
            tie = chessboard.robot_move(robot,robot2_side,screen)

            tie = chessboard.robot_move(robot,robot1_side,screen)
            time.sleep(0.5)
            tie = chessboard.robot_move(robot,robot1_side,screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
