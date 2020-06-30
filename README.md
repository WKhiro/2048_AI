# 2048 AI

Self-playing 2048 game that can constantly hit 2048 or higher utilizing a simple expectimax search. I added in heuristics (smoothness) to the improve performance of the AI, and also used a depth-5 tree to simulate that many steps from any game state in my expectimax algorithm. The base game engine is using the code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). Pygame is required to run the program. 

<p align="center">
  <img src="https://media.giphy.com/media/gF92QHJAuWldZ6a8Mm/giphy.gif" alt=""/>
</p>

### Keyboard Controls
- **Enter** toggles on/off the AI autoplay functionality, and allows the user to play the game starting at the current game state, if desired.
- **Arrow keys** allow the user to move the tiles around in their respective directions during manual play.
- **r** restarts the game.
- **u** undos the last made move.
- **s** stores a snapshot (write to a save file) of the current game state.
- **l** loads in the saved game state.

### Possible Improvements
- This program can 100% use memoization to increase its speed; I'll possibly implement it in the future.
- I can add more heuristics such as monotonicity to make the AI play the game even better.

