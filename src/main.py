from .game_handler import Game_Handler
from .player import AI_Player, Player
from .board import Board
import json

def main():
    config = load_config()

    board = create_board(config['board'], config['color_values'])
    players = create_players(config['players'], config['color_values'])

    game = Game_Handler(players = players, board = board)

    game.game_loop()

def load_icon(color_config, icon, color_name="white"):
    escape_code = color_config["colors"][color_name].encode('utf-8').decode('unicode_escape')
    reset = color_config["colors"]["reset"].encode('utf-8').decode('unicode_escape')
    return f"{escape_code}{icon}{reset}"

def load_config(file_path = "config.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def create_board(board_config, color_config):
    color = board_config['background_color'] if 'background_color' in board_config else 'white'
    empty_char = load_icon(color_config, board_config['icons']['empty_char'], color)
    h_divider = load_icon(color_config, board_config['icons']['h_divider'], color)
    v_divider = load_icon(color_config, board_config['icons']['v_divider'], color)

    board = Board(
        width = board_config['width'],
        height = board_config['height'],
        num_to_win = board_config['num_to_win'],
        empty_char = empty_char,
        h_divider = h_divider,
        v_divider = v_divider,
    )

    return board

def create_players(players_config, color_config):
    all_player_icons = []

    for each_player_config in players_config:
        color = each_player_config['color'] if 'color' in each_player_config else 'white'
        all_player_icons.append(load_icon(color_config, each_player_config['icon'], color ))

    player = None
    all_players = []
    for i, each_player_config in enumerate(players_config):
        # Prompt for a player's name  if none is found
        if 'name' not in each_player_config:
            name = input(f"Player {i+1}, enter your name: ")
        else:
            name = each_player_config['name']

        # Load colored icons for each player
        if 'color' not in each_player_config:
            color = 'white'
        else:
            color = each_player_config['color']

        colored_icon = load_icon(color_config, each_player_config['icon'], color)

        # Create a player/ai player
        if 'is_ai' in each_player_config and each_player_config["is_ai"]:
            animate = False
            if 'animate' in each_player_config:
                animate = each_player_config['animate']

            player = AI_Player(
                name = name,
                icon = colored_icon,
                opponent_icons = all_player_icons,
                max_search_depth = each_player_config['max_search_depth'],
                animate = animate
            )
        else:
            player = Player(
                name = name,
                icon = colored_icon,
            )
        all_players.append(player)

    return all_players


if __name__ == "__main__":
    main()
