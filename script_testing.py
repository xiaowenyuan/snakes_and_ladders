from random import randrange, choice
from math import sqrt

def generate_grid(grid):
    count = 1
    index = 0
    row_length = int(sqrt(len(grid)))
    for row in range(1, row_length+1):
        row_for_print = ""
        for square in range(1,row_length+1):
            player_token = ""
            if grid[index].occupied():
                list_of_players = grid[index].obtain_players()
                for player in list_of_players:
                    player_token += player
            if grid[index].query_is_free():
                if row == 1 and square <10:
                    count_for_print = f"|      {player_token}{count}     |"
                elif row > 9 and square > 9:
                    count_for_print = f"|     {player_token}{count}    |"
                elif row > 10:
                    count_for_print = f"|     {player_token}{count}    |"
                else:
                    count_for_print = f"|      {player_token}{count}     |"
            else:
                if grid[index].query_if_snake_head():
                    count_for_print = f"|    {player_token}{count}SH{grid[index].snake_tail_square.get_label()}   |"
                elif grid[count-1].query_if_snake_tail():
                    count_for_print = f"|     {player_token}{count}ST    |"
                elif grid[count-1].query_if_ladder_bottom():
                    count_for_print = f"|    {player_token}{count}LB{grid[index].ladder_top_square.get_label()}   |"
                else:
                    count_for_print = f"|    {player_token}{count}LT    |"

            row_for_print += count_for_print
            count+=1
            index += 1
        print(row_for_print)
        print("\n")

class Square:
    def __init__(self, index, snake_head = False, ladder_bottom = False, start = False, end = False):
        self.index = index
        self.label = str(self.index + 1)
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
        to_be_returned = self.label
        if self.is_snake_head:
            to_be_returned += ("SH" + self.snake_tail_square.get_label())
        if self.is_snake_tail:
            to_be_returned += "ST" 
        if self.is_ladder_bottom:
            to_be_returned += ("LB" + self.ladder_top_square.get_label())
        if self.is_ladder_top:
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

    def get_label(self):
        return self.label

    def get_index(self):
        return self.index

    def set_snake_head(self, tail):
        self.is_snake_head = True
        self.snake_tail_square = tail 
        tail.set_snake_tail()
        
    def set_snake_tail(self):
        self.is_snake_tail = True 
    
    def get_snake_tail_square(self):
        return self.snake_tail_square

    def get_ladder_top_square(self):
        return self.ladder_top_square
    
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
    for i in range(0,n**2):
        if i == 0:
            square_i = Square(i, start = True)
        elif i == n**2 - 1:
            square_i = Square(i, end = True)
        else:    
            square_i = Square(i)
        list_of_squares.append(square_i)
    return list_of_squares

def set_board_snakes(n, list_of_squares):
    row_length = int(sqrt(len(list_of_squares)))
    print(f'Setting {n} snakes...')
    for i in range(0, n):
        print(f'Looping the outer for loop ... loop number {i+1} out of {n}')
        square_index_for_snake_head = randrange(row_length, len(list_of_squares) - 1)
        while list_of_squares[square_index_for_snake_head].query_is_free() == False:
            print(f'COLLISION FOUND! Entering while loop to change snake head square index {square_index_for_snake_head} which is square label {list_of_squares[square_index_for_snake_head].get_label()}')
            square_index_for_snake_head = randrange(row_length, len(list_of_squares) - 1)
        #make a list of possible indexes for snake tail
        snake_tail_list = range(1, square_index_for_snake_head)
        #remove from the list any square that is not free
        snake_tail_list = [square for square in snake_tail_list if list_of_squares[square].query_is_free()]
        #check length of snake_tail_list, if it is empty, then possible snake tail index is None, if not use random choice to generate index for snake tail
        if len(snake_tail_list) == 0 :
            square_index_for_snake_tail = None
        else:
            square_index_for_snake_tail = choice(snake_tail_list)
        if square_index_for_snake_tail != None:
            #set the snake head and tail squares using the class method
            list_of_squares[square_index_for_snake_head].set_snake_head(list_of_squares[square_index_for_snake_tail])
        else:
            if i > 0:
                print(f'There is no suitable square for snake tail {i}. Only {i-1} snakes are set')
            else:
                print('There is no suitable square to set for snake tail to bet set. No snakes are set.')
            break
        #print(list_of_squares)

