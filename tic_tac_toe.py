import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Global variables
board = [''] * 9
buttons = []
player_symbol = ''
ai_symbol = ''

def choose_symbol():
    global player_symbol, ai_symbol
    while True:
        choice = simpledialog.askstring("Choose Symbol", "Do you want to be X or O?").upper()
        if choice in ['X', 'O']:
            player_symbol = choice
            ai_symbol = 'O' if player_symbol == 'X' else 'X'
            break
        else:
            messagebox.showerror("Invalid Choice", "Please choose X or O.")

    # AI makes the first move if it is X
    if ai_symbol == 'X':
        root.after(300, make_ai_move)

def check_win(symbol):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(board[a]==board[b]==board[c]==symbol for a,b,c in wins)

def is_full():
    return all(cell != '' for cell in board)

def make_ai_move():
  #Try to Win
    for i in range(9):
        if board[i] == '':
            copy = board[:]
            copy[i] = ai_symbol
            if check_win_on_board(copy, ai_symbol):
                update_cell(i, ai_symbol, "blue")
                return
   #Block Player’s Win
    for i in range(9):
        if board[i] == '':
            copy = board[:]
            copy[i] = player_symbol
            if check_win_on_board(copy, player_symbol):
                update_cell(i, ai_symbol, "blue")
                return
  #otherwise
    move = random.choice([i for i in range(9) if board[i] == ''])
    update_cell(move, ai_symbol, "blue")

def check_win_on_board(brd, symbol):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(brd[a]==brd[b]==brd[c]==symbol for a,b,c in wins)

def on_click(index):
    if board[index] == '' and not game_over():
        update_cell(index, player_symbol, "red")
        if not game_over():
            root.after(300, make_ai_move)

def update_cell(index, symbol, color):
    board[index] = symbol
    buttons[index].config(text=symbol, fg=color)
    if check_win(symbol):
        messagebox.showinfo("Game Over", f"{'You' if symbol == player_symbol else 'AI'} win!")
    elif is_full():
        messagebox.showinfo("Game Over", "It's a tie!")

def game_over():
    return check_win(player_symbol) or check_win(ai_symbol) or is_full()

def reset_game():
    global board
    board = [''] * 9
    for btn in buttons:
        btn.config(text='', fg='black')
    choose_symbol()

# Setup UI
root = tk.Tk()
root.title("Tic Tac Toe game")

for i in range(9):
    btn = tk.Button(root, text='', font=('Arial', 40), width=5, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

reset_btn = tk.Button(root, text="Reset", font=('Arial', 14), command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Start game with symbol selection
root.after(100, choose_symbol)
root.mainloop()
