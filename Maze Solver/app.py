import matplotlib.pyplot as plt
import random

def generate_random_maze(rows, cols, wall_chance=0.25):
    """Generates a random maze."""
    maze = []
    for r in range(rows):
        row_data = []
        for c in range(cols):
            if random.random() < wall_chance:
                row_data.append(1)  # Wall
            else:
                row_data.append(0)  # Path
        maze.append(row_data)
    
    # Force Start and End to be open
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0
    return maze

def is_safe(maze, row, col):
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0

def solve_maze(maze, start, end):
    """Standard DFS to find the path."""
    path = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited: return False
        visited.add((row, col))
        path.append((row, col))

        if (row, col) == end: return True

        # Randomize directions for variety
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_safe(maze, new_row, new_col):
                if dfs(new_row, new_col): return True
        
        path.pop()
        return False

    if dfs(start[0], start[1]):
        return path
    else:
        return None

def animate_solution(maze, path, start, end):
    """Animates the path movement step-by-step."""
    nrows, ncols = len(maze), len(maze[0])
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 1. Draw the Base Maze
    ax.imshow(maze, cmap="binary")
    
    # Setup Grid
    ax.set_xticks([x - 0.5 for x in range(1, ncols)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, nrows)], minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=2)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax.set_title("Maze Animation (Green=Start, Blue=End)")

    # 2. Mark Initial (Start) and Final (End) Positions
    # Green Square for Start
    ax.add_patch(plt.Rectangle((start[1]-0.4, start[0]-0.4), 0.8, 0.8, color='limegreen', label='Start'))
    ax.text(start[1], start[0], 'S', color='white', ha='center', va='center', fontweight='bold')
    
    # Blue Square for End
    ax.add_patch(plt.Rectangle((end[1]-0.4, end[0]-0.4), 0.8, 0.8, color='blue', label='End'))
    ax.text(end[1], end[0], 'E', color='white', ha='center', va='center', fontweight='bold')

    plt.draw() # Draw the initial setup
    
    # 3. Animate the Movement
    if path:
        print("Animating path...")
        for i, (row, col) in enumerate(path):
            # Skip drawing over the Start/End markers specifically to keep them visible
            if (row, col) == start or (row, col) == end:
                continue
                
            # Draw the red movement dot
            circle = plt.Circle((col, row), 0.3, color='red')
            ax.add_patch(circle)
            
            # Refresh the plot to show movement
            plt.draw()
            plt.pause(0.3)  # <--- Controls speed (0.3 seconds per step)
    
    plt.show()

def main():
    rows, cols = 8, 8  # Made slightly larger for better animation
    maze = generate_random_maze(rows, cols, wall_chance=0.25)
    start = (0, 0)
    end = (rows-1, cols-1)

    print("Solving maze...")
    path = solve_maze(maze, start, end)

    if path:
        print(f"Path found with {len(path)} steps!")
        animate_solution(maze, path, start, end)
    else:
        print("No path found! (Random walls blocked the way). Try running again.")

if __name__ == "__main__":
    main()