def set_board_ladders(n, list_of_squares):
    row_length = int(sqrt(len(list_of_squares)))
    print(f'Setting {n} ladders...')
    for i in range(0, n):
        print(f'\n Looping the outer for loop ... loop number {i+1} out of {n}')
        print('--->Setting ladder bottom...<---')
        ladder_bottom_list = range(1, len(list_of_squares) - row_length)
        ladder_bottom_list = [square for square in ladder_bottom_list if list_of_squares[square].query_is_free()]
        print('Possible square indexes for ladder bottom are:')
        print(ladder_bottom_list)
        if len(ladder_bottom_list) == 0 :
            possible_square_index_for_ladder_bottom = None
        else:
            possible_square_index_for_ladder_bottom = choice(ladder_bottom_list)
            ladder_top_list = range(possible_square_index_for_ladder_bottom + row_length, len(list_of_squares) - 1)
            ladder_top_list = [i for i in ladder_top_list if list_of_squares[i].query_is_free()]
            print(f'If we pick {possible_square_index_for_ladder_bottom}, this is the possible list of possible square index for ladder top:')
            print(ladder_top_list)
            ladder_bottom_while_loop_count = 1
            #check if the possible ladder botom index will + row_length = the last index of the grid or if the length of possible ladder top indexes list is 0
            while possible_square_index_for_ladder_bottom + row_length == len(list_of_squares) - 1 or len(ladder_top_list) == 0:
                print(f'Entering inner while loop for the ladder bottom as {possible_square_index_for_ladder_bottom} cannot be chosen')
                #removing the conflicted possible square index from ladder_bottom_list
                ladder_bottom_list = [square for square in ladder_bottom_list if square is not possible_square_index_for_ladder_bottom]
                if len(ladder_bottom_list) == 0 :
                    possible_square_index_for_ladder_bottom = None
                    break
                print('Revised square indexes for ladder bottom are:')
                print(ladder_bottom_list)
                possible_square_index_for_ladder_bottom = choice(ladder_bottom_list)
                #regenerating ladder_top_list to check for the while loop
                ladder_top_list = range(possible_square_index_for_ladder_bottom + row_length, len(list_of_squares) - 1)
                ladder_top_list = [square for square in ladder_top_list if list_of_squares[square].query_is_free()]
                print(f'Picking {possible_square_index_for_ladder_bottom} as possible square index')
                print(f'If we pick {possible_square_index_for_ladder_bottom}, this is the possible list of possible square index for ladder top:')
                print(ladder_top_list)
                ladder_bottom_while_loop_count += 1
                if ladder_bottom_while_loop_count > len(list_of_squares):
                    possible_square_index_for_ladder_bottom = None
                    break
        square_index_for_ladder_bottom = possible_square_index_for_ladder_bottom
        if square_index_for_ladder_bottom != None:
            #if the index is not None, then pick the ladder top
            print(f'Square index {square_index_for_ladder_bottom} is picked for ladder bottom')
            print(list_of_squares)
            print('--->Setting ladder top...<---')
            print('Possible square indexes for ladder top are:')
            print(ladder_top_list)
            if len(ladder_top_list) == 0:
                if i > 0:
                    print(f'No possible square that can be set for ladder {i}. Only {i-1} ladders are set on the board.')
                else:
                    print(f'No possible square that can be set for ladder. {i} ladder is set on the board.')
                break
            square_index_for_ladder_top = choice(ladder_top_list)
            print(f'Square index {square_index_for_ladder_top} is chosen as ladder top to ladder bottom index {square_index_for_ladder_bottom}')
            # use the class method to set the ladder for the square
            list_of_squares[square_index_for_ladder_bottom].set_ladder_bottom(list_of_squares[square_index_for_ladder_top])
            print(list_of_squares)
        else:
            if i > 0:
                print(f'No possible square that can be set for ladder {i}. Only {i-1} ladders are set on the board.')
            else:
                print(f'No possible square that can be set for ladder. {i} ladder is set on the board.')
            break

