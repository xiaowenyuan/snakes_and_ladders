from random import randrange
from math import sqrt

def generate_grid(grid, player_dictionary):
    count = 1
    row_length = int(sqrt(len(grid)))
    for row in range(1, row_length+1):
        row_for_print = ""
        for square in range(1,row_length+1):
            player_token = ""
            if grid[count-1].occupied():
                list_of_players = grid[count-1].obtain_players()
                for player in list_of_players:
                    player_token += player
            if grid[count-1].query_is_free():
                if row == 1 and square <10:
                    count_for_print = f"|      {player_token}{count}     |"
                elif row > 9 and square > 9:
                    count_for_print = f"|     {player_token}{count}    |"
                elif row > 10:
                    count_for_print = f"|     {player_token}{count}    |"
                else:
                    count_for_print = f"|      {player_token}{count}     |"
            else:
                if grid[count-1].query_if_snake_head():
                    count_for_print = f"|    {player_token}{count}SH{str(grid[count-1].snake_tail_square.get_number())}   |"
                elif grid[count-1].query_if_snake_tail():
                    count_for_print = f"|     {player_token}{count}ST    |"
                elif grid[count-1].query_if_ladder_bottom():
                    count_for_print = f"|    {player_token}{count}LB{str(grid[count-1].ladder_top_square.get_number())}   |"
                else:
                    count_for_print = f"|    {player_token}{count}LT    |"

            row_for_print += count_for_print
            count+=1
        print(row_for_print)
        print("\n")

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
        self.occupied_by_players = []
    
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

    def stepped_on(self, player):
        self.occupied_by_players.append(player)

    def stepped_off(self, player):
        self.occupied_by_players = [x for x in self.occupied_by_players if x is not player]

    def obtain_players(self):
        return self.occupied_by_players
    
    def occupied(self):
        if len(self.occupied_by_players) == 0:
            return False
        else:
            return True

    def get_number(self):
        return self.number

    def set_snake_head(self, tail):
        self.is_snake_head = True
        self.snake_tail_square = tail 
        tail.set_snake_tail()
        
    def set_snake_tail(self):
        self.is_snake_tail = True 
    
    def give_snake_tail_square_number(self):
        return self.snake_tail_square.get_number()

    def give_ladder_top_square_number(self):
        return self.ladder_top_square.get_number()
    
    def set_ladder_top(self):
        self.is_ladder_top = True

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
    
    def reach_end(self):
        if self.end:
            return True
        else:
            return False
    
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

def set_board_snakes(n, list_of_squares):
    for i in range(1, n+1):
        snake_head = randrange(10, len(list_of_squares)-1) - 1
        while list_of_squares[snake_head].query_if_ladder_top() == True or list_of_squares[snake_head].query_if_ladder_bottom() == True or list_of_squares[snake_head].query_if_snake_tail() == True:
            snake_head = randrange(11, len(list_of_squares)-1) - 1
        snake_tail = randrange(2, list_of_squares[snake_head].get_number()) - 1
        while list_of_squares[snake_tail].query_if_ladder_top() == True or list_of_squares[snake_tail].query_if_ladder_bottom() == True or list_of_squares[snake_tail].query_if_snake_head() == True:
            snake_tail = randrange(2, list_of_squares[snake_head].get_number()) - 1
        list_of_squares[snake_head].set_snake_head(list_of_squares[snake_tail])

def set_board_ladders(n, list_of_squares):
    for i in range(1, n+1):
        #randomise square that will be the bottom of the ladder
        ladder_bottom = randrange(2, len(list_of_squares) - 10) - 1
        #check if the square already is a snake head, snake tail, or another ladder top or bottom
        while list_of_squares[ladder_bottom].query_if_ladder_top() == True or list_of_squares[ladder_bottom].query_if_snake_tail() == True or list_of_squares[ladder_bottom].query_if_snake_head() == True:
            ladder_bottom = randrange(2, len(list_of_squares) - 10) - 1
        #randomise square that will be the top of the ladder
        ladder_top = randrange(ladder_bottom+10, len(list_of_squares)-1) - 1
        #check if the square is already a snake head, snake tail or bottom of the ladder
        while list_of_squares[ladder_top].query_if_ladder_bottom() == True or list_of_squares[ladder_top].query_if_snake_tail() == True or list_of_squares[ladder_top].query_if_snake_head() == True:
            ladder_top = randrange(ladder_bottom+10, len(list_of_squares)-1) - 1
        #use the class method to set the ladder for the square
        list_of_squares[ladder_bottom].set_ladder_bottom(list_of_squares[ladder_top])

