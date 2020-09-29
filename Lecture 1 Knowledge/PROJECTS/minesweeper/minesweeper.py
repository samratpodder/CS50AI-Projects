import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return True
        return False

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return True
        return False


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        neighbours =set()
        i,j=cell
        for row in range(i-1,i+2):
            for col in range(j-1,j+2):
                if((row>=0 and row <self.width)and (col >=0 and col <self.width)and ((row,col)!=cell) 
                and ((row,col) not in self.moves_made)):
                    if ((row,col) in self.mines):
                        count-=1
                    if (row,col) in self.safes:
                        continue
                    else:
                        neighbours.add((row,col))
        new_sentence = Sentence(neighbours,count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
        for sentence in self.knowledge:
            known_safes = sentence.known_safes()
            for known_safe in known_safes:
                self.mark_safe(known_safe)
            known_mines = sentence.known_mines()
            for known_mine in known_mines.copy():
                self.mark_mine(known_mine)
        known_sentences = copy.deepcopy(self.knowledge)
        for sentence1 in known_sentences:
            known_sentences.remove(sentence1)
            for sentence2 in known_sentences:
                if (len(sentence1.cells)==len(sentence2.cells)):
                    continue
                elif (len(sentence1.cells)>len(sentence2.cells)):
                    subset = sentence2.cells
                    bigset = sentence1.cells
                    diff_count = sentence1.count - sentence2.count
                elif (len(sentence2.cells)>len(sentence1.cells)):
                    subset = sentence1.cells
                    bigset = sentence2.cells
                    diff_count = sentence2.count - sentence1.count
                else:
                    continue
                diff_set = bigset-subset
                copyset = diff_set.copy()
                if len(diff_set)==1:
                    if diff_count==1:
                        new_safe = copyset.pop()
                        self.mark_safe(new_safe)
                    elif diff_count == 0:
                        new_mine = copyset.pop()
                        self.mark_mine(new_mine)
                else:
                    self.knowledge.append(Sentence(diff_set,diff_count))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("------------------------------")
        for mines in self.mines:
            print("Mines:"+str(mines)+",")
        for safes in self.mines:
            print("Safes:"+str(safes)+",")
        for moves in self.moves_made:
            print("Moves Made:"+str(moves)+",")
        for safe_move in self.safes:
            if safe_move not in self.mines and safe_move not in self.moves_made:
                print("Move Now(+1,+1): "+str(safe_move))
                print("------------------------------")
                return safe_move
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move = ()
        while True:
            move = (random.randrange(0,8),random.randrange(0,8))
            if move not in self.mines and move not in self.moves_made:
                return move
