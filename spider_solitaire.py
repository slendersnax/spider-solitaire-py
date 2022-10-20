import random, os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.hidden = True

    def same_suit(self, otherCard):
        return self.suit == otherCard.suit

class Error:
    def __init__(self):
        self.bIsError = False
        self.msg = ""
    
    def signal_error(self, _msg):
        self.bIsError = True
        self.msg = _msg
    
    def clear_error(self):
        self.bIsError = False
        self.msg = ""

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
    nLongestColumn = max([len(col) for col in t_columns])

    row = "   "    
    for i in range(nTotalColumns):
        row += t_colours[10] + str(i + 1) + "  "

    # here we print the cards
    print(row)
    for i in range(nLongestColumn):
        s = str(i + 1)  # we display the row number at the beginning and end
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
        row += " " + str(i + 1)
        print(row)

    print("")
    print("Completed Units: {}".format(nCompletedUnits))
    print("Deals: {}".format(nDeals))
    # make instructions screen
    # x to give up, d for deal

def gameOver():
    if nCompletedUnits == nTotalUnits:
        return True
    return False

# this is where the game itself begins -------------------------------------------------------------------------------------------

nCompletedUnits = 0
nDeals = nTotalDeals # is the same as len(t_deals), do we really need it? - yes, as it is right now

clearScreen()
print("How many suits do you want to play with? \nOptions are: one (1), two (2), or four (4)")
nNumberOfSuits = int(input())

while nNumberOfSuits not in [1, 2, 4]:
    print("Not acceptable, you can only play with one (1), two (2), or four (4) suits")
    print("Please enter the number of suits you wish to play with: ")
    nNumberOfSuits = int(input())

# based on the number of suits chosen we run through them enough times
# to get an equal amount of units of each available suit then generate cards
# we take the indexes of the suits and ranks (numbers) for easier comparison between cards
for i in range(nNumberOfSuits):                     
    for j in range(nTotalUnits // nNumberOfSuits):
        for r in range(len(t_ranks)):
            t_allCards.append(Card(i, r))

# shuffling all the cards
random.shuffle(t_allCards)

# adding cards to the deals, 10 card in each deal
for i in range(nTotalDeals):
    t_deals.append([])
    for j in range(10):
        t_deals[i].append(t_allCards.pop(random.randint(0, len(t_allCards) - 1)))

# adding cards to the playing columns
# first we create the columns
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

# gameloop ---------------------------------------------------------------------------------------------------------------
display()
bUsedDeal = False
b_s = Error() # because errors are bull_shit B) yeeeaahhhhhh

while not gameOver():
    if bUsedDeal:
        if nDeals > 0:
            print("Used a deal")
        else:
            print("No more deals")
        bUsedDeal = False

    coordFrom = [c for c in input("Input col, row to move from: ").strip().split(" ")]
    coordTo = input("Input column to move to: ")
    b_s.signal_error("") # automatically error is TRUE, if we pass all the checks, error becomes FALSE

    # dealing cards
    if coordFrom == ['d'] or coordTo == 'd':
        bUsedDeal = True
        b_s.clear_error()
        if nDeals > 0:
            nDeals -= 1
            for col in t_columns:
                col.append(t_deals[-1].pop())
            
            t_deals.pop(-1)
    elif coordFrom == ['x']:
        print("Player gave up")
        break
    # condition checking starts here
    # see error messages for what the conditions are
    # FIX: better/more readable way for this? pretty diff to check if-else pairs
    elif len(coordFrom) == 2:
        if int(coordFrom[0]) - 1 in [num for num in range(nTotalColumns)]:
            nMaxRow = len(t_columns[int(coordFrom[0]) - 1])
            if int(coordFrom[1]) - 1 in [num for num in range(nMaxRow)]:
                # we transform the inputs into numerical values here for easier use further on
                coordFrom = [int(c) - 1 for c in coordFrom]
                if not t_columns[coordFrom[0]][coordFrom[1]].hidden:
                    if int(coordTo) - 1 in [num for num in range(nTotalColumns)]:
                        coordTo = int(coordTo) - 1
                        bSameSuit = True
                        for i in range(coordFrom[1], len(t_columns[coordFrom[0]])):
                            if t_columns[coordFrom[0]][i].suit != t_columns[coordFrom[0]][coordFrom[1]].suit:
                                bSameSuit = False
                                break

                        if bSameSuit:
                            bInOrder = True
                            if coordFrom[1] < nMaxRow - 1: # aka we're moving a series of cards, not just one
                                for i in range(coordFrom[1], len(t_columns[coordFrom[0]]) - 1):
                                    if t_columns[coordFrom[0]][i].rank - 1 != t_columns[coordFrom[0]][i + 1].rank:
                                        bInOrder = False
                                        break
                            
                            if bInOrder:
                                if len(t_columns[coordTo]) == 0 or t_columns[coordFrom[0]][coordFrom[1]].rank + 1 == t_columns[coordTo][-1].rank:
                                    b_s.clear_error()
                                else:
                                    b_s.signal_error("The rank of the topmost card to be moved must be 1 below the bottom card of the column to be moved to")
                            else:
                                b_s.signal_error("Card(s) to move must be in direct descending order")
                        else:
                            b_s.signal_error("Card(s) to move must all be of the same suit")
                    else:
                        b_s.signal_error("Column to move to must be a number between 1 and {}".format(nTotalColumns))
                else:
                    b_s.signal_error("Card(s) to move must not be hidden")
            else:
                b_s.signal_error("Card/row to move from must be a number between 1 and respective column's length: {}".format(nMaxRow))
        else:
            b_s.signal_error("Column to move from must be a number between 1 and {}".format(nTotalColumns + 1))
    else:
        b_s.signal_error("There must be two inputs - column and row")

    if not b_s.bIsError and not bUsedDeal:
        # moving the card(s)
        for i in range(coordFrom[1], len(t_columns[coordFrom[0]])):
            t_columns[coordTo].append(t_columns[coordFrom[0]].pop(coordFrom[1]))

    # checking for completed units
    for col in t_columns:
        nSeriesLen = 1
        for i in range(len(col) - 1):
            # checking if suits are same and ranks are in order
            if not col[i].hidden and col[i].suit == col[i + 1].suit and col[i].rank - 1 == col[i + 1].rank:
                nSeriesLen += 1
            else:
                nSeriesLen = 0

        # we have a completed unit
        if nSeriesLen == len(t_ranks):
            # a unit's end is at the end of the list, so we can just pop the last card 13 times
            for i in range(len(t_ranks)):
                col.pop()

            nCompletedUnits += 1

    # revealing the bottom cards if they haven't been revealed yet
    for col in t_columns:
        if len(col) > 0:
            col[-1].hidden = False

    display()
    if b_s.bIsError:
        print("{}{}{}".format(t_colours[0], b_s.msg, t_colours[10]))
        print("Input again.")