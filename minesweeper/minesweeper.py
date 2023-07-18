import itertools
import random


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

        # Return set of mines
        if self.cells and len(self.cells) == self.count:
            return self.cells
        return None        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Return set of known safes
        if self.cells and self.count == 0:
            return self.cells      
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # Removes mine from sentence and count
        self.cells.remove(cell)
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # Removes safe cells from sentence
        if cell in self.cells:
            self.cells.remove(cell)

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
        #print("AI -> Mark_mine: ")
        self.mines.add(cell)
        #print(f"removing cell: {cell}")
        for sentence in self.knowledge:
            #print(f"sentence: {sentence.__str__()}, removing {cell}")
            if cell in sentence.cells:
                sentence.mark_mine(cell)
        #print("AI -> Mark_mine: END") 

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        #print("AI -> Mark_safe: ")
        if cell not in self.moves_made:
            self.safes.add(cell)
            for sentence in self.knowledge:
                sentence.mark_safe(cell)
        #print("AI -> Mark_safe END") 

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
        
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # Get cell and all neighbours
        cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_cell = (cell[0] + i, cell[1] + j)
                if new_cell[0] in range(8) and new_cell[1] in range(8) and new_cell not in self.moves_made:# and new_cell not in self.safes: # added self.safes
                    cells.add(new_cell)  

        # Add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        new_sentence = Sentence(cells, count)
        print(f"new sentence 1 = {new_sentence}")
        self.knowledge.append(new_sentence)
        
        # Mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        if cells:
            if len(cells) == count:
                for element in cells:
                    self.mark_mine(element)
                    
            if count == 0:
                for element in cells:
                    self.mark_safe(element)
        
        # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        new_mines = set()                  
        new_safes = set()        

# error: there is a bug -> some setneces that are subsets of others are not detected and resolved as such
        lisd1 = []
        for element in self.knowledge:
            lisd1.append(element.__str__())
        #print(f"KB pre-inferred = {lisd1}")    
        #print(f"len KB = {len(lisd1)}")
        counter = 0
        counter2 = 0
        flagged_sentences = []
        inferred_sentences = []
# Maybe make a new list and add new sentences, then add those to the KB after the loop.
# also maybe it is nec. to separate the finding new sentences and updating the KB into 2 loops
        for sentence_1 in self.knowledge:
            counter += 1
            #print(f"counter sentence_1 = {counter}")
            for sentence_2 in self.knowledge:
                counter2 += 1
                if not sentence_1.__eq__(sentence_2):
                    if sentence_2.cells.issubset(sentence_1.cells) and sentence_1.cells and sentence_2.cells:
                        print(f"####################################\nforLoop: sentence_2 rep. = {counter2}")
                        print(f"current sentences are: \nSentence_1 = {sentence_1.__str__()}\nSentence_2 = {sentence_2.__str__()}\n####################################\n")
                        print(f"subset = {sentence_2.cells.issubset(sentence_1.cells)}")
                        print(f"sentence_1: cells = {sentence_1.cells}, count = {sentence_1.count}")
                        print(f"sentence_2: cells = {sentence_2.cells}, count = {sentence_2.count}")
                        new_cells = sentence_1.cells.difference(sentence_2.cells) 
                        new_count = sentence_1.count - sentence_2.count
                        #print(f"sentence_1 edited: cells = {sentence_1.cells}, count = {sentence_1.count}")
                        
  
                        print(f"new_cells = {new_cells}\nnew_count = {new_count}")
                        if new_cells:
                            if len(new_cells) == new_count:
                                print("inferred new mines")
                                new_mines.update(new_cells)
                            if new_count == 0:
                                print("inferred new safes")
                                new_safes.update(new_cells)                            
                            else:
                                print(f"new cells = {new_cells}")
                                inferred_sentence = Sentence(new_cells, new_count)
                                print(f"inferred sentence = {inferred_sentence}")
                                if inferred_sentence not in inferred_sentences:
                                    inferred_sentences.append(inferred_sentence)

        for infer_sentence in inferred_sentences:
            self.knowledge.append(infer_sentence)       
                      
        for sentence in self.knowledge:                 
            if len(sentence.cells) == sentence.count:
                print("found new_mine from sentence_1")
                print(sentence.__str__())
                new_mines.update(sentence.cells)
                flagged_sentences.append(sentence)
            elif sentence.count == 0:
                print("found new_safe from sentence_1") 
                print(sentence.__str__())
                new_safes.update(sentence.cells)
                flagged_sentences.append(sentence)

        for flagged_sentence in flagged_sentences:
            print(f"Flagged sentence remove = {flagged_sentence}")            
            self.knowledge.remove(flagged_sentence)

        # mark all additional mines found
        if new_mines:         
            for mine in new_mines:
                self.mark_mine(mine)   

        # mark all additional safe moves found
        if new_safes:            
            for safe in new_safes:
                self.mark_safe(safe)
        
        # remove empty sets for better performance     
        for sentence in self.knowledge:
            if not sentence.cells:
                self.knowledge.remove(sentence)

        #print(f"safe = {self.safes}")
        #print(f"mines = {self.mines}")
        #print(f"moves made = {self.moves_made}")
        lisd = []
        for element in self.knowledge:
            lisd.append(element.__str__())

        print(f"KB = {lisd}")
        print(f"num of list items = {len(lisd)}")
        print("AI -> add_KB: END\n----------------------------------------------------------------------\n") 

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        # returns the first safe, unused move
        if self.safes:
            moves = []
            for safe in self.safes:
                if safe not in self.moves_made:
                    moves.append(safe)
                    return moves[0]
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # creates all possible moves
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                moves.add((i, j))
                
        # reduces moves using existing information
        moves.difference_update(self.moves_made)
        moves.difference_update(self.mines)
        
        # returns a random move
        if moves:
            move = random.choice(list(moves))           
            return move
        return None

                