#the start_game function initialises the dictionary and 1st grid 
def start_game_for_each_player(player_dictionary, player, grid):
    #every player starts at square 1
    grid[0].stepped_on(player)
    #update players dictionary to reflect that each player is at grid1
    player_dictionary[player] = grid[0]


def each_turn(players, number_of_dice, grid):
    #gameplay is looped between each player
    for player in players.keys():
        print(f'Player {player}\'s turn.')
        #check what square the player is currently on 
        current_square = players[player]
        current_square_number = players[player].get_number()
        print(f'Player {player} is currently at square {current_square_number}')
        #each player starts by rolling the dice
        player_to_continue = input(f'Is Player {player} ready to roll the dice? Type Y to continue.') 
        while player_to_continue.lower() != 'y':
            player_to_continue = input(f'Is Player {player} ready to roll the dice? Type Y to continue.')
        dice_result = dice_roll(number_of_dice)
        print(f'Player {player} rolled a {dice_result}')
        #step off the current square 
        current_square.stepped_off(player)
        #move to the new square according to the dice result
        new_square_number = current_square_number + dice_result
        new_square_index = new_square_number - 1
        #check if new square number is below the max
        if new_square_number < len(grid):
            new_square = grid[new_square_index] 
            #check if square is ladder bottom or snake head
            if new_square.query_if_snake_head():
                print(f'Oh no! Player stepped on snake head at square {new_square_number}')
                snake_tail_square_number = new_square.give_snake_tail_square_number()
                new_square_number = snake_tail_square_number
                new_square_index = new_square_number - 1
                new_square = grid[new_square_index]
            elif new_square.query_if_ladder_bottom():
                print(f'Awesome! Player stepped on ladder at square {new_square_number}')
                ladder_top_square_number = new_square.give_ladder_top_square_number()
                new_square_number = ladder_top_square_number
                new_square_index = new_square_number - 1
                new_square = grid[new_square_index]
            #player steps on the correct square and update the dictionary accordingly
            new_square.stepped_on(player)
            players[player] = new_square
            #print out what square the player is now on 
            print(f'Player {player} has moved to square {new_square_number}')
            generate_grid(grid, players)
        else:
            grid[len(grid)-1].stepped_on(player)
            print(f'Player {player} has reached the end.')
            print(f'Player {player} has won the game.')
            generate_grid(grid, players)
            return True
    return False


def run_game():
    print('Welcome to Snakes and Ladders!')
    number_of_players = input('How many players are playing? Please insert a number between 1 to 4')
    while int(number_of_players) < 1 or int(number_of_players) > 4:
        number_of_players = input('How many players are playing? Please insert a number between 1 to 4')
    grid_number = input('What size of a board would you like? Please insert a number n to represent nxn board.')
    gameboard = generate_squares(int(grid_number))
    number_of_snakes_ladders = input(f'How many sets of snakes and ladders would you like on the board? Please insert a number between 1 to {grid_number}')
    while int(number_of_players) < 1 or int(number_of_players) > int(grid_number):
        number_of_snakes_ladders = input(f'How many sets of snakes and ladders would you like on the board? Please insert a number between 1 to {grid_number}')
    set_board_snakes(int(number_of_snakes_ladders), gameboard)
    set_board_ladders(int(number_of_snakes_ladders), gameboard)
    print('Generating your board...')
    print(gameboard)
    number_of_dice = input('How many dies would you like to use? Insert a number between 1 and 2.')
    while int(number_of_dice) < 1 or int(number_of_dice) > 2:
        number_of_dice = input('How many dies would you like to use? Insert a number between 1 and 2.')
    player_tokens_list = ['!', '@', '#', "?", '%', '&', '$', '*']
    players_and_grid = {}
    for i in range(1, int(number_of_players)+1):
        player_token = input(f'Choose a token to represent Player {i}: {str(player_tokens_list)}')
        player_tokens_list = [x for x in player_tokens_list if x is not player_token]
        start_game_for_each_player(players_and_grid, player_token, gameboard)
    print(f'Our players are:')
    for player in players_and_grid.keys():
        print(player + " ")
    generate_grid(gameboard, players_and_grid)
    game_over = False
    while not game_over:
        game_over = each_turn(players_and_grid, int(number_of_dice), gameboard)
    print('Game over. Thank you for playing.')

run_game()

        

        
