# 2048 AI

Self-playing 2048 game that can constantly hit 2048 or higher utilizing a simple expectimax search. I added in heuristics (smoothness) to the improve performance of the AI, and also used a depth-5 tree to simulate that many steps from any game state in my expectimax algorithm. The base game engine is using the code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). 

![](https://media.giphy.com/media/gF92QHJAuWldZ6a8Mm/giphy.gif)

### Possible Improvements
- This program can 100% use memoization to increase its speed; I'll possibly implement it in the future.
- I can add more heuristics such as monotonicity to make the AI play the game even better.


