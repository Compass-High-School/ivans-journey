# Ivan's Journey: Roadmap 🗺️

**Status:** Proposed. Nothing here is scheduled or approved yet.

**Last updated:** 2026-10-21

This file lists known issues and proposed ideas for Ivan's Journey. It does not describe how the game works today; see the [README](README.md) for that.

## 🎯 Purpose
Ivan's Journey is meant to be silly and fun. Ivan the Gator sneaks past Hall Monitors, collects homework and tries to graduate without landing in summer school.

The game has a second job. It shows students that a game is just code they can read and change, to spark interest in learning to code at Compass. Every level is a list of strings, and settings like walking speed are plain numbers in `main.py`.

**Call-to-action wording:**
*   Point players to **Compass Code**, the school's self-guided coding course.
*   Say "self-guided course", not "coding class", until a real coding elective exists.
*   The course link is not final. Use one placeholder link everywhere until it is picked, so it only has to change once.

## 🐛 Known Issues
Checked against `main.py` on 2026-10-21. Fix the first three before promoting the game more widely, because new players will hit them.

| Issue | What happens | Where |
| :--- | :--- | :--- |
| **Mobile sprint can't work** | `get_active_buttons` reads a single pointer (`pygame.mouse.get_pos()` and `get_pressed()`). One point can't be inside RUN and a D-pad button at the same time, and RUN alone does nothing. The README says RUN sprints. | `TouchController`, `Game.handle_input` |
| **Enter or GO on an end screen skips the title** | After the 1-second lockout, pressing Space, Enter or GO on SUMMER SCHOOL! or YOU GRADUATED! switches to `START_MENU`. `START_MENU` has no lockout and starts a game whenever the action input is down. A normal press lasts longer than one frame, so it starts a new run right away. | `Game.handle_input` |
| **Touch overlay on every screen, including desktop** | `touch_controls.draw()` runs in every state, with no check for a touch screen. The semi-transparent UP button (x 110-175, y 350-415) sits over the bottom-left of each 440px-tall map and clips Ivan's start tile on Levels 3 and 4. A code comment notes the overlap. | `TouchController.__init__`, `Game.draw` |
| **Timer runs on LEVEL COMPLETE** | `get_time_string` counts live in both `PLAYING` and `LEVEL_COMPLETE`, so time spent on the between-level screen is added to the final time. | `Game.get_time_string` |
| **README out of date** | The Pygame CE link (`https://pyga-ce.org/`) does not resolve; the project site is https://pyga.me/. Detentions are called "persistent", but they reset every new run and are never saved. RUN-button sprint is listed (see above). It says Pygbag "compiles" Python to WebAssembly; Pygbag packages the game to run on a WebAssembly build of CPython and pygame-ce. Prerequisites leave out pygbag. | `README.md` |
| **Assets load relative to the working folder** | `load_images` builds paths with `os.path.join("assets", ...)`. Running `python main.py` from anywhere but the repo root silently shows fallback shapes instead of sprites. | `Game.load_images` |
| **Arial in the browser** | Fonts use `pygame.font.SysFont('Arial', ...)`. The browser build probably has no Arial and falls back to pygame's default font, and the ▲▼◀▶ D-pad labels may then render as boxes. Not yet checked in a browser build. | `TouchController.__init__`, `Game.__init__` |
| **CI actions behind** | The workflow uses `actions/checkout@v4`, `actions/setup-python@v4`, `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4`. setup-python, checkout and upload-pages-artifact all have newer major versions. CI only builds and deploys; there are no tests or lint. | `.github/workflows/main.yml` |

