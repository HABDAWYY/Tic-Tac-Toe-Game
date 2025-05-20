import tkinter as tk
import math
Player = 'X'
AI = 'O'
class TicTacToe:
    def __init__(self,root):
        self.root = root
        self.root.title("Tic Tac Toe By Ahmed Maher")
        self.root.configure(bg='#121212')
        self.Board = [[' ' for _ in range(3)]for _ in range(3)]
        self.Buttons = [[None]*3 for _ in range(3)]
        self.MainLabel = tk.Label(self.root, text="Your Turn", font=('Courier New',18), bg='#121212',fg='#e0e0e0')
        self.MainLabel.grid(row=0, column=0, columnspan=3, pady=10)
        self.PlayBoard()
        self.Restart_Button()

    def PlayBoard(self):
        for i in range(3):
            for j in range (3):
                Button = tk.Button(self.root, text=' ', font=('Courier New',40), bg='#444444', fg='#e0e0e0', width = 5, height = 2, command= lambda r=i, c=j: self.HumanMove(r,c))
                Button.grid(row = i + 1, column=j)
                self.Buttons[i][j] = Button

    def Restart_Button(self):
        RestartButton = tk.Button(self.root, text="Restart!", font=('Courier New', 14), bg='#121212', fg='#e0e0e0', command = self.ResetGame)
        RestartButton.grid(row=4, column=0, columnspan=3, sticky='N'+'S'+'E'+'W', pady=2)

    def HumanMove(self, row, col):
        if self.Board[row][col] == ' ':
            self.MainLabel.config(text="Your Turn...")
            self.MakeMove(row, col, Player)
            Score, WinCells = self.evaluate(self.Board)
            if Score == -1:
                self.HighlightWinner(WinCells)
                self.EndGame("Congratulations, You Win!")
            elif not self.MovesLeft():
                self.EndGame("It's a draw!")
            else:
                self.MainLabel.config(text="AI is thinking...")
                self.root.after(500, self.AiMove)

    def AiMove(self):
        row, col = self.BestMove()
        self.MakeMove(row, col, AI)
        Score, WinCells = self.evaluate(self.Board)
        if Score == 1:
            self.HighlightWinner(WinCells)
            self.EndGame("AI Wins!")
        elif not self.MovesLeft():
            self.EndGame("It's a draw!")
        else:
            self.MainLabel.config(text="Your Turn!")
            
    def MakeMove(self, row, col, Player):
        self.Board[row][col] = Player
        self.Buttons[row][col].config(text=Player, state='disabled')

    def MovesLeft(self):
        return any(cell == ' ' for row in self.Board for cell in row)

    def evaluate(self, Board):
        for i in range(3):
            if Board[i][0] == Board[i][1] == Board[i][2] != ' ':
                return (1 if Board[i][0] == AI else -1), [(i, 0), (i, 1), (i, 2)]
        for j in range(3):
            if Board[0][j] == Board[1][j] == Board[2][j] != ' ':
                return (1 if Board[0][j] == AI else -1), [(0, j), (1, j), (2, j)]
        if Board[0][0] == Board[1][1] == Board[2][2] != ' ':
            return (1 if Board[0][0] == AI else -1), [(0, 0), (1, 1), (2, 2)]
        if Board[0][2] == Board[1][1] == Board[2][0] != ' ':
            return (1 if Board[0][2] == AI else -1), [(0, 2), (1, 1), (2, 0)]
        return 0, []

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        score, _ = self.evaluate(board)
        if score != 0 or not self.MovesLeft():
            return score

        if is_maximizing:
            best = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = AI
                        val = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ' '
                        best = max(best, val)
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            return best
            return best
        else:
            best = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = Player
                        val = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ' '
                        best = min(best, val)
                        beta = min(beta, best)
                        if beta <= alpha:
                            return best
            return best

    def BestMove(self):
        BestVal = -math.inf
        BestMove = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.Board[i][j] == ' ':
                    self.Board[i][j] = AI
                    MoveVal = self.minimax(self.Board, 0, False, -math.inf, math.inf)
                    self.Board[i][j] = ' '
                    if MoveVal > BestVal:
                        BestVal = MoveVal
                        BestMove = (i, j)
        return BestMove



    def EndGame(self, result):
        self.MainLabel.config(text=result)
        self.DisableButtons()

    def DisableButtons(self):
        for i in range(3):
            for j in range(3):
                self.Buttons[i][j].config(state='disabled')

    def HighlightWinner(self, cells):
        for r,c in cells:
            self.Buttons[r][c].config(bg='lightgreen')

    def ResetGame(self):
        self.Board = [[' ' for _ in range(3)] for _ in range(3)]
        self.MainLabel.config(text="Your Turn")
        for i in range(3):
            for j in range(3):
                self.Buttons[i][j].config(text=' ', state='normal', bg= '#444444')
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
