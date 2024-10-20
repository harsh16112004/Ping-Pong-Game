import pygame
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600  # This will be overridden for fullscreen
FPS = 60

# Define vibrant colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8
PADDLE_SPEED = 5

# Ball speed and acceleration
INITIAL_BALL_SPEED_X, INITIAL_BALL_SPEED_Y = 4, 4
SPEED_INCREMENT = 0.05  # Smaller speed increment for gradual acceleration
MAX_SPEED = 8  # Maximum speed of the ball

# Define win condition score
WINNING_SCORE = 5

# Paddle class
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.color = color  # Assign a color to each paddle

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # Use the paddle's color

# Ball class
class Ball:
    def __init__(self, color):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)
        self.speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))
        self.color = color  # Assign a color to the ball

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        # Start the ball from the center
        self.rect.x = WIDTH // 2 - BALL_RADIUS // 2
        self.rect.y = HEIGHT // 2 - BALL_RADIUS // 2
        self.speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))

    def speed_up(self):
        # Gradually increase speed if it's still under the max limit
        if abs(self.speed_x) < MAX_SPEED:
            self.speed_x *= (1 + SPEED_INCREMENT)
        if abs(self.speed_y) < MAX_SPEED:
            self.speed_y *= (1 + SPEED_INCREMENT)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)  # Use the ball's color

