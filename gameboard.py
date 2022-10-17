import tkinter as tk
import select
import time
class BoardClass:
    def __init__(self, name1, name2, label, connectionSocket):
        self.program = tk.Tk()
        self.user_name = name1
        self.last_user_name = name2
        self.program.title(self.user_name+"'s game")
        self.label = label
        self.play_numbers = 0
        self.win_numbers = 0
        self.tie_numbers = 0
        self.loss_numbers = 0
        self.app_button = {}
        self.board_size = 3

        # interface
        self.boards = {}
        for row in range(self.board_size):
            # reset to ''
            for col in range(self.board_size):
                self.boards[(row, col)] = ''
                # 定义9个button
                def function(x = row, y = col): return self.click(x, y)
                button = tk.Button(self.program, width = 16, height = 6, command = function)
                self.app_button[(row, col)] = button
                button.grid(row = row, column = col)
        self.label_name = tk.Label(self.program, text = 'Input your name: ')
        self.label_name.grid(row = self.board_size + 1 , column = 0)
        self.input_name = tk.Entry(self.program, text = '', width = 16)
        self.input_name.grid(row = self.board_size + 1, column = 1)
        self.input_name_button = tk.Button(self.program, text = 'Confirm', command = self.input_name_command)
        self.input_name_button.grid(row = self.board_size + 1, column = 2)
        self.str1 = tk.StringVar('')
        self.reset_label = tk.Label(self.program, textvariable = self.str1)
        self.yes_button = tk.Button(self.program, text = 'Yes', command = self.start_new)
        self.no_button = tk.Button(self.program, text = 'No', command = self.quit)
        self.reset_label.grid(row = self.board_size + 2, column = 0)
        self.yes_button.grid(row = self.board_size + 2, column = 1)
        self.no_button.grid(row = self.board_size + 2, column = 2)
        self.quit_button = tk.Button(self.program, text ='QUIT', command = self.quit)
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.program, textvariable = self.status_var)
        self.turn_var = tk.StringVar()
        self.turn_label = tk.Label(self.program, textvariable = self.turn_var)
        self.turn_label.grid(row=self.board_size + 3, column=1)
        self.status_label.grid(row = self.board_size + 4, column = 1)
        self.quit_button.grid(row = self.board_size + 10, column = 1)

        self.resetGameBoard()
        self.connectionSocket = connectionSocket
        self.receive()

    def updateGamesPlayed(self):
        self.status_var.set(self.printStatus())

    def input_name_command(self):
        # 更新姓名
        name = self.input_name.get()
        if name:
            self.user_name = name
            self.connectionSocket.send(('name,'+self.user_name).encode())
        self.updateGameBoard()

    def resetGameBoard(self):
        # 重置界面和变量
        self.status = ''
        self.move_flag = False
        self.otherLabel = 'X'
        if self.label == 'X':
            # 第一个player先走
            self.move_flag = True
            self.otherLabel = 'O'
        if self.move_flag:
            self.turn_var.set("Your turn.")
        else:
            self.turn_var.set("Another player turn.")
        self.end_flag = False
        self.str1.set("Game on")
        self.yes_button['state'] = 'disabled'
        self.no_button['state'] = 'disabled'
        for row in range(self.board_size):
            # reset to ''
            for col in range(self.board_size):
                self.boards[(row, col)] = ''
        if self.label == 'X':
            # 第一个player先走
            self.move_flag = True
            self.otherLabel = 'O'
        self.updateGameBoard()
        
    def quit(self):
        self.connectionSocket.send('quit.'.encode())
        time.sleep(0.5)
        print(self.printStatus())
        exit()
    
    def start_new(self):
        self.resetGameBoard()
        self.connectionSocket.send('reset.'.encode())

    def click(self, x, y):
        # button点击后进行处理
        if self.boards[(x, y)] == '':
            self.boards[(x, y)] = self.label
        self.move_flag = False
        self.end_flag = self.isEnd()
        self.updateGameBoard()
        string = 'move,' + str(x) + ',' + str(y)
        self.connectionSocket.send(string.encode())
    
    def receive(self):
        # 设置超时
        ready = select.select([self.connectionSocket], [], [], 0.01)
        if ready[0]:
            serverData = self.connectionSocket.recv(1024)
            serverData = serverData.decode('ascii')
            self.parser_receive(serverData)
        # 每隔100ms接收信息
        self.program.after(50, self.receive)

    def parser_receive(self, receive):
        if receive == "":
            return
        if receive.startswith('name'):
            self.last_user_name = receive.split(',')[1]
        elif receive.startswith('move'):
            receive = receive.split(',')
            self.move_flag = True
            self.boards[(int(receive[1]), int(receive[2]))] = self.otherLabel
            self.end_flag = self.isEnd()
        elif receive.startswith('quit'):
            print(self.printStatus())
            exit()
        elif receive.startswith('reset'):
            self.resetGameBoard()
        self.updateGameBoard()

    def updateGameBoard(self):
        # 更新button
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.app_button[(row, col)]['text'] = self.boards[(row, col)]
                if self.boards[(row, col)] != '' or self.move_flag == False or self.end_flag:
                    self.app_button[(row, col)]['state'] = 'disabled'
                else:
                    self.app_button[(row, col)]['state'] = 'normal'
        self.str1.set("Game on")
        self.yes_button['state'] = 'disabled'
        self.no_button['state'] = 'disabled'
        if self.end_flag:
            self.str1.set(self.status + 'Try Again?')
            self.yes_button['state'] = 'normal'
            self.no_button['state'] = 'normal'
            self.play_numbers += 1
            self.turn_var.set("Game Over")
        else: 
            if self.move_flag:
                self.turn_var.set("Your turn.")
            else:
                self.turn_var.set("Another player turn.")
        self.updateGamesPlayed()

    def isWinner(self, label):
        # 判断对角线是否连起来
        rows = []
        cols = []
        win_flag = False
        for row in range(self.board_size):
            # 正对角
            if self.boards[(row, row)] == label:
                rows.append(1)
            # 斜对角
            if self.boards[row,self.board_size-1-row] == label:
                cols.append(1)
        if len(rows) == self.board_size or len(cols) == self.board_size:
            win_flag = True
        # 判断某行或者某列是否连起来
        for row in range(self.board_size):
            cols = []
            rows = []
            for col in range(self.board_size):
                if self.boards[(row, col)] == label:
                    cols.append(1)
                if self.boards[(col, row)] == label:
                    rows.append(1)
            if len(rows) == self.board_size or len(cols) == self.board_size:
                win_flag = True
        return win_flag

    def boardIsFull(self):
        # 判断是否游戏结束
        for (i, j) in self.boards:
            if self.boards[(i, j)] == '':
                return False
        self.tie_numbers += 1
        return True

    def isEnd(self):
        if self.isWinner(self.label):
            self.status = 'You Win.'
            self.win_numbers += 1
            return True
        if self.isWinner(self.otherLabel):
            self.status = 'You Lose.'
            self.loss_numbers += 1
            return True
        if self.boardIsFull():
            self.status = 'Game Tie.'
            return True
        return False
            

    def printStatus(self):
        string = "All Status:\n"
        string += "User name: " + self.user_name + "\n"
        string += "Last user: " + self.last_user_name + "\n"
        string += "Number of games: " + str(self.play_numbers) + "\n"
        string += "Number of wins: " + str(self.win_numbers) + "\n"
        string += "Number of loss: " + str(self.loss_numbers) + "\n"
        string += "Number of tie: " + str(self.tie_numbers)
        return string

