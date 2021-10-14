from random import randrange

def generate_grid(n):
    count = 1
    for row in range(1,n+1):
        row_for_print = ""
        for square in range(1,n+1):
            if row == 1 and square <10:
                count_for_print = f"|   0{count}   |"
            else:
                count_for_print = f"|   {count}   |"
            row_for_print += count_for_print
            count+=1
        print(row_for_print)
        print("\n")

#generate_grid(10)

class Square:
    def __init__(self, number, snake_head = False, ladder_bottom = False, start = False, end = False):
        self.number = number
        self.is_snake_head = snake_head
        self.is_ladder_bottom = ladder_bottom
        self.start = start
        self.end = end
        self.is_snake_tail = False
        self.is_ladder_top = False
        self.snake_tail_square = None
        self.ladder_top_square = None
    
    def __repr__(self):
        to_be_returned = str(self.number)
        if self.is_snake_head:
            to_be_returned += ("SH" + str(self.snake_tail_square.get_number()))
        elif self.is_snake_tail:
            to_be_returned += "ST" 
        elif self.is_ladder_bottom:
            to_be_returned += ("LB" + str(self.ladder_top_square.get_number()))
        elif self.is_ladder_top:
            to_be_returned += "LT" 
        return to_be_returned

    def get_number(self):
        return self.number

    def set_snake_head(self, tail):
        self.is_snake_head = True
        self.snake_tail_square = tail 
        tail.set_snake_tail()
        
    def set_snake_tail(self):
        self.snake_tail = True 
    
    def set_ladder_top(self):
        self.ladder_top = True

    def set_ladder_bottom(self, top):
        self.is_ladder_bottom = True
        self.ladder_top_square = top
        top.set_ladder_top()

    def query_if_snake_head(self):
        if self.is_snake_head == True:
            return True
        else:
            return False
    
    def query_if_snake_tail(self):
        if self.is_snake_tail == True:
            return True
        else:
            return False

    def query_if_ladder_bottom(self):
        if self.is_ladder_bottom == True:
            return True
        else:
            return False
    
    def query_if_ladder_top(self):
        if self.is_ladder_top == True:
            return True
        else:
            return False

    def query_is_free(self):
        if self.query_if_snake_head() or self.query_if_snake_tail() or self.query_if_ladder_bottom() or self.query_if_ladder_top():
            return False
        return True
    
def generate_squares(n):
    list_of_squares = []
    for i in range(1,n**2+1):
        if i == 1:
            square_i = Square(i, start = True)
        elif i == n**2:
            square_i = Square(i, end = True)
        else:    
            square_i = Square(i)
        list_of_squares.append(square_i)
    return list_of_squares

sample_board = generate_squares(10)

def set_board_snakes(n, list_of_squares):
    for i in range(1, n+1):
        snake_head = randrange(11, len(list_of_squares))
        while not list_of_squares[snake_head].query_is_free():
            snake_head = randrange(11, len(list_of_squares))
        snake_tail = randrange(1, list_of_squares[snake_head].get_number())
        while not list_of_squares[snake_tail].query_is_free():
            snake_tail = randrange(1, list_of_squares[snake_head].get_number())
        list_of_squares[snake_head].set_snake_head(list_of_squares[snake_tail])

def set_board_ladders(n, list_of_squares):
    for i in range(1, n+1):
        #randomise square that will be the bottom of the ladder
        ladder_bottom = randrange(1, len(list_of_squares) - 10)
        #check if the square already is a snake head, snake tail, or another ladder top or bottom
        #while not list_of_squares[ladder_bottom].query_is_free():
            #ladder_bottom = randrange(1, len(list_of_squares) - 10)
        #randomise square that will be the top of the ladder
        ladder_top = randrange(ladder_bottom+10, len(list_of_squares))
        #check if the square is already a snake head, snake tail or bottom of the ladder
        #while not list_of_squares[ladder_top].query_is_free():
            #ladder_top = randrange(ladder_bottom+10, len(list_of_squares))
        #use the class method to set the ladder for the square
        list_of_squares[ladder_bottom].set_ladder_bottom(list_of_squares[ladder_top])
set_board_snakes(5, sample_board)
set_board_ladders(5, sample_board)
print(sample_board)
