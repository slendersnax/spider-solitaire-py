import random, os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

t_suits = ["H", "S", "D", "C"]
t_ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"] # note: i put T instead of 10 because I want every card to be displayed as [SR] (SuitRank)
t_colours = {
    0 : "\033[31m", # red
    1 : "\033[34m", # blue
    2 : "\033[91m", # light red
    3 : "\033[94m", # light blue
    10 : "\033[97m", # white
    11 : "\033[90m",  # gray
    12 : "\033[32m"   # green
}

nTotalUnits = 8
nTotalColumns = 10
nTotalHelpDecks = 4

t_columns = []
t_helpDecks = [] # the decks usually in the bottom right corner
t_allCards = []  # where every card is before we sort them into decks

def display():
    os.system("cls" if os.name == "nt" else "clear")
    nMaxCards = max([len(col) for col in t_columns])
    
    for i in range(nMaxCards):
        row = ""
        for col in t_columns:
            if i < len(col) - 1:
                row += t_colours[11] + "XX" + t_colours[10]
            elif i == len(col) - 1:
                row += t_colours[col[i].suit] + t_suits[col[i].suit] + t_colours[10]
                row += t_colours[12] + t_ranks[col[i].rank] + t_colours[10]
            else:
                row += "  "
            row += " "
        print(row)

    print("")
    print("Completed Units: {}".format(nCompletedUnits))
    print("Help Decks: {}".format(nHelpDecks))

# this is where the game itself begins

nCompletedUnits = 0
nHelpDecks = nTotalHelpDecks

print("How many suits do you want to play with? \nOptions are: one (1), two (2), or four (4)")
nNumberOfSuits = int(input())

while nNumberOfSuits not in [1, 2, 4]:
    print("Not acceptable, you can only play with one (1), two (2), or four (4) suits")
    print("Please enter the number of suits you wish to play with: ")
    nNumberOfSuits = int(input())

for i in range(nNumberOfSuits):                     # based on the number of suits chosen...
    for j in range(nTotalUnits // nNumberOfSuits):  # we run through them enough times to get equal amounts of units of each available suit
        for r in range(len(t_ranks)):               # and generate cards
            t_allCards.append(Card(i, r))           # we take the indexes of the suits and ranks for easier comparison between cards

random.shuffle(t_allCards)

for i in range(nTotalHelpDecks):
    t_helpDecks.append([])
    for j in range(10):
        t_helpDecks[i].append(t_allCards.pop(random.randint(0, len(t_allCards) - 1))) # to increase randomness, we take 10 random cards for the helper decks

for i in range(nTotalColumns):
    t_columns.append([])

nCurrentCol = 0
while len(t_allCards):
    t_columns[nCurrentCol].append(t_allCards.pop(random.randint(0, len(t_allCards) - 1))) # similarly with the columns
    nCurrentCol = (nCurrentCol + 1) % nTotalColumns

display()