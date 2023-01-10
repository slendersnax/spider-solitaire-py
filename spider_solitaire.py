import random, os

# -------------------------------------------------------------------------
# classes

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

# -------------------------------------------------------------------------
# global vars

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

# -------------------------------------------------------------------------
# functions

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
                row += t_colours[12] + t_ranks[col[i].rank] + t_colours[10]
                row += t_colours[col[i].suit] + t_suits[col[i].suit] + t_colours[10]
            row += " "
        row += " " + str(i + 1)
        print(row)

    print("")
    print("Completed Units: {}".format(nCompletedUnits))
    print("Deals: {}".format(nDeals))
    # make instructions screen
    # x to give up, d for deal

# based on the number of suits chosen we run through them enough times
# to get an equal amount of units of each available suit then generate cards
# we take the indexes of the suits and ranks (numbers) for easier comparison between cards    
def createAllCardsDeck(nNumberOfSuits):
    p_allCards = [] # p_allCards instead of t_ to denote it's in a func

    for i in range(nNumberOfSuits):                     
        for j in range(nTotalUnits // nNumberOfSuits):
            for r in range(len(t_ranks)):
                p_allCards.append(Card(i, r))

    return p_allCards

# function for inputting number of suits
def inputNumberOfSuits():
    clearScreen()
    print("How many suits do you want to play with? \nOptions are: one (1), two (2), or four (4)")
    p_nNumberOfSuits = int(input())

    while p_nNumberOfSuits not in [1, 2, 4]:
        print("Not acceptable, you can only play with one (1), two (2), or four (4) suits")
        print("Please enter the number of suits you wish to play with: ")
        p_nNumberOfSuits = int(input())

    return p_nNumberOfSuits

# dealing the cards from the all-card deck to the 
# columns and deals
def dealCards(p_allCards):
    p_deals = []
    p_columns = []
    # adding cards to the deals, 10 card in each deal
    for i in range(nTotalDeals):
        p_deals.append([])
        for j in range(10):
            p_deals[i].append(p_allCards.pop(random.randint(0, len(p_allCards) - 1)))

    # adding cards to the playing columns
    # first we create the columns
    for i in range(nTotalColumns):
        p_columns.append([])

    # we loop over the columns and add a randomly popped card until we have no cards left
    nCurrentCol = 0
    while len(p_allCards):
        p_columns[nCurrentCol].append(p_allCards.pop(random.randint(0, len(p_allCards) - 1)))
        nCurrentCol = (nCurrentCol + 1) % nTotalColumns

    return (p_deals, p_columns)

def revealBottomCards(p_columns):
    for col in p_columns:
        if len(col) > 0:
            col[-1].hidden = False

    return p_columns

# check the error messages for what we're checking in each condition
def isInputError(coordFrom, coordTo):
    for el in coordFrom:
        if el == '':
            return (True, "Please enter the coordinates of the card(s) you wish to move")
        if not el.isnumeric():
            return (True, "Please enter only numeric values for coordinates")

    if len(coordFrom) != 2:
        return (True, "There must be two inputs - column and row")

    nColLength = len(t_columns[int(coordFrom[0]) - 1])

    if int(coordFrom[0]) - 1 not in [num for num in range(nTotalColumns)]:
        return (True, "Column to move from must be a number between 1 and {}".format(nTotalColumns + 1))
            
    if int(coordFrom[1]) - 1 not in [num for num in range(nColLength)]:
        return (True, "Card/row to move from must be a number between 1 and respective column's length: {}".format(nColLength))

    # we transform the inputs into numerical values here for easier use further on
    coordFrom = [int(c) - 1 for c in coordFrom]
                
    if t_columns[coordFrom[0]][coordFrom[1]].hidden:
        return (True, "Card(s) to move must not be hidden")

    if coordTo == '':
        return (True, "Please enter the coordinates of the destination")

    if not coordTo.isnumeric():
        return (True, "Please enter only numeric values for the coordinates of the destination")

    if int(coordTo) - 1 not in [num for num in range(nTotalColumns)]:
        return(True, "Column to move to must be a number between 1 and {}".format(nTotalColumns))

    #same here
    coordTo = int(coordTo) - 1
    bSameSuit = True
    for i in range(coordFrom[1], len(t_columns[coordFrom[0]])):
        if t_columns[coordFrom[0]][i].suit != t_columns[coordFrom[0]][coordFrom[1]].suit:
            bSameSuit = False
            break

    if not bSameSuit:
        return (True, "Card(s) to move must all be of the same suit")

    bInOrder = True
    if coordFrom[1] < nColLength - 1: # aka we're moving a series of cards, not just one
        for i in range(coordFrom[1], len(t_columns[coordFrom[0]]) - 1):
            if t_columns[coordFrom[0]][i].rank - 1 != t_columns[coordFrom[0]][i + 1].rank:
                bInOrder = False
                break
        
    if not bInOrder:
        return (True, "Card(s) to move must be in direct descending order")

    if len(t_columns[coordTo]) == 0 or t_columns[coordFrom[0]][coordFrom[1]].rank + 1 == t_columns[coordTo][-1].rank:
        pass
    else:
        return (True, "The rank of the topmost card to be moved must be 1 below the bottom card of the column to be moved to")
            
    return (False, "")

def gameOver():
    if nCompletedUnits == nTotalUnits:
        return True
    return False

# -------------------------------------------------------------------------
# this is where the game itself begins

nCompletedUnits = 0
nDeals = nTotalDeals # is the same as len(t_deals), do we really need it? - yes, as it is right now

nNumberOfSuits = inputNumberOfSuits()
t_allCards = createAllCardsDeck(nNumberOfSuits)

# shuffling all the cards
random.shuffle(t_allCards)

(t_deals, t_columns) = dealCards(t_allCards)

t_columns = revealBottomCards(t_columns)

# -------------------------------------------------------------------------
# gameloop

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
    else: # we check if the inputs are alright
        (b_s.bIsError, b_s.msg) = isInputError(coordFrom, coordTo)

    if not b_s.bIsError and not bUsedDeal:
        # transforming inputs into numerical values
        coordFrom = [int(c) - 1 for c in coordFrom]
        coordTo = int(coordTo) - 1

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
                nSeriesLen = 1

        # we have a completed unit
        if nSeriesLen == len(t_ranks):
            # a unit's end is at the end of the list, so we can just pop the last card 13 times
            for i in range(len(t_ranks)):
                col.pop()

            nCompletedUnits += 1

    t_columns = revealBottomCards(t_columns)

    display()
    if b_s.bIsError:
        print("{}{}{}".format(t_colours[0], b_s.msg, t_colours[10]))
        print("Input again.")