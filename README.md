# 2D Board Game with Minimax AI (Python)

## Overview
This is a 2D board game implemented in Python using **pygame**.  
- Player 1 starts with a gem in the top-left corner; Player 2 starts in the bottom-right corner.  
- Players take turns adding gems. Gems overflow to neighbors following specific rules.  
- The game ends when all gems are the same color; the player of that color wins.

## Features
- **Custom overflow logic** to manage gem spreading across the board.  
- **Evaluation function** to score board states for AI decision-making.  
- **Game tree implementation** using a **minimax algorithm** for optimal moves.  
- Supports multiple levels of AI difficulty by adjusting tree depth.

## Highlights
- Designed using object-oriented programming.
- Implemented AI bots using evaluation functions and minimax strategy.
- Demonstrates game logic, algorithms, and Python programming skills.

## Technologies
- **Python 3.x**  
- **pygame** (for graphical interface)  
- **Algorithms:** Game tree, Minimax, Evaluation functions

## How to Run
1. Install pygame: [Pygame Installation](https://www.pygame.org/wiki/GettingStarted)  
2. Run the game:
```bash
python game.py
```

## Contributors

- **Professor Reza Khojasteh** (Instructor, Seneca Polytechnic, DSA456, 2023 Fall)  
- **Di Liu** - [dliu84](https://github.com/dliu84)
- **Henry Luong** - [lluong7](https://github.com/HenryLuong8888)
- **Techatat Obun** - [tobun](https://github.com/Tobun3)

## Citation

If you use this project in your work, please cite it as follows:

> Di Liu (2025). *Python-Board-Game*. GitHub. [https://github.com/dliu84/Python-Board-Game](https://github.com/dliu84/Python-Board-Game)
