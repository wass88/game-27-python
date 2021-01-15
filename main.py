#!/usr/bin/env python3
from typing import NamedTuple
from enum import Enum
import sys

SIZE = 9
FIRST = 1
SECOND = -1

class Action(NamedTuple):
    pas: bool
    x: int
    i: int

    def __str__(self):
        if self.pas:
            return "pass"
        return "move {} {}".format(self.x, self.i)


class Game:
    def __init__(self):
        self.board = [[] for _ in range(SIZE)]
        self.board[0] = [FIRST for _ in range(SIZE)]
        self.board[SIZE-1] = [SECOND for _ in range(SIZE)]
        self.first_turn = True

    def playable(self):
        towers = self.towers()
        moves = []
        for x in range(SIZE):
            if not len(self.board[x]) > 0:
                continue
            if not self.board[x][0] == self.current_player():
                continue

            target = x + towers * self.current_player()
            if not 0 <= target < SIZE:
                continue
            for i in range(1, len(self.board[x])+1):
                moves.append(Action(False, x, i))

        if len(moves) == 0:
            moves.append(Action(True, 0, 0))
        return moves

    def act(self, action: Action):
        if action.pas:
            pass
        else:
            self.move(action.x, action.i)
        self.first_turn = not self.first_turn
    
    def move(self, x: int, i: int):
        if not 0 <= x < SIZE:
            raise ValueError("The position is out of board")
        if not len(self.board[x]) > 0:
            raise ValueError("There is no tower")
        if not self.board[x][0] == self.current_player():
            raise ValueError("The tower is not yours")
        if not i <= len(self.board[x]):
            raise ValueError("The move is too big to move")

        towers = self.towers()
        target = x + towers * self.current_player()
        if not 0 <= target < SIZE:
            raise ValueError("The move is out of board")

        self.board[target] = self.board[x][:i] + self.board[target]
        self.board[x] = self.board[x][i:]

    def current_player(self) -> int:
        return FIRST if self.first_turn else SECOND

    def towers(self) -> int:
        return sum(tower[0] == self.current_player() if len(tower) > 0 else False for tower in self.board)

    def is_end(self) -> bool:
        if self.playable()[0].pas:
            self.first_turn = not self.first_turn
            end = self.playable()[0].pas
            self.first_turn = not self.first_turn
            return end
        return False

    def __str__(self) -> str:
        output = ""
        for x in range(SIZE):
            output += "{}: ".format(x)
            for tower in self.board[x]:
                output += "O" if tower == FIRST else "X"
            if x < SIZE - 1:
                output += "\n"
        return output

class Player:
    def __init__(self):
        self.game = Game()
        self.first = True
    
    def play(self, command) -> (bool, str):
        cmd = command.split(" ")
        if cmd[0] == "init":
            order = int(cmd[1])
            self.first = order == 0
            return (False, "")
        if cmd[0] == "played":
            if cmd[1] == "move":
                action = Action(False, int(cmd[2]), int(cmd[3]))
                self.game.act(action)
                return (False, "")
            if cmd[1] == "pass":
                action = Action(False, int(cmd[2]), int(cmd[3]))
                self.game.act(action)
                return (False, "")
        if cmd[0] == "result":
            return (True, "")
        if cmd[0] == "wait":
            action = self.thinking()
            self.game.act(action)
            return (False, action.__str__())
        raise ValueError("The command is unknown: " + command)

    def thinking(self) -> Action:
        moves = self.game.playable()

        # TODO: create AI!
        move = moves[0]

        return move


def start():
    player = Player()
    while True:
        command = input()
        end, response = player.play(command)
        if response != "":
            print(response)
        if end:
            break

if __name__ == "__main__":
    start()
