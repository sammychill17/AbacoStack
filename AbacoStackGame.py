from AbacoStack import *

if __name__ == '__main__':
    """
    This main function runs the game
    - It will take the size and depth inputs from the user in order to initialize the game
    - the game  will keep the user playing but the user until they want to quit
    -  The player will be congratulated once they match the card configuration
    """
    # user inputs
    size = int(input("Please enter the number of stacks between 2 and 5: "))
    depth = int(input("Please enter the depth of stacks between 2 and 4: "))
    # initialize the stacks and card configuration through the AbacoStack class
    abaco = AbacoStack(size, depth)
    # display
    abaco.show(abaco.card)
    # initialize variable to be used during iteration
    play = "Y"
    solved = False
    while play.upper() != "N":
        move = input("Enter your move(s) [Q for quit and R to reset]: ")
        while move.upper() != "Q" and not solved:
            if move.upper() == "R":
                abaco.reset()
                abaco.show()
            else:
                moves = move.split(" ")
                temp = abaco.moves
                for i in range(len(moves)):
                    if i < 5:
                        in_temp = abaco.moves
                        # print("Move: ", moves[i])
                        moved = abaco.moveBead(moves[i])
                        if not moved:
                            break
                if temp == abaco.moves:
                    abaco.show()
                else:
                    abaco.show(abaco.card)
                # check if solved
            solved = abaco.isSolved()
            if solved:
                print("Congratulations! Well done.")
            else:
                move = input("Enter your move(s) [Q for quit and R to reset]: ")
        play = input("Would you like another game?[Y/N]:")
        if play != "Y" and play != "N":
            print("Invalid input(", play, ")")
        elif play == "Y":
            abaco = AbacoStack(size, depth)
            solved = False
            abaco.show(abaco.card)