def dice_roll(number_of_dice):
    result = 0
    for dice in range(1, number_of_dice+1):
        result += randrange(1,7)
    return result

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
        current_square_label = current_square.get_label()
        current_square_index = current_square.get_index()
        print(f'Player {player} is currently at square {current_square_label}')
        #each player starts by rolling the dice
        player_to_continue = input(f'Is Player {player} ready to roll the dice? Type Y to continue.') 
        while player_to_continue.lower() != 'y':
            player_to_continue = input(f'Is Player {player} ready to roll the dice? Type Y to continue.')
        dice_result = dice_roll(number_of_dice)
        print(f'Player {player} rolled a {dice_result}')
        #step off the current square 
        current_square.stepped_off(player)
        #move to the new square according to the dice result
        new_square_index = current_square_index + dice_result
        #check if new square index is below the max
        if new_square_index < len(grid) - 1:
            new_square = grid[new_square_index] 
            new_square_label = new_square.get_label()
            #check if square is ladder bottom or snake head
            if new_square.query_if_snake_head():
                print(f'Oh no! Player stepped on snake head at square {new_square.get_label()}')
                snake_tail_square= new_square.get_snake_tail_square()
                new_square_index = snake_tail_square.get_index()
                new_square_label = snake_tail_square.get_label()
                new_square = grid[new_square_index]
            elif new_square.query_if_ladder_bottom():
                print(f'Awesome! Player stepped on ladder at square {new_square_label}')
                ladder_top_square = new_square.get_ladder_top_square()
                new_square_index = ladder_top_square.get_index()
                new_square_label = ladder_top_square.get_label()
                new_square = grid[new_square_index]
            #player steps on the correct square and update the dictionary accordingly
            new_square.stepped_on(player)
            players[player] = new_square
            #print out what square the player is now on 
            print(f'Player {player} has moved to square {new_square_label}')
            generate_grid(grid)
        else:
            grid[len(grid)-1].stepped_on(player)
            print(f'Player {player} has reached the end.')
            print(f'Player {player} has won the game.')
            generate_grid(grid)
            return True
    return False


def run_game():
    print('Welcome to Snakes and Ladders!')
    number_of_players = input('How many players are playing? Please insert a number between 1 to 4')
    while int(number_of_players) < 1 or int(number_of_players) > 4:
        number_of_players = input('How many players are playing? Please insert a number between 1 to 4')
    grid_number = input('What size of a board would you like? Please insert a number n to represent nxn board, and n is between 8 and 12.')
    while int(grid_number) < 8 or int(grid_number) > 12:
        grid_number = input('What size of a board would you like? Please insert a number n to represent nxn board, and n is between 8 and 12.')
    gameboard = generate_squares(int(grid_number))
    permissible_snakes_ladders = int(grid_number) - 3
    number_of_snakes_ladders = input(f'How many sets of snakes and ladders would you like on the board? Please insert a number between 1 to {permissible_snakes_ladders}')
    while int(number_of_snakes_ladders) < 1 or int(number_of_snakes_ladders) > permissible_snakes_ladders:
        number_of_snakes_ladders = input(f'How many sets of snakes and ladders would you like on the board? Please insert a number between 1 to {permissible_snakes_ladders}')
    print('Generating your board...')
    set_board_snakes(int(number_of_snakes_ladders), gameboard)
    set_board_ladders(int(number_of_snakes_ladders), gameboard)
    number_of_dice = input('How many dies would you like to use? Insert a number between 1 and 2.')
    while int(number_of_dice) < 1 or int(number_of_dice) > 2:
        number_of_dice = input('How many dies would you like to use? Insert a number between 1 and 2.')
    player_tokens_list = ['!', '@', '#', "?", '%', '&', '$', '*']
    players_and_grid = {}
    for i in range(1, int(number_of_players)+1):
        player_token = input(f'Choose a token to represent Player {i}: {str(player_tokens_list)}')
        while player_token not in player_tokens_list:
          player_token = input(f'Choose a token to represent Player {i}: {str(player_tokens_list)}')  
        player_tokens_list = [x for x in player_tokens_list if x is not player_token]
        start_game_for_each_player(players_and_grid, player_token, gameboard)
    print(f'Our players are:')
    for player in players_and_grid.keys():
        print(player + " ")
    generate_grid(gameboard)
    regenerate_grid = input('Would you like to generate a new board? Type Y to generate a new grid or N to proceed with this grid.')
    while regenerate_grid.lower() == "y":
        gameboard = generate_squares(int(grid_number))
        set_board_snakes(int(number_of_snakes_ladders), gameboard)
        set_board_ladders(int(number_of_snakes_ladders), gameboard)
        print('Generating your board...')
        generate_grid(gameboard)
        regenerate_grid = input('Would you like to generate a new board? Type Y to generate a new grid or N to proceed with this grid.')
    while regenerate_grid.lower() != "y" and regenerate_grid.lower() != "n":
        regenerate_grid = input('Would you like to generate a new board? Type Y to generate a new grid or N to proceed with this grid.')
    game_over = False
    while not game_over:
        game_over = each_turn(players_and_grid, int(number_of_dice), gameboard)
    print('Game over. Thank you for playing.')

if __name__ == '__main__':
    run_game()

        

        
