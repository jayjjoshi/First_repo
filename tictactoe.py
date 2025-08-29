"""Tic-Tac-Toe game with an unbeatable AI using the minimax algorithm.

This module can be used either interactively by a human player or in a
"demo" mode where two AI players compete against each other.
The implementation showcases object‑oriented design, recursion, and search
algorithms in Python.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple
import argparse
import math
import random

Player = str  # either "X" or "O"

@dataclass
class GameState:
    board: List[Optional[Player]]
    current: Player

    def available_moves(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot is None]

    def winner(self) -> Optional[Player]:
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6),             # diagonals
        ]
        for a, b, c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if all(self.board):
            return "T"  # tie
        return None

    def make_move(self, idx: int) -> 'GameState':
        new_board = self.board.copy()
        new_board[idx] = self.current
        next_player = "O" if self.current == "X" else "X"
        return GameState(new_board, next_player)


class MinimaxAI:
    def choose_move(self, state: GameState) -> int:
        best_score = -math.inf
        best_move = -1
        for move in state.available_moves():
            score = self._minimax(state.make_move(move), False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _minimax(self, state: GameState, maximizing: bool) -> float:
        result = state.winner()
        if result == "X":
            return 1
        if result == "O":
            return -1
        if result == "T":
            return 0

        if maximizing:
            value = -math.inf
            for move in state.available_moves():
                value = max(value, self._minimax(state.make_move(move), False))
            return value
        else:
            value = math.inf
            for move in state.available_moves():
                value = min(value, self._minimax(state.make_move(move), True))
            return value


def print_board(board: List[Optional[Player]]):
    symbols = [spot or str(i+1) for i, spot in enumerate(board)]
    for row in range(0, 9, 3):
        print(" | ".join(symbols[row:row+3]))
        if row < 6:
            print("---------")


def human_vs_ai():
    board = [None] * 9
    human = random.choice(["X", "O"])
    ai_player = MinimaxAI()
    state = GameState(board, "X")
    print(f"You are {human}. {('You go first' if human == 'X' else 'Computer goes first')}\n")
    while True:
        if state.current == human:
            print_board(state.board)
            move = int(input("Choose your move (1-9): ")) - 1
            if move not in state.available_moves():
                print("Invalid move. Try again.")
                continue
            state = state.make_move(move)
        else:
            move = ai_player.choose_move(state)
            state = state.make_move(move)
            print(f"Computer chooses {move + 1}\n")
        result = state.winner()
        if result:
            print_board(state.board)
            if result == human:
                print("You win! 🎉")
            elif result == "T":
                print("It's a tie.")
            else:
                print("Computer wins. 😞")
            break


def ai_demo():
    board = [None] * 9
    state = GameState(board, "X")
    ai = MinimaxAI()
    while True:
        move = ai.choose_move(state)
        state = state.make_move(move)
        print_board(state.board)
        result = state.winner()
        if result:
            if result == "T":
                print("Demo game ended in a tie.")
            else:
                print(f"Player {result} wins the demo game.")
            break
        print()


def main():
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe against an AI or watch a demo.")
    parser.add_argument("--demo", action="store_true", help="Run an AI vs AI demo")
    args = parser.parse_args()

    if args.demo:
        ai_demo()
    else:
        human_vs_ai()


if __name__ == "__main__":
    main()
