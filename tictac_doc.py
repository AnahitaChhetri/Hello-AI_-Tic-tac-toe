"""
🎮 Tic Tac Toe Game — with line-by-line documentation
🧠 Author: [Your Name]
📚 Description:
    This program creates a Tic Tac Toe game using Tkinter (Python’s built-in GUI library).
    The player chooses X or O, and plays against a simple AI that can try to win or block.
"""

# --- Import required libraries ---

import tkinter as tk                             # Tkinter handles the GUI (buttons, window, etc.)
from tkinter import messagebox, simpledialog     # For popup dialogs and input boxes
import random                                    # Used to let the AI make random moves


# --- Global variables (used throughout the program) ---

board = [''] * 9        # Represents the 9 squares on the Tic Tac Toe board
buttons = []            # Will hold the 9 Tkinter Button widgets
player_symbol = ''      # The symbol the player chooses (X or O)
ai_symbol = ''          # The symbol assigned to the AI (the opposite of the player)


# --- Function: ask the player to choose X or O ---

def choose_symbol():
    """
    Asks the user whether they want to play as 'X' or 'O'.
    Then assigns the AI the opposite symbol.
    If the AI is X, it will make the first move automatically.
    """
    global player_symbol, ai_symbol

    while True:
        # Show an input box asking for X or O, and convert the answer to uppercase
        choice = simpledialog.askstring("Choose Symbol", "Do you want to be X or O?").upper()

        # If valid, assign symbols and stop asking
        if choice in ['X', 'O']:
            player_symbol = choice
            ai_symbol = 'O' if player_symbol == 'X' else 'X'
            break
        else:
            # If invalid, show an error popup
            messagebox.showerror("Invalid Choice", "Please choose X or O.")

    # If AI is X, it goes first — schedule AI move after a short delay
    if ai_symbol == 'X':
        root.after(300, make_ai_move)


# --- Function: check if a symbol has won the game ---

def check_win(symbol):
    """
    Returns True if the given symbol (X or O) has any of the 8 winning combinations.
    """
    wins = [
        (0,1,2), (3,4,5), (6,7,8),   # Rows
        (0,3,6), (1,4,7), (2,5,8),   # Columns
        (0,4,8), (2,4,6)             # Diagonals
    ]
    return any(board[a]==board[b]==board[c]==symbol for a,b,c in wins)


# --- Function: check if the board is full (tie) ---

def is_full():
    """Returns True if all 9 board spaces are filled."""
    return all(cell != '' for cell in board)


# --- Function: AI’s move logic ---

def make_ai_move():
    """
    The AI will:
      1. Try to win if possible
      2. Try to block the player's win
      3. Otherwise, pick a random empty space
    """
    # 1️⃣ Try to win
    for i in range(9):
        if board[i] == '':
            copy = board[:]                # Make a copy of the board
            copy[i] = ai_symbol            # Pretend to place AI’s symbol
            if check_win_on_board(copy, ai_symbol):
                update_cell(i, ai_symbol, "blue")
                return

    # 2️⃣ Try to block player’s win
    for i in range(9):
        if board[i] == '':
            copy = board[:]
            copy[i] = player_symbol
            if check_win_on_board(copy, player_symbol):
                update_cell(i, ai_symbol, "blue")
                return

    # 3️⃣ If no immediate win or block, pick a random spot
    move = random.choice([i for i in range(9) if board[i] == ''])
    update_cell(move, ai_symbol, "blue")


# --- Helper function: check for a win on a given board copy (used by AI) ---

def check_win_on_board(brd, symbol):
    """Checks if 'symbol' wins on a temporary board (used for AI testing moves)."""
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    return any(brd[a]==brd[b]==brd[c]==symbol for a,b,c in wins)


# --- Function: what happens when a player clicks a square ---

def on_click(index):
    """
    Called when the player clicks one of the 9 squares.
    If the square is empty and the game is not over,
    it fills it with the player's symbol, then lets the AI move.
    """
    if board[index] == '' and not game_over():
        update_cell(index, player_symbol, "red")
        if not game_over():  # Only let AI move if game not finished
            root.after(5000, make_ai_move)  # Wait 0.3 sec for effect


# --- Function: update the game board (and check for results) ---

def update_cell(index, symbol, color):
    """
    Updates one cell of the game board:
      - Changes the board list
      - Updates the button text/color
      - Checks for win or tie
    """
    board[index] = symbol
    buttons[index].config(text=symbol, fg=color)

    # Check if someone won
    if check_win(symbol):
        messagebox.showinfo("Game Over", f"{'You' if symbol == player_symbol else 'AI'} win!")
    elif is_full():  # Or if it’s a tie
        messagebox.showinfo("Game Over", "It's a tie!")


# --- Function: check if the game has ended ---

def game_over():
    """Returns True if the game has been won or tied."""
    return check_win(player_symbol) or check_win(ai_symbol) or is_full()


# --- Function: restart the game ---

def reset_game():
    """
    Resets the entire game:
      - Clears all button text
      - Empties the board
      - Asks the player again to choose X or O
    """
    global board
    board = [''] * 9
    for btn in buttons:
        btn.config(text='', fg='black')
    choose_symbol()


# --- Tkinter window setup ---

root = tk.Tk()                    # Create the main Tkinter window object
root.title("Tic Tac Toe game")    # Set window title (appears in the title bar)


# --- Create 9 buttons for the game grid ---

for i in range(9):
    btn = tk.Button(
        root,
        text='',                   # Start empty
        font=('Arial', 40),        # Large font for X and O
        width=5, height=2,         # Button size
        command=lambda i=i: on_click(i)  # When clicked, call on_click() with index i
    )
    btn.grid(row=i//3, column=i%3)  # Arrange in 3x3 grid (row and column math)
    buttons.append(btn)             # Save each button in the list


# --- Add a Reset button below the grid ---

reset_btn = tk.Button(
    root,
    text="Reset",
    font=('Arial', 14),
    command=reset_game              # When clicked, restarts the game
)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")


# --- Start the game by asking player for symbol ---

root.after(100, choose_symbol)  # Schedule choose_symbol() after a short delay


# --- Run the main Tkinter event loop ---

root.mainloop()  # This displays the window and keeps it open, handling all events
