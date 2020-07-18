from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

def testGame():
    import os
    os.system('python3 -m unittest -v test_chess.TestCoreReqs')
    os.system('python3 -m unittest -v test_chess.TestBonusReqs')
testGame()

print(
    "\033[2;37;44m               ##               "
    "\n        Proudly created by:     "
    "\n            ZhengNan            "
    "\n              Vina              "
    "\n              SiYi              "
    "\n             Bryan              "
    "\n             David              "
)
game = Board()
game.start()

while game.winner is None:
    game.display()
    start, end = game.prompt()
    game.update(start, end)
    game.next_turn()
print(f"Game over. {game.winner} player wins!")
