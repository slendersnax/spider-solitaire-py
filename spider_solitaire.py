import random, os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.hidden = True

t_suits = ["H", "S", "D", "C"]
t_ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"] # note: i put T instead of 10 because I want every card to be displayed as [SR] (SuitRank)
t_colours = {
    0 : "\033[31m", # red
    1 : "\033[34m", # blue
    2 : "\033[91m", # light red
    3 : "\033[94m", # light blue
    10 : "\033[97m", # white
    11 : "\033[90m", # gray
    12 : "\033[32m"  # green
}

nTotalUnits = 8
nTotalColumns = 10
nTotalDeals = 4

t_columns = []
t_deals = []     # the decks usually in the bottom right corner
t_allCards = []  # where every card is before we sort them into decks

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def display():
    clearScreen()
    nMaxCards = max([len(col) for col in t_columns])

    row = "   "    
    for i in range(nTotalColumns):
        row += t_colours[10] + str(i + 1) + "  "

    print(row)
    for i in range(nMaxCards):
        s = str(i + 1)
        row = str(i + 1) + " " * (3 - len(s))
        for col in t_columns:
            if i >= len(col):
                row += "  "
            elif col[i].hidden:
                row += t_colours[11] + "XX" + t_colours[10];
            else:
                row += t_colours[col[i].suit] + t_suits[col[i].suit] + t_colours[10]
                row += t_colours[12] + t_ranks[col[i].rank] + t_colours[10]
            row += " "
        print(row)

    print("")
    print("Completed Units: {}".format(nCompletedUnits))
    print("Deals: {}".format(nDeals))
    print("Input format: col row, or 0 for helpdeck, 1 to give up")

# check if coordinates are within bounds
def invalidCoord(coord, nMaxCards):
    return len(coord) != 2 or coord[0] >= nTotalColumns or coord[0] < 0 or coord[1] >= len(t_columns[coord[0]]) or coord[1] < 0

# trim the whitespace at the edges, split by space to get each separate coordinate
# subtract one because list indexes begin at 0, input begins at 1
def getInput(inputText):
    return [int(c) - 1 for c in input(inputText).strip().split(" ")]

def gameOver():
    if nCompletedUnits == nTotalUnits:
        return True
    return False

# this is where the game itself begins -------------------------------------------------------------------------------------------

nCompletedUnits = 0
nDeals = nTotalDeals

clearScreen()
print("How many suits do you want to play with? \nOptions are: one (1), two (2), or four (4)")
nNumberOfSuits = int(input())

while nNumberOfSuits not in [1, 2, 4]:
    print("Not acceptable, you can only play with one (1), two (2), or four (4) suits")
    print("Please enter the number of suits you wish to play with: ")
    nNumberOfSuits = int(input())

# based on the number of suits chosen we run through them enough times
# to get an equal amount of units of each available suit then generate cards
# we take the indexes of the suits and ranks for easier comparison between cards
for i in range(nNumberOfSuits):                     
    for j in range(nTotalUnits // nNumberOfSuits):
        for r in range(len(t_ranks)):
            t_allCards.append(Card(i, r))

random.shuffle(t_allCards)

# adding cards to the deals
for i in range(nTotalDeals):
    t_deals.append([])
    for j in range(10):
        # to increase randomness, we take 10 random cards for the deal decks
        t_deals[i].append(t_allCards.pop(random.randint(0, len(t_allCards) - 1)))

# adding cards to the playing columns
# first we create a two-dimensional array by appending arrays to t_columns
for i in range(nTotalColumns):
    t_columns.append([])

# we loop over the columns and add a randomly popped card until we have no cards left
nCurrentCol = 0
while len(t_allCards):
    t_columns[nCurrentCol].append(t_allCards.pop(random.randint(0, len(t_allCards) - 1)))
    nCurrentCol = (nCurrentCol + 1) % nTotalColumns

# we reveal the cards at the bottom of every column
for col in t_columns:
    col[-1].hidden = False

# gameloop
display()
bUsedDeal = False

while not gameOver():
    if bUsedDeal:
        if nDeals > 0:
            print("Used a deal")
        else:
            print("No more deals")
        bUsedDeal = False
    
    # first col and then row, more intuitive imo
    coord = getInput("Input: ")

    if coord == [-1]:
        bUsedDeal = True
        if nDeals > 0:
            nDeals -= 1
            # use helpdeck here
    else:
        nMaxCards = max([len(col) for col in t_columns])

        while invalidCoord(coord, nMaxCards):
            coord = getInput("Invalid input, input both col and row within bounds: ")
        
        while t_columns[coord[0]][coord[1]].hidden:
            coord = getInput("Invalid input, card is still hidden. Input again: ")

        print(t_suits[t_columns[coord[0]][coord[1]].suit] + t_ranks[t_columns[coord[0]][coord[1]].rank])

    display()