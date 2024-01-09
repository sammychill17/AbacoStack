import random


class Card:
    """
    This  class generates a single card configuration using the number of colors(A, B, C, ...)
    and depth( the number of colors in one stack.
    Using random the colors can be shuffled randomly
    """

    # constructor
    def __init__(self, colors, depth):
        self.__beads = []
        self.colorList = []
        self.colors = colors
        self.depth = depth
        alpha = 'a'
        for i in range(0, colors):
            self.colorList.append(alpha.upper())
            alpha = chr(ord(alpha) + 1)
        for i in range(colors * depth):
            self.__beads.append(self.colorList[i % colors])

    # Shuffle the list  of beads
    def reset(self):
        random.shuffle(self.__beads)

    # Display the card config
    def show(self):
        for row in range(self.colors):
            print("|", end=" ")
            for col in range(self.depth):
                print(self.__beads[row + (col * self.colors)], end=" ")
            print("|")

    # get the specific stack
    def stack(self, n):
        index = self.depth * (n - 1)
        stack = []
        for i in range(self.depth):
            stack.append(self.__beads[index + i])
        return stack

    # String  to pring when printing this class as an object
    def __str__(self):
        s = "|"
        for i in range(0, len(self.__beads)):
            s = s + self.__beads[i]
            if (i + 1) % self.colors == 0 and (i + 1) != len(self.__beads):
                s = s + "||"
        return s + "|"

    # Replace the specified line in the file given with the card configuration
    def replace(self, filename, n):
        # read file
        file = open(filename, 'r')
        lines = file.readlines()
        count = 0
        for line in lines:
            count += 1
            print("Line{}: {}".format(count, line.strip()))
        file.close()
        # replace if within bounds, append otherwise
        if n < len(lines):
            lines[n] = ' '.join(self.__beads) + "\n"
        else:
            lines.append(' '.join(self.__beads) + "\n")
        # write back
        with open(filename, "w") as outfile:
            outfile.write("".join(lines))


class BStack:
    """
    This class will model the behaviour of a single stack - Last in First out.
    - We can push int the stack and Pop from the stack from the same end
    - we can peek what is on top of the stack
    - We can find an item at a specified index in the stack.
    - List will represent the stack, we therefore will appedn and pop from the end of the list.
    """

    # Set the maximum capacity of the stack and declare the list(stack)
    def __init__(self, capacity):
        if type(capacity) != int or capacity <= 0:
            print("Capacity Error, Enter the correct capacity")
        self._items = []
        self._capacity = capacity

    # add into the stack( append to the end of the list)
    def push(self, item):
        if self.isFull():
            print('Error: Stack is full')
        else:
            self._items.append(item)

    # Check what is at the end of list( which is the top of our stack)
    def peek(self):
        if len(self._items) == 0:
            print('Error: Stack is empty')
            return None
        return self._items[self.size() - 1]

    # find item at the given index return None if not found
    def find(self, index):
        if self.size() > index >= 0:
            return self._items[index]
        else:
            return None

    # return true if the stack is full
    def isFull(self):
        return len(self._items) == self._capacity

    # remove and return the last added item into the list(stack)
    def pop(self):
        if len(self._items) == 0:
            print('Error: Stack is empty')
            return ""
        return self._items.pop()

    # return the number of items in our list(stack)
    def size(self):
        return len(self._items)

    def capacity(self):
        return self._capacity

    def __str__(self):
        stackView = self._items.copy()
        stackView.reverse()
        return "[" + " ".join(stackView) + "]"