# Function to display buttons and handle pause
def pause_game(screen, font):
    paused = True

    # Draw pause message
    pause_text = font.render("Game Paused", True, WHITE)
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 100))

    # Create buttons (without text)
    menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    # Draw buttons
    pygame.draw.rect(screen, GREEN, menu_button)
    pygame.draw.rect(screen, RED, restart_button)

    # Draw labels for the buttons
    menu_label = font.render("Menu", True, WHITE)
    restart_label = font.render("Restart", True, WHITE)
    screen.blit(menu_label, (menu_button.x + (menu_button.width - menu_label.get_width()) // 2, menu_button.y + 10))
    screen.blit(restart_label, (restart_button.x + (restart_button.width - restart_label.get_width()) // 2, restart_button.y + 10))

    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get the mouse position
                # Check if buttons are clicked
                if menu_button.collidepoint(mouse_pos):
                    return 'menu'
                if restart_button.collidepoint(mouse_pos):
                    return 'restart'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Unpause with ESC key
                    paused = False

        pygame.time.Clock().tick(5)  # Limit loop speed during pause

# Return to the menu function
def return_to_menu():
    pygame.quit()  # Close pygame window
    main()  # Reopen the tkinter menu

# Main game function for multiplayer
def pong_game_multiplayer():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Open game in full screen
    WIDTH, HEIGHT = screen.get_size()  # Get the actual full-screen dimensions
    pygame.display.set_caption('Pong Game - Multiplayer')

    clock = pygame.time.Clock()

    # Create paddles with different colors for two players
    player1 = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, RED)  # Player 1 (Left)
    player2 = Paddle(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE)  # Player 2 (Right)
    ball = Ball(YELLOW)  # Make the ball yellow

    player1_score = 0
    player2_score = 0

    font = pygame.font.Font(None, 74)

    # Start the ball at the center at the beginning
    ball.reset()

    running = True
    while running:
        screen.fill(BLACK)  # Fixed black background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        # Player 1 movement (using 'W' and 'S' keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.move(up=True)
        if keys[pygame.K_s]:
            player1.move(up=False)

        # Player 2 movement (using 'Up' and 'Down' arrow keys)
        if keys[pygame.K_UP]:
            player2.move(up=True)
        if keys[pygame.K_DOWN]:
            player2.move(up=False)

        # Pause the game with ESC key
        if keys[pygame.K_ESCAPE]:
            action = pause_game(screen, font)
            if action == 'menu':
                return_to_menu()
            elif action == 'restart':
                return pong_game_multiplayer()

        # Ball movement and collision with paddles
        ball.move()
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.speed_x *= -1
            ball.speed_up()  # Gradually increase ball speed on paddle hit

        # Check if the ball goes out of bounds
        if ball.rect.left <= 0:  # Player 1 misses
            player2_score += 1
            ball.reset()
        if ball.rect.right >= WIDTH:  # Player 2 misses
            player1_score += 1
            ball.reset()

        # Draw paddles and ball
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)

        # Display the scores with different colors
        player1_text = font.render(str(player1_score), True, GREEN)
        player2_text = font.render(str(player2_score), True, RED)
        screen.blit(player1_text, (WIDTH // 4, 20))
        screen.blit(player2_text, (WIDTH * 3 // 4, 20))

        # Check for win condition
        if player1_score == WINNING_SCORE:
            display_winner("Player 1", screen, font)
            running = False
        elif player2_score == WINNING_SCORE:
            display_winner("Player 2", screen, font)
            running = False

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

# Main game function for playing against AI
def pong_game_ai():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Open game in full screen
    WIDTH, HEIGHT = screen.get_size()  # Get the actual full-screen dimensions
    pygame.display.set_caption('Pong Game - Against AI')

    clock = pygame.time.Clock()

    # Create paddles with different colors
    player1 = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, RED)  # Player 1 (Left)
    ai_player = Paddle(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE)  # AI Player (Right)
    ball = Ball(YELLOW)  # Make the ball yellow

    player1_score = 0
    ai_score = 0

    font = pygame.font.Font(None, 74)

    # Start the ball at the center at the beginning
    ball.reset()

    running = True
    while running:
        screen.fill(BLACK)  # Fixed black background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        # Player 1 movement (using 'W' and 'S' keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.move(up=True)
        if keys[pygame.K_s]:
            player1.move(up=False)

        # AI movement
        if ai_player.rect.centery < ball.rect.centery:
            ai_player.move(up=False)
        elif ai_player.rect.centery > ball.rect.centery:
            ai_player.move(up=True)

        # Pause the game with ESC key
        if keys[pygame.K_ESCAPE]:
            action = pause_game(screen, font)
            if action == 'menu':
                return_to_menu()
            elif action == 'restart':
                return pong_game_ai()

        # Ball movement and collision with paddles
        ball.move()
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(ai_player.rect):
            ball.speed_x *= -1
            ball.speed_up()  # Gradually increase ball speed on paddle hit

        # Check if the ball goes out of bounds
        if ball.rect.left <= 0:  # Player 1 misses
            ai_score += 1
            ball.reset()
        if ball.rect.right >= WIDTH:  # AI misses
            player1_score += 1
            ball.reset()

        # Draw paddles and ball
        player1.draw(screen)
        ai_player.draw(screen)
        ball.draw(screen)

        # Display the scores with different colors
        player1_text = font.render(str(player1_score), True, GREEN)
        ai_text = font.render(str(ai_score), True, RED)
        screen.blit(player1_text, (WIDTH // 4, 20))
        screen.blit(ai_text, (WIDTH * 3 // 4, 20))

        # Check for win condition
        if player1_score == WINNING_SCORE:
            display_winner("Player 1", screen, font)
            running = False
        elif ai_score == WINNING_SCORE:
            display_winner("AI Player", screen, font)
            running = False

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

# Display winner and restart the game or quit
def display_winner(winner, screen, font):
    screen.fill(BLACK)
    text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Pause for 1 second to show the winner
    
    # Show restart and quit options using tkinter
    show_restart_menu()

# Function to handle restart or quit
def show_restart_menu():
    restart_window = tk.Tk()
    restart_window.title("Game Over")
    restart_window.geometry("300x200")

    label = tk.Label(restart_window, text="Game Over! What do you want to do?", font=("Helvetica", 12))
    label.pack(pady=20)

    restart_button = tk.Button(restart_window, text="Restart", width=15, height=2, bg="#32CD32", fg="white",
                               font=("Helvetica", 12), command=lambda: [restart_window.destroy(), main()])
    restart_button.pack(pady=10)

    quit_button = tk.Button(restart_window, text="Quit", width=15, height=2, bg="#FF6347", fg="white",
                            font=("Helvetica", 12), command=restart_window.quit)
    quit_button.pack(pady=10)

    restart_window.mainloop()

# GUI setup using tkinter
class PongGUI:
    def __init__(self, root):
        self.root = root
        root.title("Pong Game")
        root.geometry("400x300")

        # Load the background image
        self.bg_image = Image.open("wallpaperflare.com_wallpaper.jpg")  # Replace with your image file path
        self.bg_image = self.bg_image.resize((1700, 1000), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label with the background image
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Set the label to cover the entire window

        # Create colorful GUI widgets (place them on top of the background)
        self.start_multiplayer_button = tk.Button(root, text="Start Multiplayer Game", command=self.start_multiplayer_game, 
                                                  width=20, height=2, bg="#32CD32", fg="white", font=("Helvetica", 14, "bold"))  # Lime green button
        self.start_ai_button = tk.Button(root, text="Start Game vs AI", command=self.start_ai_game, 
                                         width=20, height=2, bg="#FFA500", fg="white", font=("Helvetica", 14, "bold"))  # Orange button
        self.quit_button = tk.Button(root, text="Quit", command=self.quit_game, 
                                     width=20, height=2, bg="#FF6347", fg="white", font=("Helvetica", 14, "bold"))  # Tomato button

        # Place buttons on top of the background image (use pack or place as required)
        self.start_multiplayer_button.pack(pady=20)
        self.start_ai_button.pack(pady=20)
        self.quit_button.pack(pady=20)

    def start_multiplayer_game(self):
        messagebox.showinfo("Pong", "Starting the Multiplayer Pong game!")
        self.root.destroy()  # Close the menu window
        pong_game_multiplayer()  # Start the multiplayer pong game using pygame

    def start_ai_game(self):
        messagebox.showinfo("Pong", "Starting the Pong game vs AI!")
        self.root.destroy()  # Close the menu window
        pong_game_ai()  # Start the pong game against AI using pygame

    def quit_game(self):
        self.root.quit()

# Main function to run the GUI
def main():
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Make the window full screen
    gui = PongGUI(root)
    
    # Allow user to exit full screen with 'Escape' key
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
    
    root.mainloop()

if __name__ == "__main__":
    main()
