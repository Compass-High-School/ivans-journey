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

## ✨ Game Features
*   **Direction Arrow:** A **GOLD** line points from Ivan toward the nearest homework assignment, helping you navigate the levels efficiently.
*   **Sprinting Mechanic:** Hold **Shift** (or the **RUN** button) to reduce movement delay from 150ms to 70ms. Use it to dodge hall monitors!
*   **Lives & Detentions:** Ivan starts each level with **3 lives**. Getting caught by a Hall Monitor sends you back to the start and adds to your persistent **Detention** count.
*   **Victory Celebration:** Graduating triggers a celebratory confetti effect featuring Compass High's colors and logos.

## 🗺️ Level Overview
The game features four distinct levels, each with increasing complexity:
1.  **Level 1: Hallway** - A basic introduction to movement and avoiding patrols.
2.  **Level 2: Classrooms** - Navigate through rows of desks and tight corners.
3.  **Level 3: Cafeteria** - A more open area with multiple patrol routes.
4.  **Level 4: Ceremony** - The final challenge before graduation!

## 🚀 Getting Started
### Prerequisites
*   Python 3.11 or higher
*   [Pygame CE](https://pyga-ce.org/)

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

### State Management
The game uses a state machine to manage transitions:
*   `START_MENU`: The title screen.
*   `PLAYING`: Active gameplay.
*   `LEVEL_COMPLETE`: Transition between levels.
*   `GAME_OVER`: Triggered when Ivan runs out of lives.
*   `VICTORY`: The graduation screen.

### HUD (Heads-Up Display)
The top bar provides real-time feedback:
*   **Hearts:** Current lives remaining in the level.
*   **Message Center:** Tracks homework collection progress and status updates.
*   **Timer:** Tracks how long it takes Ivan to complete his journey.

### Async Main Loop
The `run()` method in the `Game` class is an `async` function. This is a requirement for `pygbag` to keep the browser tab responsive while running the Python loop in WebAssembly.

## 🖼️ Asset Reference
Assets are located in the `assets/` directory:
*   `player.png`: Ivan's character sprite.
*   `enemy.png`: The Hall Monitor/Enemy sprite.
*   `homework.png`: Collectible homework assignments.
*   `door.png`: The goal/exit for each level.
*   `wall.png` / `floor.png` / `desk.png`: Environmental tiles.
*   `heart.png`: Represents Ivan's lives in the HUD.
*   `compass.png`: The Compass High logo used in effects.

## 🏗️ How to Customize
### Adding or Modifying Levels
Levels are stored in `main.py` as lists of strings in the `ALL_LEVELS` list. You can create a new level by defining a grid:

```python
NEW_LEVEL = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W.P................W",
    "W.......H..........W",
    "W.........E........W",
    "W................O.W",
    "WWWWWWWWWWWWWWWWWWWW",
]
ALL_LEVELS.append(NEW_LEVEL)
```

**Character Legend:**
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

### Adjusting Game Constants
In `main.py`, you can modify these values to change the feel of the game:
*   `FPS`: Default is `60`.
*   `TILE_SIZE`: Default is `40`.
*   `self.walk_delay`: Player movement delay in ms (Default: `150`).
*   `self.sprint_delay`: Sprinting delay in ms (Default: `70`).

## 🌐 Web Deployment
This project uses **Pygbag** to compile Python code into WebAssembly (WASM).

### Build Locally
To test the web build locally:
```bash
pygbag main.py
```
This starts a local server at `http://localhost:8000`.

### Automatic Deployment
Any push to the `main` branch automatically triggers a GitHub Action (`.github/workflows/main.yml`) that builds the project and deploys it to GitHub Pages.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
