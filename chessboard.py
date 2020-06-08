import pygame
import os

class Chessboard(object):
    base_folder = os.path.dirname(__file__)
    img_folder = os.path.join(base_folder,'image')

    def __init__(self,width,height):
        self.background_img = pygame.image.load(os.path.join(self.img_folder,'background.jpg')).convert()
        self.height = height
        self.width = width
        self.grid_width = self.width // 20
        self.moves = []


    def draw_board(self,screen):
        screen.blit(pygame.transform.scale(self.background_img, (self.width,self.height)),(0,0))
        rec_lines = [((self.grid_width, self.grid_width), (self.grid_width, self.height - self.grid_width)),
                    ((self.grid_width, self.grid_width), (self.width - self.grid_width, self.grid_width)),
        ((self.grid_width, self.height - self.grid_width),
            (self.width - self.grid_width, self.height - self.grid_width)),
        ((self.width - self.grid_width, self.grid_width),
            (self.width - self.grid_width, self.height - self.grid_width)),]

        for line in rec_lines:
            pygame.draw.line(screen,pygame.Color("black"),line[0],line[1],2)

        for i in range(17):
            pygame.draw.line(screen, pygame.Color("black"),
                         (self.grid_width * (2 + i), self.grid_width),
                         (self.grid_width * (2 + i), self.height - self.grid_width))
            pygame.draw.line(screen, pygame.Color("black"),
                         (self.grid_width, self.grid_width * (2 + i)),
                         (self.height - self.grid_width, self.grid_width * (2 + i)))

        circle_center = [
        (self.grid_width * 4, self.grid_width * 4),
        (self.width - self.grid_width * 4, self.grid_width * 4),
        (self.width - self.grid_width * 4, self.height - self.grid_width * 4),
        (self.grid_width * 4, self.height - self.grid_width * 4),
        (self.grid_width * 10, self.grid_width * 10)]

        for cc in circle_center:
            pygame.draw.circle(screen, pygame.Color("black"), cc, 5)

    def draw_coin(self,side,position,screen):
        self.moves.append((position,side))
        for m in self.moves:
            pos = self.invertPosition(m[0])
            pygame.draw.circle(screen,pygame.Color(m[1]),pos,16)
        

    #转换位置变为UI中的坐标   
    def invertPosition(self,position):
        x = (position[0]+1)*self.grid_width
        y = (position[1]+1)*self.grid_width
        return (x,y)


    def draw_text(self,screen,text,size,x,y,color = "black"):
        font = pygame.font.Font(pygame.font.get_default_font(),size)
        text_serface = font.render(text,True,pygame.Color(color))
        text_rect = text_serface.get_rect()
        text_rect.midtop =(x,y)
        screen.blit(text_serface,text_rect)

    def make_move(self,pos,robot,step,player_side,screen):
        grid = (int(round(pos[0] / (self.grid_width + .0))-1),int(round(pos[1] / (self.grid_width + .0))-1))
        if robot.model.board[grid[1],grid[0]]==0:
            step = step+1
            robot.make_move((grid[1],grid[0]),player_side)
            self.draw_coin(player_side,grid,screen)
            pygame.display.update()
        return step

    def robot_move(self,robot,robot_side,screen):
        robot_step = robot.query(robot.model.board,robot_side)
        robot.make_move(robot_step,robot_side)
        self.draw_coin(robot_side,(robot_step[1],robot_step[0]),screen)
        pygame.display.update()
