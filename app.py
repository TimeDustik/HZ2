from flask import Flask, render_template, request

app = Flask(__name__)

# Логика игры
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_turn = 'X'
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square):
        if self.board[square] == ' ' and not self.current_winner:
            self.board[square] = self.current_turn
            if self.winner(square, self.current_turn):
                self.current_winner = self.current_turn
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

# Создание глобальной переменной для игры
game = TicTacToe()

@app.route('/')
def home():
    return render_template('index.html', game=game)

@app.route('/move', methods=['POST'])
def move():
    square = int(request.form['square'])
    if game.make_move(square):
        if game.current_winner:
            return render_template('index.html', game=game, winner=game.current_winner)
        else:
            return render_template('index.html', game=game)
    return render_template('index.html', game=game)

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = TicTacToe()
    return render_template('index.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)
