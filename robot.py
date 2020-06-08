import numpy as np

from model import ABModel

class Robot:

    def start(self):
        '''
        初始化机器人, 重新开局时也可调用, 无需新建对象
        '''
        self.model = ABModel()
    
    def set_param(self, depth=3):
        '''
        设置机器人的参数
        - side: 机器人棋子颜色, 取值为'black'或'white'
        - depth: Alpha-Beta搜索的深度
        '''
        self.depth = depth

    def judge(self, board):
        '''
        判断该局面是否有一方胜利
        - 入参
            - board: 二维数组
        - 返回值
            - side: None表示无人胜利, 'black'表示黑棋胜利, 'white'表示白棋胜利
        '''
        return self.model.judge()

    def query(self, board,side):
        '''
        查询在棋盘局面为board的情形下, 对于机器人而言最好的一步
        - 入参
            - board: 二维数组
        - 返回值
            - movement: 二元组, 表示下棋坐标, 返回None代表死局(和棋)
        '''
        assert self.depth > 0 and side in ['black', 'white']
        val = self.model.search(self.depth, side)
        if self.model.best_move is None:
            return np.random.randint(0, 19, size=2)
        if self.model.no_move:
            return None
        return self.model.best_move

    def make_move(self, movement,side):
        '''
        让一方走一步棋
        - 入参
            - movement: 二元组, 下棋的坐标
        '''
        self.model.take(*movement, side)
    