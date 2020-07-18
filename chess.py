class Board:
    from datetime import datetime
    starttime = datetime.today()
    """
    The game board is represented as an 8×8 grid,
    with each position on the grid described as
    a pair of ints (range 0-7): col followed by row

    07  17  27  37  47  57  67  77
    06  16  26  36  46  56  66  76
    05  15  25  35  45  55  65  75
    04  14  24  34  44  54  64  74
    03  13  23  33  43  53  63  73
    02  12  22  32  42  52  62  72
    01  11  21  31  41  51  61  71
    00  10  20  30  40  50  60  70
    """

    def __init__(self, debug=False):
        self.position = {}
        self.debug = debug

    def coords(self):
        """Return list of piece coordinates."""
        return self.position.keys()

    def pieces(self):
        """Return list of board pieces."""
        return self.position.values()

    def get_piece(self, coord):
        """
        Return the piece at coord.
        Returns None if no piece at coord.
        """
        return self.position.get(coord, None)

    def add(self, coord, piece):
        """Add a piece at coord."""
        self.position[coord] = piece

    def remove(self, coord):
        """
        Remove the piece at coord, if any.
        Does nothing if there is no piece at coord.
        """
        if coord in self.coords():
            del self.position[coord]

    def move(self, start, end):
        """
        Move the piece at start to end.
        Validation should be carried out first
        to ensure the move is valid.
        """
        piece = self.get_piece(start)
        self.remove(start)
        self.add(end, piece)

    def start(self):
        """Set up the pieces and start the game."""
        colour = "black"
        self.add((0, 7), Rook(colour))
        self.add((1, 7), Knight(colour))
        self.add((2, 7), Bishop(colour))
        self.add((3, 7), Queen(colour))
        self.add((4, 7), King(colour))
        self.add((5, 7), Bishop(colour))
        self.add((6, 7), Knight(colour))
        self.add((7, 7), Rook(colour))
        for x in range(0, 8):
            self.add((x, 6), Pawn(colour))

        colour = "white"
        self.add((0, 0), Rook(colour))
        self.add((1, 0), Knight(colour))
        self.add((2, 0), Bishop(colour))
        self.add((3, 0), Queen(colour))
        self.add((4, 0), King(colour))
        self.add((5, 0), Bishop(colour))
        self.add((6, 0), Knight(colour))
        self.add((7, 0), Rook(colour))
        for x in range(0, 8):
            self.add((x, 1), Pawn(colour))

        self.winner = None
        self.turn = "white"

    def display(self):
        """
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        """
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        if self.debug == True:
            print("== DISPLAY ==")
        if self.turn == "white":
            print("\033[1;30;47m")  # black w white bg
        if self.turn == "black":
            print("\033[1;37;40m")  # white w blk bg
        print("           [ column ]          ", end="\n")
        print("        0\\1\\2\\3\\4\\5\\6\\7\\       ")
        for row in range(7, -1, -1):
            print(f" [row {row}]", end="")
            # for i in range(0,8):
            # print(i, end="")
            for col in range(8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    # not here
                    print(f"{piece.symbol()}", end="")
                else:
                    piece = None
                    print(" ", end="")
                if col == 7:  # Put line break atthe end
                    print(f" [row {row}]")
                else:  # Print a space between pieces
                    print(" ", end="")
        print("        0/1/2/3/4/5/6/7/       ")
        print("           [ column ]          ", end="\n")
        # print("\033[1;37;40m") #white w blk bg

    def prompt(self):
        """
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        """
        if self.debug == True:
            print("== PROMPT ==")

        def valid_format(inputstr):
            """
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            """
            return (
                len(inputstr) == 5
                and inputstr[2] == " "
                and inputstr[0:2].isdigit()
                and inputstr[3:5].isdigit()
            )

        def valid_num(inputstr):
            """Ensure all inputted numerals are 0-7."""
            for char in inputstr[0:2] + inputstr[3:5]:
                if char not in "01234567":
                    return False
            return True

        def split_and_convert(inputstr):
            """Convert 5-char inputstr into start and end tuples."""
            start, end = inputstr.split(" ")
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        def printmove():
            return (
                f"{str(self.get_piece(start))} {start[0]}{start[1]} -> {end[0]}{end[1]}"
            )

        while True:
            inputstr = input(f"{self.turn.title()} player: ")
            if not valid_format(inputstr):
                print(
                    "Invalid input. Please enter your move in the "
                    "following format: __ __ where '__' contains digit 0 to 7.\n"
                    "Example: [current-column][current-row] [new-column][new-row]"
                )
            elif not valid_num(inputstr):
                print("Invalid input. Move digits should be 0-7.")
            else:
                start, end = split_and_convert(inputstr)
                if self.valid_move(start, end):
                    # print(
                    #     self.get_piece(start),
                    #     f"{start[0]}{start[1]} -> {end[0]}{end[1]}",
                    # )
                    # print (start,end)
                    print(printmove())
                    endtime = self.datetime.today()
                    with open('moves.txt', 'a+') as f:
                        f.write(f'{endtime}: {self.turn} {start[0]}{start[1]} -> {end[0]}{end[1]}\n')
                    timetaken = endtime - self.starttime
                    timetaken_inseconds = timetaken.total_seconds()
                    print(f"{self.turn} player took {timetaken_inseconds}seconds to make a move.")
                    return start, end
                else:
                    print(f"Invalid move for {self.get_piece(start)}.")

    def valid_move(self, start, end):
        """
        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not valid for the selected piece
        
        Returns False otherwise
        """
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif start_piece.name == "pawn":
            if not start_piece.isvalid(start, end, end_piece):
                return False
        elif not start_piece.isvalid(start, end):
            return False
        return True

    def update(self, start, end):
        """Update board information with the player's move."""
        if self.debug == True:
            print("== UPDATE ==")
        self.remove(end)
        self.move(start, end)
        self.win()
        self.promotion()
        self.check()

    def win(self):
        if self.debug == True:
            print("== CHECKING FOR WINNER ==")
        piecelist = [str(pieces) for pieces in self.pieces()]
        if "black king" not in piecelist:
            self.winner = "White"
        if "white king" not in piecelist:
            self.winner = "black"

    def check(self):
        if self.debug == True:
            print(" == CHECKING IF KING IS CHECKED ==")
        for coord in self.coords():
            if "white king" in str(self.get_piece(coord)):
                wkingcoord = coord
            elif "black king" in str(self.get_piece(coord)):
                bkingcoord = coord
        for coord in self.coords():
            if self.valid_move(coord, wkingcoord):
                print("white is in check!")
                break
            elif self.valid_move(coord, bkingcoord):
                print("black is in check!")
                break

    def promotion(self):
        """
        Check if last row contains opposing pawn and swap to queen if true
        """
        if self.debug == True:
            print("== CHECKING FOR PROMOTION ==")
        black_last_row = [
            (0, 7),
            (1, 7),
            (2, 7),
            (3, 7),
            (4, 7),
            (5, 7),
            (6, 7),
            (7, 7),
        ]
        white_last_row = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        ]
        for coords in black_last_row:
            if str(self.get_piece(coords)) == "white pawn":
                self.remove(coords)
                self.add(coords, Queen("white"))
        for coords in white_last_row:
            if str(self.get_piece(coords)) == "black pawn":
                self.remove(coords)
                self.add(coords, Queen("black"))

    def next_turn(self):
        """Hand the turn over to the other player."""
        if self.debug == True:
            print("== NEXT TURN ==")
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"