class AbacoStack:
    """
    This class Uses the Stack  and Card class to enable movement of colors/beads from one stack to another
    We have new list (named topRow) to help with the movement of color/beads from one stack to another.
    This class has functions to rest the stacks, show the stacks, verify whether the  card configuration
    was solved using the stacks
    """

    def __init__(self, stacksNum, depth):
        self.stacks = []
        self.topRow = [None] * (stacksNum + 2)
        self.moves = 0
        self.card = Card(stacksNum, depth)
        for i in range(stacksNum):
            stack = BStack(depth)
            for d in range(depth):
                stack.push(self.card.colorList[i])
            self.stacks.append(stack)
        self.card.reset()

    def moveBead(self, move):
        moved = False
        if len(move) < 2:
            return moved
        possibleMoves = ['r', 'l', 'u', 'd']
        m = int(move[0])
        direction = move[1]

        if m < 0 or m > (len(self.stacks) + 1) or direction not in possibleMoves:
            raise Exception('Error: Invalid Move')

        for i in range(-1, len(self.stacks) + 1):
            if i == (m - 1):
                # check if item is there
                if self.topRow[m] is not None:
                    if direction == possibleMoves[0]:
                        # move right
                        if m < len(self.topRow) - 1 and self.topRow[m + 1] is None:
                            self.topRow[m + 1] = self.topRow[m]
                            self.topRow[m] = None
                            self.moves = self.moves + 1
                            moved = True
                        else:
                            print("Error: Invalid Move")
                    elif direction == possibleMoves[1]:
                        # move left
                        if m > 0 and self.topRow[m - 1] is None:
                            self.topRow[m - 1] = self.topRow[m]
                            self.topRow[m] = None
                            self.moves = self.moves + 1
                            moved = True
                        else:
                            print("Error: Invalid Move")
                    elif direction == possibleMoves[3] and len(self.stacks) > i > -1:
                        # move down
                        if not self.stacks[i].isFull():
                            self.stacks[i].push(self.topRow[m])
                            self.topRow[m] = None
                            self.moves = self.moves + 1
                            moved = True
                        else:
                            print("Error: Invalid Move")
                    else:
                        print("Error: Invalid Move")
                else:
                    if len(self.stacks) > i > -1 and self.stacks[i].peek() is not None:

                        if direction == possibleMoves[2]:
                            # move up
                            item = self.stacks[i].pop()
                            self.topRow[m] = item
                            self.moves = self.moves + 1
                            moved = True
                        else:
                            print("Error: Invalid Move")
                return moved

    # Reset the stacks to have their original one color for each
    def reset(self):
        self.stacks.clear()
        self.topRow.clear()
        self.topRow = [None] * (self.card.colors + 2)
        self.moves = 0
        for i in range(self.card.colors):
            stack = BStack(self.card.depth);
            for d in range(self.card.depth):
                stack.push(self.card.colorList[i])
            self.stacks.append(stack)

    # return true if the card configuration matched with the user's stacks
    def isSolved(self):
        solved = True
        for i in range(self.card.colors):
            stck = self.card.stack(i + 1)
            for x in range(self.card.depth):
                if stck[(len(stck) - 1) - x] != self.stacks[i].find(x):
                    solved = False
        return solved

    # display the top row and the stacks and card when  not None
    def show(self, card=None):
        for x in range(len(self.topRow)):
            print(x, end=" ")
        print()
        for x in range(len(self.topRow)):
            n = "." if self.topRow[x] is None else self.topRow[x]
            print(n, end=" ")

        copiedStacks = self.stacks.copy()

        if card is not None:
            print("\t\tCard", end=" ")
            for x in range(self.stacks[0].capacity()):
                i = (self.stacks[0].capacity() - 1) - x
                print("\n|", end=" ")
                for j in range(len(self.stacks)):
                    diff = self.stacks[j].capacity() - self.stacks[j].size()
                    if diff > 0 and x < diff:
                        print(".", end=" ")
                    else:
                        # index = (i - diff) if i - diff > 0 else ((i - diff) * -1)
                        print(self.stacks[j].find(i), end=" ")
                print("|", end="     ")
                print("|", end=" ")
                for j in range(len(self.stacks)):
                    print(card.stack(j + 1)[x], end=" ")
                print("|", end=" ")
        else:

            for x in range(self.stacks[0].capacity()):
                i = (self.stacks[0].capacity() - 1) - x
                print("\n|", end=" ")
                for j in range(len(self.stacks)):
                    diff = self.stacks[j].capacity() - self.stacks[j].size()
                    if diff > 0 and x < diff:
                        print(".", end=" ")
                    else:
                        # index = (i - diff) if i - diff > 0 else ((i - diff) * -1)
                        print(self.stacks[j].find(i), end=" ")
                print("|", end=" ")
        print("\n+-------+\t", self.moves, " moves\n")

    def __str__(self):
        s = ""
        for x in range(len(self.topRow)):
            n = "." if self.topRow[x] == "" else self.topRow[x]
            s = s + n + " "
        for i in range(self.stacks[0].capacity()):
            s = s + "\n| "
            for j in range(len(self.stacks)):
                s = s + self.stacks[j].find(i) + " "
            s = s + "|"
        return s


if __name__ == '__main__':
    # Test Card class
    '''
    c = Card(3, 3)
    c.show()
    print(c)
    c.reset()
    c.show()
    print(c)
    c.replace("data.txt", 5)
    '''
    # Test BStack Class
    '''
    print("\nTesting BStack Class")
    b = BStack(3)
    b.pop()
    b.push("A")
    b.push("B")
    print(b)
    print(b.peek())
    b.pop()
    print(b.peek())
    '''
    # Testing AbacoStack Class
    print("\nTesting AbacoStack Class")
    a = AbacoStack(3, 3)
    a.show()
    a.show(a.card)
    a.card.show()
