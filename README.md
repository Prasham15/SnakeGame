# Terminal Snake Game

A classic Snake game implementation that runs directly in your terminal using Python and curses.

## Features

- 🐍 Classic snake gameplay
- 🎮 Multiple control schemes (Arrow keys or WASD)
- 🎨 Colorized graphics (if terminal supports colors)
- ⏸️ Pause/resume functionality
- 📊 Score tracking
- 🖥️ Cross-platform terminal support

## Requirements

- Python 3.6+
- `windows-curses` package (for Windows users)

## Installation

1. Clone or download this repository
2. If on Windows, install the required package:
   ```bash
   pip install windows-curses
   ```

## How to Play

1. Run the game:
   ```bash
   python snake_game.py
   ```

2. Controls:
   - **Arrow Keys** or **WASD**: Move the snake
   - **P**: Pause/unpause the game
   - **Q**: Quit the game

3. Objective:
   - Eat the food (*) to grow and increase your score
   - Avoid hitting the walls or your own body
   - Try to achieve the highest score possible!

## Game Elements
![image](https://github.com/user-attachments/assets/8f1f0814-7da5-406f-9064-1e6f03543321)

- `@` - Snake head
- `#` - Snake body
- `*` - Food
- Score increases by 10 points for each food eaten

## Technical Details

- Built with Python's `curses` library for terminal manipulation
- Uses non-blocking input for smooth gameplay
- Implements collision detection and game state management
- Supports terminal resizing and color detection

## Author

Created with AI assistance for educational and entertainment purposes.

Enjoy the game! 🎮🐍
