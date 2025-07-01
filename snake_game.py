#!/usr/bin/env python3
"""
Terminal Snake Game
A classic snake game that runs in the terminal using curses.

Controls:
- Arrow keys or WASD to move
- Q to quit
- P to pause/unpause

Author: AI Assistant
"""

import curses
import random
import time
from enum import Enum
from collections import deque


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_screen()
        self.reset_game()
        
    def setup_screen(self):
        """Initialize the game screen and settings."""
        # Hide cursor
        curses.curs_set(0)
        
        # Enable keypad mode for arrow keys
        self.stdscr.keypad(True)
        
        # Set non-blocking input with timeout
        self.stdscr.timeout(100)  # 100ms timeout
        
        # Get screen dimensions
        self.height, self.width = self.stdscr.getmaxyx()
        
        # Define game area (leave space for borders and UI)
        self.game_height = self.height - 4
        self.game_width = self.width - 4
        self.start_row = 2
        self.start_col = 2
        
        # Initialize colors if supported
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Border
            
    def reset_game(self):
        """Reset the game to initial state."""
        # Snake starts in the middle of the screen
        start_row = self.game_height // 2
        start_col = self.game_width // 2
        
        # Snake body (head first)
        self.snake = deque([
            (start_row, start_col),
            (start_row, start_col - 1),
            (start_row, start_col - 2)
        ])
        
        # Initial direction
        self.direction = Direction.RIGHT
        
        # Score
        self.score = 0
        
        # Game state
        self.game_over = False
        self.paused = False
        
        # Generate first food
        self.generate_food()
        
    def generate_food(self):
        """Generate food at a random location not occupied by snake."""
        while True:
            food_row = random.randint(0, self.game_height - 1)
            food_col = random.randint(0, self.game_width - 1)
            
            if (food_row, food_col) not in self.snake:
                self.food = (food_row, food_col)
                break
                
    def handle_input(self):
        """Handle user input."""
        try:
            key = self.stdscr.getch()
        except:
            return
            
        if key == -1:  # No input
            return
            
        # Quit game
        if key in [ord('q'), ord('Q')]:
            self.game_over = True
            return
            
        # Pause/unpause
        if key in [ord('p'), ord('P')]:
            self.paused = not self.paused
            return
            
        if self.paused:
            return
            
        # Movement controls
        new_direction = None
        
        # Arrow keys
        if key == curses.KEY_UP:
            new_direction = Direction.UP
        elif key == curses.KEY_DOWN:
            new_direction = Direction.DOWN
        elif key == curses.KEY_LEFT:
            new_direction = Direction.LEFT
        elif key == curses.KEY_RIGHT:
            new_direction = Direction.RIGHT
            
        # WASD keys
        elif key in [ord('w'), ord('W')]:
            new_direction = Direction.UP
        elif key in [ord('s'), ord('S')]:
            new_direction = Direction.DOWN
        elif key in [ord('a'), ord('A')]:
            new_direction = Direction.LEFT
        elif key in [ord('d'), ord('D')]:
            new_direction = Direction.RIGHT
            
        # Prevent snake from going backwards into itself
        if new_direction and self.is_valid_direction(new_direction):
            self.direction = new_direction
            
    def is_valid_direction(self, new_direction):
        """Check if the new direction is valid (not opposite to current)."""
        current = self.direction
        
        # Can't go in opposite direction
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        return new_direction != opposite_directions[current]
        
    def update_game(self):
        """Update game state."""
        if self.game_over or self.paused:
            return
            
        # Calculate new head position
        head_row, head_col = self.snake[0]
        dir_row, dir_col = self.direction.value
        new_head = (head_row + dir_row, head_col + dir_col)
        
        # Check collisions
        if self.check_collision(new_head):
            self.game_over = True
            return
            
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 10
            self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
    def check_collision(self, position):
        """Check if position collides with walls or snake body."""
        row, col = position
        
        # Wall collision
        if (row < 0 or row >= self.game_height or 
            col < 0 or col >= self.game_width):
            return True
            
        # Self collision
        if position in self.snake:
            return True
            
        return False
        
    def draw_game(self):
        """Draw the game on screen."""
        self.stdscr.clear()
        
        # Draw border
        self.draw_border()
        
        # Draw snake
        self.draw_snake()
        
        # Draw food
        self.draw_food()
        
        # Draw UI
        self.draw_ui()
        
        # Refresh screen
        self.stdscr.refresh()
        
    def draw_border(self):
        """Draw game border."""
        color = curses.color_pair(4) if curses.has_colors() else 0
        
        # Top and bottom borders
        for col in range(self.width):
            self.stdscr.addch(0, col, '-', color)
            self.stdscr.addch(self.height - 2, col, '-', color)
            
        # Left and right borders
        for row in range(self.height - 1):
            self.stdscr.addch(row, 0, '|', color)
            self.stdscr.addch(row, self.width - 1, '|', color)
            
        # Corners
        self.stdscr.addch(0, 0, '+', color)
        self.stdscr.addch(0, self.width - 1, '+', color)
        self.stdscr.addch(self.height - 2, 0, '+', color)
        self.stdscr.addch(self.height - 2, self.width - 1, '+', color)
        
    def draw_snake(self):
        """Draw the snake."""
        color = curses.color_pair(1) if curses.has_colors() else 0
        
        for i, (row, col) in enumerate(self.snake):
            screen_row = row + self.start_row
            screen_col = col + self.start_col
            
            if i == 0:  # Head
                char = '@'
            else:  # Body
                char = '#'
                
            try:
                self.stdscr.addch(screen_row, screen_col, char, color)
            except curses.error:
                pass  # Ignore if we can't draw at edge
                
    def draw_food(self):
        """Draw the food."""
        color = curses.color_pair(2) if curses.has_colors() else 0
        
        food_row, food_col = self.food
        screen_row = food_row + self.start_row
        screen_col = food_col + self.start_col
        
        try:
            self.stdscr.addch(screen_row, screen_col, '*', color)
        except curses.error:
            pass
            
    def draw_ui(self):
        """Draw user interface elements."""
        color = curses.color_pair(3) if curses.has_colors() else 0
        
        # Score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(self.height - 1, 2, score_text, color)
        
        # Controls
        controls = "Controls: Arrow keys/WASD=Move, P=Pause, Q=Quit"
        if len(controls) < self.width - 4:
            self.stdscr.addstr(self.height - 1, self.width - len(controls) - 2, controls)
        
        # Game state messages
        if self.paused:
            msg = "PAUSED - Press P to continue"
            start_col = (self.width - len(msg)) // 2
            self.stdscr.addstr(1, start_col, msg, curses.A_BLINK)
            
        if self.game_over:
            msg = f"GAME OVER! Final Score: {self.score} - Press Q to quit"
            start_col = (self.width - len(msg)) // 2
            try:
                self.stdscr.addstr(1, start_col, msg, curses.A_BLINK | color)
            except curses.error:
                pass
                
    def run(self):
        """Main game loop."""
        while not self.game_over:
            self.handle_input()
            self.update_game()
            self.draw_game()
            
        # Game over screen
        while True:
            key = self.stdscr.getch()
            if key in [ord('q'), ord('Q')]:
                break
            self.draw_game()


def main(stdscr):
    """Main function to run the game."""
    try:
        game = SnakeGame(stdscr)
        game.run()
    except KeyboardInterrupt:
        pass  # Allow Ctrl+C to exit gracefully


if __name__ == "__main__":
    # Check terminal size
    import os
    try:
        size = os.get_terminal_size()
        if size.columns < 40 or size.lines < 10:
            print("Terminal too small! Please resize to at least 40x10 characters.")
            exit(1)
    except:
        pass  # Can't check size, proceed anyway
        
    print("Starting Snake Game...")
    print("Use arrow keys or WASD to move, P to pause, Q to quit.")
    print("Press any key to start...")
    input()
    
    # Start the game
    curses.wrapper(main)
