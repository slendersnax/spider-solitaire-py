# spider solitaire in terminal/console

An implementation of the Spider Solitaire game using Python that is played in the console.

There's one thing to note - you can use a deal even if you have one or more empty columns / stacks. I never understood why this limitation existed in most versions of the game, so I didn't implement it.

### usage

You don't need any special Python libraries for this, just run `python spider_solitaire.py` (or the included `play-spider.sh` file if you're on Linux), which does the same thing.

### todo
- [ ] remake with OOP principles to handle decks and cards easier
- [ ] refactor a bit to clean it up
- [ ] add "move from a single column", which moves all the revealed cards from a single column

- [ ] clean up output after game is over
	- [ ] add game over message
- [ ] add undo function