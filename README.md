# snakes_and_ladders

## Introduction
This is a simple Python project that I made for practice. To run it, simply call the file `script.py` in the terminal. In each round, the board's snakes and ladders will be generated randomly.

## Gameplay
Up to four people can play the game. Theoretically, there should be no limit on the number of players, but the wait time between the players will be too long if too many players are involved. 

The player can choose to set the size of the square board (`n*n`) limited between 8x8 to 12x12. Both lower and upper limits are theoretical; too low and it jeopardises the number of snakes and ladders that can be set on the board, and too high and it makes gameplay too long while the grid will also not fit in a standard terminal.

Each board will have the same number of snakes to ladders. The player can set this amount, but the maximum number is `n - 3` (n being the length of the board). This is to ensure that there will be as many snakes and ladders set on the board. 

The script can recognise if there is no appropriate square that can be set as snake tail or ladder bottom/top. It is therefore possible for fewer snakes or ladders to be generated than requested.

The board can be re-generated prior to the gameplay if the players are not happy with the snakes and ladders generated on the board. 

1 or 2 dies can be used. No extra roll is given if the player rolls a 6 or 12.

The player wins if they roll more than the required amount of steps to reach the end square (ie if `s` is the steps to the end square, player wins as long as `dice_roll > s`). There is no need to roll a precise amount. 

## The Board
After each dice roll, the script will print out the current state of the board. Each square is numbered, and may contain the following letters at the right side of the number: 

* `SHXX`: this refers to Snake Head. The number `XX` refers to where the snake tail (and hence the square the player will end up on) is.
* `ST`: this refers to Snake Tail.
* `LBXX`: this refers to Ladder Bottom. The number `XX` refers to where the ladder top (and hence the square the player will end up on) is.
* `LT`: this refers to Ladder Top.

The left side of each square number may show the players' tokens. Players can occupy the same square without any consequences. 

## Files
* `script.py`: This is the file that runs the game.
* `test.py`: This file contains testing functions, specifically the generation of snakes and ladders. 
* `script_testing.py`: This file is a carbon copy of `script.py`, except that `print` statements are uncommented. This file is used for testing. 
