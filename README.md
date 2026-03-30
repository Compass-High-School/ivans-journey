# Compass High: Ivan's Journey 🎓

Welcome to **Ivan's Journey**, a 2D stealth-adventure game built for Compass High School! 

**[➡️ CLICK HERE TO PLAY NOW! ⬅️](https://compass-high-school.github.io/ivans-journey)**

## 📖 Overview
Help Ivan navigate the treacherous hallways of Compass High! Your goal is to collect all the missing homework assignments without getting caught by the Hall Monitors. Can you graduate with a perfect record?

## 🎮 Controls
### Keyboard
*   **Arrow Keys:** Move Ivan
*   **Shift:** Sprint (Faster movement, but harder to control!)
*   **Space / Enter:** Start Game / Next Level / Restart

### Touch (Mobile)
*   **D-Pad (Arrows):** Move Ivan
*   **RUN Button:** Sprint
*   **GO Button:** Action (Start/Next)

## 🚀 Getting Started
### Prerequisites
*   Python 3.11 or higher
*   [Pygame CE](https://pyga.me/)

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/compass-high-school/ivans-journey.git
    cd ivans-journey
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the game:
    ```bash
    python main.py
    ```

## 🛠️ Technical Architecture
The game is built using **Pygame CE** and designed to be compatible with **Pygbag** for web deployment.

### Key Classes
*   **`Game`**: The central engine that manages game states (`START_MENU`, `PLAYING`, `LEVEL_COMPLETE`, `GAME_OVER`, `VICTORY`), level loading, collision detection, and the main loop.
*   **`Player`**: Handles player movement and wall collisions.
*   **`Enemy`**: Manages patrol logic for hall monitors (both horizontal and vertical).
*   **`TouchController`**: Renders and processes input for on-screen controls, enabling mobile playability.

### Async Main Loop
The `run()` method in the `Game` class is an `async` function. This is a requirement for `pygbag` to keep the browser tab responsive while running the Python loop.

## 🏗️ How to Customize
### Adding or Modifying Levels
Levels are stored in `main.py` as lists of strings in the `ALL_LEVELS` list. You can create new maps using the following characters:

| Character | Description |
| :--- | :--- |
| `W` | **Wall**: Solid obstacle. |
| `D` | **Desk**: Solid obstacle (uses desk asset). |
| `P` | **Player**: Ivan's starting position. |
| `O` | **Goal**: The exit door (unlocks after all homework is collected). |
| `H` | **Homework**: Collectible items. |
| `E` | **Enemy (Vertical)**: Patrols up and down. |
| `R` | **Enemy (Horizontal)**: Patrols left and right. |
| `.` | **Floor**: Walkable space. |

### Updating Assets
Graphics are located in the `assets/` directory. You can replace them with your own `.png` files, but ensure they keep the same filenames:
*   `player.png`, `enemy.png`, `wall.png`, `floor.png`, `desk.png`, `door.png`, `homework.png`, `heart.png`, `compass.png`.

### Adjusting Difficulty
You can tweak the following variables in `main.py`:
*   `self.walk_delay` / `self.sprint_delay`: Controls how fast the player moves (lower is faster).
*   `spd = random.choice([0.8, 1.0, 1.2, 1.5])`: Modify these values in `load_level` to change enemy patrol speeds.
*   `self.lives`: Change the number of chances Ivan gets per level.

## 🌐 Web Deployment
This project uses **Pygbag** to compile Python code into WebAssembly (WASM).

### Build Locally
To test the web build locally:
```bash
pygbag main.py
```
This will start a local server, usually at `http://localhost:8000`.

### Automatic Deployment
Any push to the `main` branch automatically triggers a GitHub Action (`.github/workflows/main.yml`) that builds the project and deploys it to GitHub Pages.

## 🛠️ Built With
*   [Python 3.12](https://www.python.org/)
*   [Pygame CE](https://pyga-ce.org/)
*   [Pygbag](https://github.com/pygame-web/pygbag)
