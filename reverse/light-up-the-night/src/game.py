import pygame
import hashlib
from Crypto.Cipher import AES

# Initialize Pygame
pygame.init()

# Define constants
GRID_SIZE = 19  # 19x19 maze
CELL_SIZE = 40  # Size of each cell in pixels
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Colors
colors = {
    'wall': BLACK,
    'path': (92, 91, 91)  # Color for the path
}

# Old maze layout (0 = wall, 1 = path)
maze = [
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
]   

path = [9, 8, 9, 6, 7, 4, 7, 6, 1, 0, 1, 6, 7, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 5, 2, 3, 0, 3, 2, 5, 4, 7, 6, 1, 0, 3, 2, 29, 28, 31, 30, 1, 0, 1, 30, 31, 28, 29, 26, 27, 24]

# Player properties
player_size = 30
player_x, player_y = GRID_SIZE // 2, GRID_SIZE - 1  # Starting at middle bottom of the map
player_color = RED
move_speed = 0.2  # Speed factor for slower movement
lost = False

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Game')

# Function to draw the maze
def draw_maze():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Use the new color for the path
            if maze[row][col] == 1:  # Path cell
                color = colors['path']
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # Draw grid lines only for path cells
                pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                
            else:  # Wall cell
                color = colors['path']  # Wall gets the same color as the path
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # Draw a black cross (straight) on the wall
                pygame.draw.line(screen, BLACK, 
                                 (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), 
                                 ((col + 1) * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), 2)  # Horizontal line
                pygame.draw.line(screen, BLACK, 
                                 (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE), 
                                 (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE), 2)  # Vertical line

                # Fill half of the wall cell black based on neighboring path cells
                if col > 0 and maze[row][col - 1] == 1:  # Path to the left
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE))
                if col < GRID_SIZE - 1 and maze[row][col + 1] == 1:  # Path to the right
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE))
                if row > 0 and maze[row - 1][col] == 1:  # Path above
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE // 2))
                if row < GRID_SIZE - 1 and maze[row + 1][col] == 1:  # Path below
                    pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE // 2))


# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, player_color, (player_x * CELL_SIZE + (CELL_SIZE - player_size) // 2, 
                                            player_y * CELL_SIZE + (CELL_SIZE - player_size) // 2, 
                                            player_size, player_size))
    

def decrypt_flag(key):
    ciphertext = b'\x15zde\xff\x1a\x93\x04\x04\xa9\xe0\x15\xf8\xa99\xe1\x98\xc5L\xcd-\xbeF\xf5O\x03_GdL\x8c\x03\x99O5'
    nonce = b'\x85\xdc\xd8\x18CI\x92\n'
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    flag = cipher.decrypt(ciphertext)
    return flag

# Function to draw the victory message
def draw_victory_message(seen_array):
    font = pygame.font.Font(None, 36)
    text = font.render(decrypt_flag(bytes.fromhex(hashlib.sha3_256(''.join(str(x) for tup in seen_array for x in tup).encode()).hexdigest())), True, (0, 255, 0))  # Green color for the message
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    screen.blit(text, text_rect)

def check_path(player_x, player_y, path, seen_array):
    if ((player_x, player_y) not in seen_array):
        seen_array.append((player_x, player_y))
        if path:
            if (player_x ^ player_y != path.pop()):
                global lost
                lost = True

# Main loop
def main():
    global player_x, player_y
    global lost
    clock = pygame.time.Clock()
    running = True
    cur_path = path.copy()
    seen_array = []

    # Movement delay (to make player slower)
    move_delay = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handling key press events
        keys = pygame.key.get_pressed()

        if move_delay > 0:
            move_delay -= 1  # Delay for movement

        # Apply movement only after some delay (slower movement)
        if move_delay == 0:
            # Check if the player tries to move onto a path (maze value == 1)
            if keys[pygame.K_LEFT] and player_x > 0 and maze[player_y][player_x - 1] == 1:
                player_x -= 1  # Move left
                move_delay = move_speed * 30
                check_path(player_x, player_y, cur_path, seen_array)
            if keys[pygame.K_RIGHT] and player_x < GRID_SIZE - 1 and maze[player_y][player_x + 1] == 1:
                player_x += 1  # Move right
                move_delay = move_speed * 30
                check_path(player_x, player_y, cur_path, seen_array)
            if keys[pygame.K_UP] and player_y > 0 and maze[player_y - 1][player_x] == 1:
                player_y -= 1  # Move up
                move_delay = move_speed * 30
                check_path(player_x, player_y, cur_path, seen_array)
            if keys[pygame.K_DOWN] and player_y < GRID_SIZE - 1 and maze[player_y + 1][player_x] == 1:
                player_y += 1  # Move down
                move_delay = move_speed * 30
                check_path(player_x, player_y, cur_path, seen_array)

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the maze
        draw_maze()

        # Check if the player has reached the end (middle top of the maze) while on path
        if player_x == GRID_SIZE // 2 and player_y == 0 and maze[player_y][player_x] == 1:
            if lost == True:
                player_x, player_y = GRID_SIZE // 2, GRID_SIZE - 1
                lost = False
                cur_path = path.copy()
                seen_array = []
            else:
                draw_victory_message(seen_array)
        else:
            # Draw the player
            draw_player()

        pygame.display.flip()
        clock.tick(30)  # Limit to 30 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()