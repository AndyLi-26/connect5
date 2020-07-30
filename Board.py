import sys
from tkinter import messagebox
class chess:
    def __init__(self):
        self.color=' '
        self.number=None

    def __eq__(self, other):
        return self.color==other
    
    def __lt__(self,other):
        return self.number<other.number
    

class node:
    def __init__(self):
        self.num = 0
        self.broken = False
        self.breakPoint = (None, None)
        self.selfbreak = False

    def p(self, node):
        self.num = node.num + 1
        self.broken = node.broken
        self.breakPoint = node.breakPoint
        self.selfbreak = False

    def newBreak(self, num, bPoint):
        self.selfbreak = True
        self.num = num
        self.breakPoint = bPoint
        self.broken = True

    def __str__(self):
        output = str(self.num) + str(self.breakPoint)
        return output


class board:
    def __init__(self, player):
        ###W for white and B for black
        self.board = [[chess() for _ in range(15)] for _ in range(15)]
        self.steps=0
        self.run = True
        self.new = False
        self.rectSize = 64
        self.zeroPoint = 50
        self.ovalSize = 16
        if player == 'W':
            self.computer = 'B'
            self.player = 'W'
        else:
            self.computer = 'W'

            self.player = 'B'

    def place(self, color, x, y):
        self.steps+=1
        if (color == 'W' or color == 'B') and (0 <= x < 15 and 0 <= y < 15):
            self.board[x][y].color = color
            self.board[x][y].number=self.steps

    def remove(self,x, y):
        if 0 <= x < 15 and 0 <= y < 15:
            self.board[x][y].color = ' '
            self.board[x][y].number=None

    def regreat(self):
        print(self.steps)
        for x,line in enumerate(self.board):
            for y,spot in enumerate(line):
                if spot.number==self.steps or spot.number==self.steps-1:
                    print("for debug")
                    self.remove(x,y)
        self.steps-=2


    def check(self, color, canvas, winCheck=False):
        '''
        check the number of same color in line
        '''

        def has(DP, item):
            ### check if the num is in the DPsol
            position = []
            for x, line in enumerate(DP):
                for y, place in enumerate(line):
                    if place.num == item:
                        position.append((x, y, place.selfbreak))
            return -1 if position == [] else position

        def printDP(DP):
            for x in range(len(DP)):
                for y in range(len(DP)):
                    print('(',y,',',x,')',DP[y][x],end='  ',sep='')
                print()

        def check_v(color, canvas, winCheck=False):
            '''
            check vertical
            '''

            ################################### constructing DP ###############################################
            DP = [[node() for _ in range(15)] for _ in range(15)]
            for x in range(15):
                for y in range(1, 15):
                    if self.board[x][y] == color:
                        DP[x][y].p(DP[x][y - 1])
                        if DP[x][
                            y].broken:  ### if broken, add one to the break point to update the potential length of that point
                            a, b = DP[x][y].breakPoint
                            DP[a][b].num += 1
                        if DP[x][y].num == 5 and DP[x][y].broken == False:
                            self.run = False
                            if color == 'W':
                                self.new = messagebox.askquestion('Sorry',
                                                                  'Computer won the game, do you want to start a new game?')
                            elif color == 'B':
                                self.new = messagebox.askquestion('Congratulation',
                                                                  'You won the game, do you want to start a new game?')

                    ### break situation
                    if y - 2 >= 0 and self.board[x][y] == color and self.board[x][y - 1] == ' ' and DP[x][
                        y - 2].num != 0:
                        DP[x][y].p(DP[x][y - 1])
                        DP[x][y].breakPoint = (x, y - 1)
                        DP[x][y].broken = True
                        DP[x][y-1].newBreak(DP[x][y - 2].num + 1, (x, y - 1))
                        '''DP[x][y].p(DP[x][y - 2])
                        DP[x][y].broken = True'''
            if winCheck:
                return

            ################################################ find 4 #########################################
            final = has(DP, 4)
            if final != -1:
                for (x, y, selfbreak) in final:
                    if not selfbreak:
                        if y + 1 < 15 and self.board[x][y + 1] == ' ':
                            return [(25, (x, y + 1))]  ### 4 has value of 25, win instantly
                        if y - 4 >= 0 and self.board[x][y - 4] == ' ':
                            return [(25, (x, y - 4))]  ### 4 has value of 25, win instantly
                    else:
                        return [(25, (x, y))]  ### 4 has value of 25, win instantly
            moves = []
            ################################################ find 3 #########################################
            final = has(DP, 3)
            if final != -1:
                for (x, y, selfbreak) in final:
                    if not selfbreak:
                        validPosition = []
                        value = 2
                        if y + 1 < 15 and self.board[x][y + 1] == ' ':
                            value += 0.5
                            validPosition.append((x, y + 1))
                        if y - 3 >= 0 and self.board[x][y - 3] == ' ':
                            value += 0.5
                            validPosition.append((x, y - 3))
                        if value != 2:
                            moves.append((value, validPosition))
                        '''if (y + 1 < 15 and self.board[x][y + 1] == ' ') and (
                                y - 3 >= 0 and self.board[x][y - 3] == ' '):
                            if predict:
                                potential += 1
                            else:
                                return (3, (x, y + 1))  ### need to be improved'''
                    else:
                        value = 2
                        forward = DP[x][y - 1].num
                        if y - 1 - forward >= 0 and self.board[x][y - 1 - forward] == ' ':
                            value += 0.5
                        if y + 4 - forward < 15 and self.board[x][y + 4 - forward] == ' ':
                            value += 0.5
                        if value != 2:
                            moves.append((value, [(x, y)]))

                    '''if (y + 1 < 15 and self.board[x][y + 1] == ' ') and (
                                y - 4 >= 0 and self.board[x][y - 4] == ' '):
                            if predict:
                                potential += 1
                            else:
                                return (3, DP[x][y].breakPoint)'''

            ################################################ find live 2#########################################
            final = has(DP, 2)
            if final != -1:
                for (x, y, selfbreak) in final:
                    value = 1
                    if not selfbreak:
                        validPosition = []
                        if y + 1 < 15 and self.board[x][y + 1] == ' ':
                            value += 0.5
                            validPosition.append((x, y + 1))
                        if y - 2 >= 0 and self.board[x][y - 2] == ' ':
                            value += 0.5
                            validPosition.append((x, y - 2))
                        if value != 1:
                            moves.append((value, validPosition))
                    else:
                        if y + 2 < 15 and self.board[x][y + 2] == ' ':
                            value += 0.5
                        if y - 2 >= 0 and self.board[x][y - 2] == ' ':
                            value += 0.5
                        if value != 1:
                            moves.append((value, [(x, y)]))
            print("     moves for vertical: ", moves)
            return None if moves == [] else moves

        def check_h(color, canvas, winCheck=False):
            '''
            check horizontal
            '''
            #####################constructing DP array########################################
            DP = [[node() for _ in range(15)] for _ in range(15)]
            for x in range(1, 15):
                for y in range(15):
                    if self.board[x][y] == color:
                        DP[x][y].p(DP[x - 1][y])
                        if DP[x][y].broken:
                            a, b = DP[x][y].breakPoint
                            DP[a][b].num += 1
                        if DP[x][y].num == 5 and DP[x][y].broken == False:
                            self.run = False
                            if color == 'W':
                                self.new = messagebox.askquestion('Sorry',
                                                                  'Computer won the game, do you want to start a new game?')
                            elif color == 'B':
                                self.new = messagebox.askquestion('Congratulation',
                                                                  'You won the game, do you want to start a new game?')
                    ### break situation
                    if x - 2 >= 0 and self.board[x][y] == color and self.board[x - 1][y] == ' ' and DP[x - 2][
                        y].num != 0:
                        DP[x][y].p(DP[x - 1][y])
                        DP[x][y].breakPoint = (x - 1, y)
                        DP[x][y].broken = True
                        DP[x - 1][y].newBreak(DP[x - 2][y].num+1, (x - 1, y))

            if winCheck:
                return
            ############################################ find 4 ###########################################
            final = has(DP, 4)
            if final != -1:
                for (x, y, selfbreak) in final:
                    if not selfbreak:
                        if x + 1 < 15 and self.board[x + 1][y] == ' ':
                            print('got here')
                            return [(25, (x + 1, y))]  ### 4 has value of 25, win instantly
                        elif x - 4 >= 0 and self.board[x - 4][y] == ' ':
                            return [(25, (x - 4, y))] ### 4 has value of 25, win instantly
                    else:
                        return [(25, (x, y))] ### 4 has value of 25, win instantly

            moves = []  ###used to store all the potential moves, to calc (1move, multiple 3 or 4 later)

            ####################################################### find live 3 ######################################
            final = has(DP, 3)
            if final != -1:
                for (x, y, selfbreak) in final:
                    if not selfbreak:  ### if not broken, any empty side can be potential moves
                        validPosition = []
                        value = 2
                        if x + 1 < 15 and self.board[x + 1][y] == ' ':
                            value += 0.5
                            validPosition.append((x + 1,y))
                        if x - 3 >= 0 and self.board[x - 3][y] == ' ':
                            value += 0.5
                            validPosition.append((x - 3,y))
                        if value!=2:
                            moves.append((value, validPosition))
                    else:  ### if broken, only breaking point can be treat as potential 3 and both side need to be free
                        value = 2
                        forward = DP[x - 1][y].num
                        if x - 1 - forward >= 0 and self.board[x - 1 - forward][y] == ' ':
                            value += 0.5
                        if x + 4 - forward < 15 and self.board[x + 4 - forward][y] == ' ':
                            value += 0.5
                        if value != 2:
                            moves.append((value, [(x, y)]))


            ######################################## find live 2 ########################################
            final = has(DP, 2)
            if final != -1:
                for (x, y, selfbreak) in final:
                    value = 1
                    if not selfbreak:
                        validPosition = []
                        if x + 1 < 15 and self.board[x + 1][y] == ' ':
                            value += 0.5
                            validPosition.append((x + 1, y))
                        if x - 2 >= 0 and self.board[x - 2][y] == ' ':
                            value += 0.5
                            validPosition.append((x - 2, y))
                        if value != 1:
                            moves.append((value, validPosition))
                    else:
                        if x + 2 < 15 and self.board[x + 2][y] == ' ':
                            value += 0.5
                        if x - 2 >= 0 and self.board[x - 2][y] == ' ':
                            value += 0.5
                        if value != 1:
                            moves.append((value, [(x, y)]))
            print("     moves for horizontal: ", moves)
            return None if moves == [] else moves

        def check_a(color, canvas, winCheck=False):
            '''
            check angle
            '''
            def check_a1(color, canvas, winCheck=False):
                '''
                check \
                '''
                ################################### constructing DP ###############################################
                DP = [[node() for _ in range(15)] for _ in range(15)]
                for x in range(1, 15):
                    for y in range(1, 15):
                        if self.board[x][y] == color:
                            DP[x][y].p(DP[x - 1][y - 1])
                            if DP[x][y].broken:
                                a, b = DP[x][y].breakPoint
                                DP[a][b].num += 1
                            if DP[x][y].num == 5 and DP[x][y].broken == False:
                                self.run = False
                                if color == 'W':
                                    self.new = messagebox.askquestion('Sorry',
                                                                      'Computer won the game, do you want to start a new game?')
                                elif color == 'B':
                                    self.new = messagebox.askquestion('Congratulation',
                                                                      'You won the game, do you want to start a new game?')
                        if x - 2 >= 0 and y - 2 >= 0 and self.board[x][y] == color and self.board[x - 1][
                            y - 1] == ' ' and DP[x - 2][y - 2].num != 0:
                            DP[x][y].p(DP[x - 1][y-1])
                            DP[x][y].breakPoint = (x - 1, y-1)
                            DP[x][y].broken = True
                            DP[x - 1][y-1].newBreak(DP[x - 2][y-2].num+1, (x - 1, y-1))
                            '''
                            DP[x][y].p(DP[x - 2][y - 2])
                            DP[x][y].breakPoint = (x - 1, y - 1)
                            DP[x][y].broken = True'''
                if winCheck:
                    return
                ############################## find 4 ##########################################################
                final = has(DP, 4)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        if not selfbreak:
                            if x + 1 < 15 and y + 1 < 15 and self.board[x + 1][y + 1] == ' ':
                                return [(25, (x + 1, y + 1))]   ### 4 has value of 25, win instantly
                            if y - 4 >= 0 and x - 4 >= 0 and self.board[x - 4][y - 4] == ' ':
                                return [(25, (x - 4, y - 4))]   ### 4 has value of 25, win instantly
                        else:
                            return [(25, (x,y))]  ### 4 has value of 25, win instantly

                ################################# find live 3 ####################################################
                moves=[]
                final = has(DP, 3)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        if not selfbreak:
                            validPosition = []
                            value = 2
                            if x + 1 < 15 and y+1<15 and self.board[x + 1][y+1] == ' ':
                                value += 0.5
                                validPosition.append((x + 1,y+1))
                            if x - 3 >= 0 and y-3>0 and self.board[x - 3][y-3] == ' ':
                                value += 0.5
                                validPosition.append((x-3,y-3))
                            if value != 2:
                                moves.append((value, validPosition))
                            '''if (x + 1 < 15 and y + 1 < 15 and self.board[x + 1][y + 1] == ' ') and (
                                    y - 3 >= 0 and x - 3 >= 0 and self.board[x - 3][y - 3] == ' '):
                                if predict:
                                    potential += 1
                                else:
                                    return (3, (x + 1, y + 1))  ### need to be improved'''
                        else:
                            value = 2
                            forward = DP[x - 1][y-1].num
                            if x - 1 - forward >= 0 and y-1-forward >=0 and self.board[x - 1 - forward][y - 1 - forward] == ' ':
                                value += 0.5
                            if x + 4 - forward < 15 and y + 4 - forward < 15 and self.board[x + 4 - forward][y + 4 - forward] == ' ':
                                value += 0.5
                            if value != 2:
                                moves.append((value, [(x, y)]))
                            '''if (x + 1 < 15 and y + 1 < 15 and self.board[x + 1][y + 1] == ' ') and (
                                    y - 4 >= 0 and x - 4 >= 0 and self.board[x - 4][y - 4] == ' '):
                                if predict:
                                    potential += 1
                                else:
                                    return (3, DP[x][y].breakPoint)'''

                #################################### find live 2 #######################################################
                final = has(DP, 2)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        value = 1
                        if not selfbreak:
                            validPosition = []
                            if x + 1 < 15 and y+1<15 and self.board[x + 1][y+1] == ' ':
                                value += 0.5
                                validPosition.append((x + 1, y+1))
                            if x - 2 >= 0 and y-2>=0 and self.board[x - 2][y-2] == ' ':
                                value += 0.5
                                validPosition.append((x - 2, y-2))
                            if value != 1:
                                moves.append((value, validPosition))
                        else:
                            if x + 2 < 15 and y+2<15 and self.board[x + 2][y+2] == ' ':
                                value += 0.5
                            if x - 2 >= 0 and y-2>=0 and self.board[x - 2][y-2] == ' ':
                                value += 0.5
                            if value != 1:
                                moves.append((value, [(x, y)]))
                print("     moves for \: ", moves)
                return None if moves == [] else moves


            def check_a2(color, canvas, winCheck=False):
                '''
                check /
                '''
                ################################### constructing DP ###############################################
                DP = [[node() for _ in range(15)] for _ in range(15)]
                for x in range(1, 15):
                    for y in range(13, -1, -1):
                        if self.board[x][y] == color:
                            DP[x][y].p(DP[x - 1][y + 1])
                            if DP[x][y].broken:
                                a, b = DP[x][y].breakPoint
                                DP[a][b].num += 1
                            if DP[x][y].num == 5 and DP[x][y].broken == False:
                                self.run = False
                                if color == 'W':
                                    self.new = messagebox.askquestion('Sorry',
                                                                      'Computer won the game, do you want to start a new game?')
                                elif color == 'B':
                                    self.new = messagebox.askquestion('Congratulation',
                                                                      'You won the game, do you want to start a new game?')
                        if x - 2 >= 0 and y + 2 < 15 and self.board[x][y] == color and self.board[x - 1][
                            y + 1] == ' '  and DP[x - 2][y + 2].num != 0:
                            DP[x][y].p(DP[x - 1][y+1])
                            DP[x][y].breakPoint = (x - 1, y+1)
                            DP[x][y].broken = True
                            DP[x - 1][y+1].newBreak(DP[x - 2][y+2].num + 1, (x - 1, y+1))
                            '''DP[x][y].p(DP[x - 2][y + 2])
                            DP[x][y].breakPoint = (x - 1, y + 1)
                            DP[x][y].broken = True'''

                if winCheck:
                    return
                ######################################### find 4 ######################################################
                final = has(DP, 4)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        if not selfbreak:
                            if x + 1 < 15 and y - 1 >= 0 and self.board[x + 1][y - 1] == ' ':
                                return [(25, (x + 1, y - 1))]    ### 4 has value of 25, win instantly
                            if x - 4 >= 0 and y + 4 <= 14 and self.board[x - 4][y + 4] == ' ':
                                return [(25, (x - 4, y + 4))]   ### 4 has value of 25, win instantly
                        else:
                            return [(25, DP[x][y].breakPoint)]  ### 4 has value of 25, win instantly

                ################################### find live 3 #######################################################
                moves=[]
                final = has(DP, 3)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        if not selfbreak:
                            validPosition = []
                            value = 2
                            if x + 1 < 15 and y-1>=0 and self.board[x + 1][y-1] == ' ':
                                value += 0.5
                                validPosition.append((x + 1,y-1))
                            if x - 3 >= 0 and y+3<15 and self.board[x - 3][y+3] == ' ':
                                value += 0.5
                                validPosition.append((x - 3,y+3))
                            if value != 2:
                                moves.append((value, validPosition))
                            '''if (x + 1 < 15 and y - 1 < 15 and self.board[x + 1][y - 1] == ' ') and (
                                    x - 3 >= 0 and y + 3 <= 14 and self.board[x - 3][y + 3] == ' '):
                                if predict:
                                    potential += 1
                                else:
                                    return (3, (x + 1, y - 1))  ### need to be improved'''
                        else:
                            value = 2
                            forward = DP[x - 1][y+1].num
                            if x - 1 - forward >= 0 and y+1+forward<15 and self.board[x - 1 - forward][y+1+forward] == ' ':
                                value += 0.5
                            if x + 4 - forward < 15 and y-1-forward>=0 and self.board[x + 4 - forward][y-1-forward] == ' ':
                                value += 0.5
                            if value != 2:
                                moves.append((value, [(x, y)]))
                            '''if (x + 1 < 15 and y + 1 < 15 and self.board[x + 1][y - 1] == ' ') and (
                                    x - 4 >= 0 and y + 4 <= 14 and self.board[x - 4][y + 4] == ' '):
                                if predict:
                                    potential += 1
                                else:
                                    return (3, DP[x][y].breakPoint)'''

                ################################ find live 2 ##################################################
                final = has(DP, 2)
                if final != -1:
                    for (x, y, selfbreak) in final:
                        value = 1
                        if not selfbreak:
                            validPosition = []
                            if x + 1 < 15 and y-1>=0 and self.board[x + 1][y-1] == ' ':
                                value += 0.5
                                validPosition.append((x + 1, y-1))
                            if x - 2 >= 0 and y+2<15 and self.board[x - 2][y+2] == ' ':
                                value += 0.5
                                validPosition.append((x - 2, y+2))
                            if value != 1:
                                moves.append((value, validPosition))
                        else:
                            if x + 2 < 15 and y-2>=0 and self.board[x + 2][y-2] == ' ':
                                value += 0.5
                            if x - 2 >= 0 and y+2<15 and self.board[x - 2][y+2] == ' ':
                                value += 0.5
                            if value != 1:
                                moves.append((value, [(x, y)]))
                print("     moves for /: ", moves)
                return None if moves == [] else moves


            ### pick the worst
            a = check_a1(color, canvas, winCheck)
            b = check_a2(color, canvas, winCheck)
            if winCheck:
                return
            if a and a[0][0]==25:
                return a
            if b and b[0][0]==25:
                return b
            if a is None and b is None:
                return
            if a is None:
                return b
            if b is None:
                return a
            else:
                return a+b

                '''if a[0] != 2 or b[0] != 2:
                    if b[0] > a[0]:
                        return b
                    return a
                else:
                    if a[0] == 2 and b[0] == 2:
                        return (2, a[1] + b[1])
                    elif a[0] == 2:
                        return a
                    else:
                        return b'''


        ### pick the best move (largest value)
        V = check_v(color, canvas, winCheck)
        H = check_h(color, canvas, winCheck)
        A = check_a(color, canvas, winCheck)
        if winCheck:
            return
        print(V,H,A)
        if V and V[0][0] == 25:
            return V[0]
        if H and H[0][0] == 25:
            return H[0]
        if A and A[0][0] == 25:
            return A[0]

        allmoves = []
        if V:
            allmoves += V
        if H:
            allmoves += H
        if A:
            allmoves += A

        if allmoves==[]:
            return
        ### find repeated position
        allpos, repeat = [], []
        for value, poslist in allmoves:
            for pos in poslist:
                if pos in allpos:
                    repeat.append(pos)
                else:
                    allpos.append(pos)
        ### calc the value for all repeated position
        ### 2sided 3 has finalvalue 10.5
        ### 1sided 3 has finalvalue 3.5
        ### 2sided 2 has finalvalue 5
        ### 1sided 2 has finalvalue 1
        ######find the max value for not repeated pos
        finalvaluelistallpos = []
        for pos in allpos:
            Found = False
            for value, poslist in allmoves:
                if Found: break
                for comppos in poslist:
                    if comppos == pos:
                        Found = True
                        if value == 3:
                            return (10.5,pos)
                        if value == 2:
                            finalvaluelistallpos.append(5)
                        elif value==2.5:
                            finalvaluelistallpos.append(3.5)
                        else:
                            finalvaluelistallpos.append(1)
                        break
        finalvalueallpos=max(finalvaluelistallpos)
        finalmoveallpos = allpos[finalvaluelistallpos.index(finalvalueallpos)]  ### choose the move with most finalvalue
        if repeat==[]:
            return (finalvalueallpos,finalmoveallpos)
        ### find max value for repeated pos
        finalvaluelistrep=[]
        for pos in repeat:
            tempFinalValue = 0
            for value, poslist in allmoves:
                for comppos in poslist:
                    if comppos == pos:
                        if value == 3:
                            tempFinalValue += 10.5
                        if value == 2:
                            tempFinalValue += 5
                        if value == 2.5:
                            tempFinalValue += 3.5
                        if value == 1.5:
                            tempFinalValue += 1

            finalvaluelistrep.append(tempFinalValue)
        finalvaluerep = max(finalvaluelistrep)
        finalmoverep = repeat[finalvaluelistrep.index(finalvaluerep)]  ### choose the move with most finalvalue

        return (finalvaluerep,finalmoverep) if finalvaluelistrep>=finalvaluelistallpos else (finalvalueallpos,finalmoveallpos)
        '''worse = max(V[0], H[0], A[0])
           if worse != 2:
               if worse == V[0]:
                   worse = V
               elif worse == H[0]:
                   worse = H
               else:
                   worse = A
           elif worse == 2:
               potential = [V[1], H[1], A[1]]
                if V[0] == -1:
                   potential.remove((0, 0))
               if H[0] == -1:
                   potential.remove((0, 0))
               if A[0] == -1:
                   potential.remove((0, 0))
               if potential == []:
                   return (-1, (0, 0))
               return (2, potential)
       else:
           ### return true if this position need to be defenced
           return True if (V + H + A) > 1 else False'''

    def computercheck(self, canvas):
        ###check if computer won
        self.check(self.player, canvas, winCheck=True)
        self.check(self.computer, canvas, winCheck=True)

    def computerTurn(self, canvas):
        print("############################################### Step: ",self.steps," #############################################")
        def attackmove(attack):
            print('strategy: attacked,value=', attack[0])
            self.place(self.computer, attack[1][0], attack[1][1])  ##formate

        def defencemove(defence):
            print('strategy: defenced,value=', defence[0])
            self.place(self.computer, defence[1][0], defence[1][1])  ##formate

        def center():
            ###place closest to center, lol
            center = (12, (0, 0))
            for x, line in enumerate(self.board):
                if ' ' not in line:
                    continue
                for y, place in enumerate(line):
                    if place == ' ':
                        distance = ((x - 7) ** 2 + (y - 7) ** 2) ** 0.5
                        if distance < center[0]:
                            center = (distance, (x, y))
            print("centered, lol")
            self.place(self.computer, center[1][0], center[1][1])  ##formate
        print('defence mvoe: ')
        defence = self.check(self.player, canvas)
        print('defence', defence)
        print("attack move: ")
        attack = self.check(self.computer, canvas)
        print('attack', attack)
        ### single sided 4
        if defence is None and attack is None:
            center()
            return
        if defence is None:
            attackmove(attack)
            return
        if attack is None:
            defencemove(defence)
            return
        if attack[0]==25:
            attackmove(attack)
            return
        if defence[0]==25:
            defencemove(defence)
            return
        ### if computer has 2 sided 3 or 1 side 3, attack
        if attack[0] >10 or attack[0] in (8.5, 7, 4.5, 3.5):
            attackmove(attack)
            return
        ### if computer has 1or2 sided 2, and player does not has 1or2 sided 3 then attack
        if attack[0] in (10,6,5):
            if defence[0] in (21, 14.5, 13, 11.5, 10.5, 8.5, 7, 4.5, 3.5):
                defencemove(defence)
                return
            attackmove(attack)
            return
        ### if computer only has 1sided2 and player
        if attack[0]==1 and defence[0]>1:
            defencemove(defence)
            return
        ### all other situation, player nearest center
        center()

    '''
       if attack[0] >= defence[0] and attack[0] > 2:
           print('strategy: attacked,value=', attack[0])
           self.place(self.computer, attack[1][0], attack[1][1])  ##formate
     elif defence[0] > attack[0] and defence > 2:
           print('strategy: defenced,value=', defence[0])
           self.place(self.computer, defence[1][0], defence[1][1])  ##formate
       elif defence[0] == 2:
           for (x, y) in defence[1]:
               self.place(self.player, x, y)
               defence = self.check(self.player, canvas, predict=1)
               if not defence:
                    self.remove(x, y)
               else:
                   self.remove(x, y)
                   self.place(self.computer, x, y)  ##formate
                   return
       # elif defence!=(-1,(0,0)):
       # print('defenced')
       # self.place(self.computer,defence[1][0],defence[1][1])##formate

        #        if defence!=(-1,(0,0)):
        #            self.place(self.computer,defence[1][0],defence[1][1])##formate
        #        elif attack!=(-1,(0,0)):
        #            self.place(self.computer,attack[1][0],attack[1][1])##formate
       else:
           ###place closest to center, lol
           center = (12, (0, 0))
           for x, line in enumerate(self.board):
               if ' ' not in line:
                   continue
               for y, place in enumerate(line):
                   if place == ' ':
                       distance = ((x - 7) ** 2 + (y - 7) ** 2) ** 0.5
                       if distance < center[0]:
                           center = (distance, (x, y))
           self.place(self.computer, center[1][0], center[1][1])  ##formate
'''

    def playerTurn(self, x, y, canvas):
        '''
        player turn and promotion
        '''
        '''
               while 1:
                   pos=input('plese enter the position as row and col number e.g. 3 2').split(' ')
                   try:
                       x,y=int(pos[0]),int(pos[1])
                       if 15>i>=0 and 15>y>=0 and self.board[x][y]==' ':
                           self.place(self.player,x,y)
                           break
                       else:
                           print('please enter an valid pos')
                   except:
                       continue
        '''
        if 15 > x >= 0 and 15 > y >= 0 and self.board[x][y] == ' ' and self.run:
            self.place(self.player, x, y)
            return True

    def __str__(self):
        output = '  ' + ' --' * 15 + '\n'
        for x in range(15):
            output += str(x)
            if x < 10:
                output += ' '
            for y in range(15):
                output += '|'
                if self.board[x][y] == 'W':
                    output += '##'
                elif self.board[x][y] == 'B':
                    output += '**'
                elif self.board[x][y] == ' ':
                    output += '  '
            output += '|\n  '
            output += ' --' * 15 + '\n'
        output += '  '
        for x in range(15):
            output += ' ' + str(i)
            if x < 10:
                output += ' '
        return output
    def update(self,root):
        geo = root.geometry()
        geo=geo.split('+')[0]
        geo=geo.split('x')
        wx=min(map(int,geo))
        rectSize=zeroPoint=wx/17
        tzeroPoint=zeroPoint*0.7
        ovalSize=rectSize*0.3
        self.rectSize, self.zeroPoint, self.ovalSize, self.tzeroPoint=rectSize, zeroPoint, ovalSize, tzeroPoint

    def display(self,canvas):
        # canvas.create_oval(self._x-Ball.radius, self._y-Ball.radius,
        #                   self._x+Ball.radius, self._y+Ball.radius,
        #                   fill=self._color)
        
        rectSize, zeroPoint, ovalSize, tzeroPoint= self.rectSize, self.zeroPoint, self.ovalSize, self.tzeroPoint
        # canvas.create_text(zeroPoint+200,10,fill="darkblue",font="Times 20 italic bold",
        #                text="1 2 3 4 5 6 7 8 9 10 11 12 13 14")
        ##write number and rectangle on edges
        canvas.create_text(tzeroPoint, tzeroPoint, fill="darkblue", font="Times 10 italic bold", text='0')
        for x in range(1, 15):
            canvas.create_text(tzeroPoint + x * rectSize, tzeroPoint, fill="darkblue", font="Times 10 italic bold", text=str(x))
        for x in range(14):
            canvas.create_text(tzeroPoint, zeroPoint + (x + 1) * rectSize, fill="darkblue",
                               font="Times 10 italic bold", text=str(x + 1))
            for y in range(14):
                canvas.create_rectangle(zeroPoint + x * rectSize, zeroPoint + y * rectSize,
                                        zeroPoint + (x + 1) * rectSize, zeroPoint + (y + 1) * rectSize, width=2,
                                        fill='#707070')
        ##draw circles
        for x in range(15):
            for y in range(15):
                if self.board[x][y] == 'W':
                    canvas.create_oval(zeroPoint + x * rectSize - ovalSize, zeroPoint + y * rectSize - ovalSize,
                                       zeroPoint + x * rectSize + ovalSize, zeroPoint + y * rectSize + ovalSize,
                                       width=1, fill='white')
                if self.board[x][y] == 'B':
                    canvas.create_oval(zeroPoint + x * rectSize - ovalSize, zeroPoint + y * rectSize - ovalSize,
                                       zeroPoint + x * rectSize + ovalSize, zeroPoint + y * rectSize + ovalSize,
                                       width=0, fill='black')