class BasePiece:
    name = "piece"

    def __init__(self, colour):
        if type(colour) != str:
            raise TypeError("colour argument must be str")
        elif colour.lower() not in {"white", "black"}:
            raise ValueError("colour must be {white, black}")
        else:
            self.colour = colour

    def __repr__(self):
        return f"BasePiece({repr(self.colour)})"

    def __str__(self):
        return f"{self.colour} {self.name}"

    def symbol(self):
        return f"{self.sym[self.colour]}"

    @staticmethod
    def vector(start, end):
        """
        Return three values as a tuple:
        - x, the number of spaces moved horizontally,
        - y, the number of spaces moved vertically,
        - dist, the total number of spaces moved.
        
        positive integers indicate upward or rightward direction,
        negative integers indicate downward or leftward direction.
        dist is always positive.
        """
        x = end[0] - start[0]
        y = end[1] - start[1]
        dist = abs(x) + abs(y)
        return x, y, dist


class King(BasePiece):
    name = "king"
    sym = {"white": "♔", "black": "♚"}

    def __repr__(self):
        return f"King('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        """
        King can move one step in any direction
        horizontally, vertically, or diagonally.
        """
        x, y, dist = self.vector(start, end)
        return (dist == 1) or (abs(x) == abs(y) == 1)


class Queen(BasePiece):
    name = "queen"
    sym = {"white": "♕", "black": "♛"}

    def __repr__(self):
        return f"Queen('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        """
        Queen can move any number of steps horizontally,
        vertically, or diagonally.
        """
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0) or (
            (abs(x) == 0 and abs(y) != 0) or (abs(y) == 0 and abs(x) != 0)
        )


class Bishop(BasePiece):
    name = "bishop"
    sym = {"white": "♗", "black": "♝"}

    def __repr__(self):
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        """Bishop can move any number of steps diagonally."""
        x, y, dist = self.vector(start, end)
        return abs(x) == abs(y) != 0


class Knight(BasePiece):
    name = "knight"
    sym = {"white": "♘", "black": "♞"}

    def __repr__(self):
        return f"Knight('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        """
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        """
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    name = "rook"
    sym = {"white": "♖", "black": "♜"}

    def __repr__(self):
        return f"Rook('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        """
        Rook can move any number of steps horizontally
        or vertically.
        """
        x, y, dist = self.vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) or (abs(y) == 0 and abs(x) != 0)


class Pawn(BasePiece):
    name = "pawn"
    sym = {"white": "♙", "black": "♟︎"}

    def __repr__(self):
        return f"Pawn('{self.name}')"

    def isvalid(self, start: tuple, end: tuple, end_piece):
        """Pawn can only move 1 step forward."""

    def pawnfirstmove(self, start, end):
        if self.colour == "black":
            if start[1] != 6:
                return False
        if self.colour == "white":
            if start[1] != 1:
                return False
        return True

    def isvalid(self, start: tuple, end: tuple, end_piece):
        """Pawn can only move 1 step forward."""
        x, y, dist = self.vector(start, end)
        if x == 0:
            if self.colour == "black":
                if self.pawnfirstmove(start, end):
                    return (y == -1) or (y == -2)
                return y == -1
            elif self.colour == "white":
                if self.pawnfirstmove(start, end):
                    return (y == 1) or (y == 2)
                return y == 1
            else:
                return False
        elif abs(x) == 1:
            if end_piece == None:
                return False
            elif end_piece.name == "pawn":
                if self.colour == "black":
                    return y == -1
                elif self.colour == "white":
                    return y == 1
            else:
                return False
        return False
