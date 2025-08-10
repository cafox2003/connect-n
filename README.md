# connect-n
A highly configureable connect4-like CLI game

## Getting Started
---

### Playing the game
1. Install Python 3.x
2. Clone the repository: 
```bash
https://github.com/cafox2003/connect-n.git
cd connect-n
```
3. Run the program
    To run the program with the default config: `python -m src.main`
    You can also pass a cli argument for a custom config: `python -m src.main your-config.json`

### Config options
This JSON file configures game settings, players, and colors. The [default configuration](config.json) contains an example of all options being used to create a standard connect 4 game against a single AI opponent.

#### `board`
Configures the board's apperance, size, and rules
Options:
- **width** (int): number of columns in the board
- **height** (int): number of rows in the board
- **num_to_win** (int): number of consecutive pieces required to win
- **icons** (object): Characters used to draw the following board elements:
    - **empty_char** (string): Character to represent empty spaces ("_")
    - **v_divider** (string): Character to represent vertical dividers ("|")
    - **h_divider** (string): Character to represent horizontal dividers ("-")
- (optional) **color** (string): color of the board, must match a key in `color_values.colors`. If not set, it defaults to white

#### `players`
An array of player configurations. Each player object can contain:

- **name** (string, optional): Player's display name. If not configured, user will be prompted to enter a name prior to the start of the game
- **icon** (string): The icon that represent's a character's piece. 
- **color** (string, optional): color of the character's piece, must match a key in `color_values.colors`. If not set, defaults to white.
- **is_ai** (boolean, optiona): Set to true if player is controlled by AI
- **max_search_depth** (int, optional): For AI players, this controls how deep the search will go. Smaller values will make AI opponents easier, while higher values will make AI opponents harder. Note that higher values may cause the program to crash.
- **animate** (boolean, optiona) If `true`, the AI player's search is shown as it "thinks" about moves.
> Note: Each player must have a unique icon-color combination. Multiple players can share an icon, or a color, but no two players can have the same icon AND color

#### `color values`
Defines ansi color codes to be used in the game

- **colors** (object): Maps color names to their ANSI escape sequences.
    - Example: `"red": "\\033[31m"`
- **reset** (string): ANSI escape code to reset color