### Suggested fixes
*   **Sprint:** make RUN a toggle (tap once to sprint, tap again to walk). That works with one pointer. True multi-touch would need finger events, which should be tested in the browser build first.
*   **End screens:** give `START_MENU` the same 1-second lockout (set `state_timer` when entering it), or wait for the action input to be released.
*   **Overlay:** show the touch controls only after a touch is detected, and test that detection in the browser build. Moving the D-pad fully off the map is harder: the bar under the map is 160px tall, and the D-pad is 225px tall, so it would need smaller buttons or a new layout.
*   **Timer:** pause the clock while `LEVEL_COMPLETE` is showing and resume it on continue.
*   **README:** fix the link, drop "persistent", reword the Pygbag sentence, add pygbag to Prerequisites, and update the sprint text once sprint is fixed.
*   **Assets:** build paths from the folder `main.py` lives in, then confirm the web build still finds them.
*   **Fonts:** bundle an open-license font in `assets/` and load it with `pygame.font.Font`, or draw the D-pad arrows as triangles with `pygame.draw.polygon`.
*   **CI:** bump each action to its current major in one change and confirm the Pages deploy still runs.

### Before promoting
*   Cold-load the live game on a managed student Chromebook and on a phone. The web build downloads its Python runtime when it starts, which could be slow or blocked by school filters.
*   Consider moving the game's green and gold to the school's official colors.

## 💡 Ideas
All proposed. The quick win comes first; the rest follow the priority order from the games and promotion ideas review.

| # | Idea | Size | Needs first |
| :--- | :--- | :--- | :--- |
| 1 | Engine-room line on the graduation screen | XS | Course link |
| 2 | Navigator Levels pack, fed by "Build Ivan a Level" | M | Course module, privacy rules below |
| 3 | Detention Slip and Diploma end screens | S | Nothing |
| 4 | The Teacher's Lounge secret menu | M | Nothing |
| 5 | Remix template and `REMIX.md` | S | Online-safety note |

### 1. Engine-room line on the graduation screen (quick win)
*   Add one line to YOU GRADUATED!: "Every level is just a few lines of text. Want to write one?", plus the Compass Code link.
*   Where: the `VICTORY` block in `Game.draw`. The stats box is 400x80 and already holds two lines, so the new line goes below it.
*   This is the first slice of ideas 3 and 4.

### 2. Navigator Levels pack, fed by "Build Ivan a Level"
A proposed optional Compass Code module has students design a real level as a text grid, using the legend in the README. They give it a silly title ("The Hall Monitor Convention") and run a checker. The best levels ship in a "Navigator Levels" option on the start menu, and each one opens with a credit card: "Level by *first name or nickname*".

**Game-side work:**
*   Move `ALL_LEVELS` into importable Python modules, for example `levels/core.py` (the four current levels) and `levels/navigator.py` (community levels). Plain modules avoid questions about how pygbag loads data files.
*   Add a menu choice on `START_MENU` between the main game and Navigator Levels. Today the start menu only waits for the action input.
*   Show each Navigator level's title and credit before it starts.
*   Add `CREDITS.md` with each level's title and credit line.
*   No extra deploy step: every push to `main` rebuilds and redeploys the game to GitHub Pages.

**Level rules** (what the checker enforces, and what a maintainer checks before merging):
*   At most 20 columns by 11 rows, the size of the 800x440 map area. The current levels are exactly that size.
*   Rectangular, with walls on every edge. Row 0 sits under the HUD bar, so it should stay a wall row.
*   Exactly one `P`, at least one `O` and at least one `H`.
*   Every `H` and at least one door can be reached from `P`. The checker does this with a breadth-first search; students never have to write it.
*   Only letters from the README legend, unless the level ships with new tile logic.
*   Keep `P` out of the bottom-left corner until the touch overlay issue is fixed.

**Later:**
*   "Make it yours" extras for the module: tweak `walk_delay` or `sprint_delay`, or invent a new tile letter (S for a slippery mopped floor) and add its logic.
*   A proposed level-design jam during CS Education Week (around Dec 7-13, 2026; dates to confirm) would ship its winners in this pack. Having the level loader and credit card ready before then is the main deadline.

**How it promotes coding:** the thing students play is the thing they edit. A level is a list of strings, which teaches lists, coordinates and constants without a lecture. Each credit card doubles as an ad: "Think you can make a harder one? Build a level in Compass Code."

