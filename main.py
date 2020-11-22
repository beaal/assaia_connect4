DECK_SIZE = (6, 7)
PLAYER_1 = '0'
PLAYER_2 = '1'

import numpy as np




class Deck():
    def __init__(self, deck_size=DECK_SIZE, player_1=PLAYER_1, player_2=PLAYER_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.rows = int(deck_size[0])
        self.columns = int(deck_size[1])
        self.deck_arr = np.array([[' '] * self.columns for i in range(self.rows)])
        self.winner_player_1 = self.player_1 * 4
        self.winner_player_2 = self.player_2 * 4

    def __str__(self):
        header = '|'.join(map(str, range(self.columns))) + '\n' + '~' * self.columns * 2 + '\n'
        s = ''
        for row in self.deck_arr:
            s += '|'.join(map(str, row))
            s += '\n'
        return header + s

    def update_deck(self, player, column):

        column_to_check = self.deck_arr[:, column]

        if self.deck_arr[self.rows - 1][column] == ' ':
            self.deck_arr[self.rows - 1][column] = player
            return True

        if ' ' in ''.join(column_to_check):
            for idx, el in enumerate(column_to_check):
                if el != ' ':
                    self.deck_arr[idx - 1][column] = player
                    return True
        else:
            return False

    def check_winner(self):
        if self._check_rows() or self._check_columns() or self._check_diagonals():
            return True

    def check_tie(self):
        if ' ' not in ''.join(str(el) for el in np.nditer(self.deck_arr)):
            return True


    def _check_diagonals(self):
        diags = [
            self.deck_arr[::-1, :].diagonal(i)
            for i in range(-self.deck_arr.shape[0] + 1, self.deck_arr.shape[1])
        ]
        diags.extend(
            self.deck_arr.diagonal(i)
            for i in range(self.deck_arr.shape[1] - 1, -self.deck_arr.shape[0], -1))

        str_diags = [''.join(el) for el in diags]
        for el in str_diags:
            if self._check_winner_in_array(el):
                return True

    def _check_winner_in_array(self, arr):
        if self.winner_player_1 in arr or self.winner_player_2 in arr:
            return True

    def _check_columns(self):
        deck_transposed = np.transpose(self.deck_arr)
        str_columns = [''.join(el) for el in deck_transposed]
        for el in str_columns:
            if self._check_winner_in_array(el):
                return True

    def _check_rows(self):
        str_rows = [''.join(el) for el in self.deck_arr]
        for el in str_rows:
            if self._check_winner_in_array(el):
                return True


if __name__ == "__main__":
    deck = Deck()
    cur_player = PLAYER_1
    print(
        'Welcome to the Connect 4 Game!\nThe rules are simple: 4 subsequent symbols in a row/column/diagonal is a win.\n'
    )
    print(deck)
    while True:
        try:
            column = int(input(f'Player *{cur_player}*, please select column: '))
        except ValueError:
            print(f'Please, input valid column number from 0 to {deck.columns-1}')
            print(deck)
            continue

        if column not in range(deck.columns):
            print(f'Please, input valid column number from 0 to {deck.columns-1}')
            print(deck)
            continue
        if deck.update_deck(cur_player, column):
            print('Succesful move!\n')
        else:
            print('Please, select proper column. Chosen column is full')
            print(deck)
            continue

        if deck.check_winner():
            print(deck)
            print(f'Player {cur_player} wins! Bye!')
            break
        
        if deck.check_tie():
            print('No more moves available. Please, restart the game.')
            break

        if cur_player == PLAYER_1:
            cur_player = PLAYER_2
        else:
            cur_player = PLAYER_1

        print(deck)
