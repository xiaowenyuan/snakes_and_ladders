from script_testing import generate_squares, set_board_snakes, set_board_ladders

def testing(tries,square,snake):
    print(f'\n Running {tries} iterations to generate size {square}x{square} grid with {snake} sets of snakes and ladders.')
    for i in range(tries):
        print(f'ITERATION {i}')
        test = generate_squares(square)
        set_board_snakes(snake, test)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        set_board_ladders(snake, test)
        print('---------------------------')
        print(f'finalised board')
        print(test)
        print('\n')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

testing(10, 5, 5)
testing(10, 3, 3)
testing(10, 8, 5)
testing(10, 10, 7)