### 3. Detention Slip and Diploma end screens
*   **SUMMER SCHOOL!** becomes a pink carbon-copy Detention Slip: a random offense ("Excessive tail swishing", "Sprinting in the hallway while carrying 6 homeworks"), the run time and the detention count, signed "Hall Monitor #3".
*   **YOU GRADUATED!** becomes a diploma: "Bachelor of Sneaking, with Honors (only 2 detentions)". It also shows a personal best time with a NEW RECORD stamp.
*   Both get a small footer: "This game is made in Python at Compass. Learn how: Compass Code", plus a QR code once the link is set.
*   Where: the `GAME_OVER` and `VICTORY` blocks in `Game.draw`. `final_time_str` and `detentions` already exist.
*   Nothing is saved today. Keep the best time in the player's browser storage through pygbag's JavaScript bridge. Test that this works in the web build, and skip the best time if it doesn't. Store only the time.
*   Later, the diploma could show a seasonal code that students enter on the school's student portal for a badge. The code is the same for everyone and carries no personal data.

**How it promotes coding:** a losing screen that's funnier than winning gets screenshotted and shared, and every screenshot carries the footer.

### 4. The Teacher's Lounge (secret cheat menu)
Typing I-V-A-N on the start menu, or tapping the title four times on a touch screen, opens a secret menu. Each silly toggle is labeled with the real variable it changes:

| Toggle | What it changes |
| :--- | :--- |
| Gator Zoom | `sprint_delay`, from 70 down to 10 |
| Hall Monitor Caffeine | `ENEMY_SPEEDS`, from Decaf to Triple Espresso |
| Moonwalk Mode | A new flag |
| Big Head Mode | A new flag |
| Homework Is Optional | The door's homework check; the run ends on "YOU GRADUATED?" |

*   Each toggle has a footnote, for example: "This is `sprint_delay` in `main.py`. In Compass Code you change it for real."
*   Label toggles by variable name, not line number, because line numbers drift.
*   Cheat runs get an asterisk and never count as best times.
*   Today `Game.update` only checks events for `QUIT`, and input is polled with `pygame.key.get_pressed()`. A typed sequence or four taps needs `KEYDOWN` and mouse-button events read in the event loop.
*   Once it ships, the school's student portal can tease it with a rumor: "Ivan's Journey has a secret menu. He answers to his name." Hold the rumor until then.

**How it promotes coding:** it shows that game feel is just numbers you can edit, and it leads straight to the remix guide.

### 5. Remix template and `REMIX.md`
*   Mark the repo as a GitHub Template, so a student can make their own copy in one click and publish it at their own github.io address.
*   Add `REMIX.md` with three silly one-line remixes. Examples: change `sprint_delay` so Ivan zooms, change one letter in a level grid to move a Hall Monitor, or change the "YOU GRADUATED!" text.
*   `REMIX.md` must say that the copy's Pages source has to be set to "GitHub Actions" (Settings > Pages), or the deploy job fails.
*   `REMIX.md` needs an online-safety note before it ships: what to leave off a public site (full names, photos of people, schedules, anything that shows where a student is).
*   An optional `.devcontainer/` could open the copy in a Codespace. pygame can't open a desktop window there, so previews would go through the pygbag web build. Not yet tested.

**How it promotes coding:** a remix is a real first project, and it works as a bonus for the course's Git and publishing modules.

## 🔒 Privacy for Student Contributions
This repo is public. Anything merged here can be seen by anyone, and deleting a file later does not remove it from git history. Check every credit before it merges.

*   **Credits are opt-in.** Use a first name or a chosen nickname only.
*   **No identifying details.** No full names, faces, photos, student IDs, emails or class periods in credits, level titles, offenses or art. Titles and jokes must not name real students or staff.
*   **Consent stays outside the repo.** The teacher collects and keeps consent. The repo only stores the credit line.
*   **Maintainer copies by default.** A maintainer copies a level from the student's private course repo into this one. Students don't open pull requests here from personal GitHub accounts, because that publicly ties their account to the school. A student who wants a public pull request can opt in.
*   **Group totals only.** Any jam or event shows totals such as "levels submitted", never individual rankings.
*   **Keep collecting nothing.** The game sends no player data anywhere today. A best time stays in the player's own browser, and no analytics get added.
