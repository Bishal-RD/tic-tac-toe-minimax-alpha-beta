def initialize_board():
    """Creates an empty 3x3 Tic-Tac-Toe board."""
    return [["" for _ in range(3)] for _ in range(3)]

def get_valid_moves(board):
    """Returns a list of valid moves on the board."""
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == ""]

def is_winner(board, player):
    """Checks if the given player has won."""
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != "" for row in board for cell in row) and not is_winner(board, "X") and not is_winner(board, "O")

def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    Logs each step for understanding AI decision-making.
    """
    if is_winner(board, "O"):  # AI wins
        return 10 - depth
    if is_winner(board, "X"):  # Player wins
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        print(f"AI evaluating maximizing options at depth {depth}...")
        best_score = float("-inf")
        for row, col in get_valid_moves(board):
            board[row][col] = "O"
            score = alpha_beta_pruning(board, depth + 1, alpha, beta, False)
            board[row][col] = ""  # Undo move
            print(f"AI considering move ({row}, {col}) with score {score}")
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:  # Beta cutoff
                print(f"Pruning branch at move ({row}, {col}) with alpha={alpha}, beta={beta}")
                break
        return best_score
    else:
        print(f"AI evaluating minimizing options at depth {depth}...")
        best_score = float("inf")
        for row, col in get_valid_moves(board):
            board[row][col] = "X"
            score = alpha_beta_pruning(board, depth + 1, alpha, beta, True)
            board[row][col] = ""  # Undo move
            print(f"AI considering move ({row}, {col}) with score {score}")
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:  # Alpha cutoff
                print(f"Pruning branch at move ({row}, {col}) with alpha={alpha}, beta={beta}")
                break
        return best_score
    
def find_best_move(board):
    """Finds the best move for the AI using the Minimax algorithm."""
    best_score = float("-inf")
    best_move = None
    print("\nAI is calculating the best move...")
    for row, col in get_valid_moves(board):
        board[row][col] = "O"
        score = alpha_beta_pruning(board, 0, float("-inf"), float("inf"), False)
        board[row][col] = ""  # Undo move
        print(f"Move ({row}, {col}) has a minimax score of {score}")
        if score > best_score:
            best_score = score
            best_move = (row, col)
    print(f"AI chooses move {best_move} with score {best_score}")
    return best_move

def print_board(board):
    """Prints the current state of the board."""
    print("\nCurrent Board:")
    for row in board:
        print(" | ".join(cell if cell else " " for cell in row))
        print("-" * 9)

def play_game():
    """Main function to play the game."""
    board = initialize_board()
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X' and the AI is 'O'. Make your move by entering row and column numbers (0-2).")

    while True:
        print_board(board)
        # Player's Turn
        try:
            row, col = map(int, input("Enter your move (row space column): ").split())
            if board[row][col] != "":
                print("Invalid move! Try again.")
                continue
            board[row][col] = "X"

        except (ValueError, IndexError):
            print("Invalid input! Enter row and column as two numbers between 0 and 2.")
            continue

        if is_winner(board, "X"):
            print("You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # AI's Turn
        print("AI is thinking...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = "O"
        if is_winner(board, "O"):
            print_board(board)
            print("AI wins! Better luck next time.")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
    print("Thank you for playing...")