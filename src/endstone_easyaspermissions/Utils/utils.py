### CHAT CONFIGURATION ###

import json
import os
import re
from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin


prefix = "§l§f[§aEA§cP§f]§r >> "


def send_custom(player: Player, message: str):
    player.send_message(prefix + message)


def error_custom(player: Player, message: str):
    player.send_message(prefix + "§cError: " + message)


### DEFAULT PERMISSIONS DATA CONFIGURATION ###

default_data = {
    "permissions": {
        "easyas.permission.example": {
            "description": "Example permission.",
            "default": "all",
        }
    },
    "roles": {
        "example": {
            "permissions": ["easyas.permission.example"],
            "players": ["Vincent"],
        }
    },
}

### PERMISSIONS CONFIGURATION MANAGEMENT ###

# Define the path to the JSON file
json_file_path = os.path.abspath("./config/permissions_manager.json")


class logger:
    def info(str: str):
        print(str)

    def error(str: str):
        print(str)


# Function to read from the JSON file
def read_permissions_config():
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.error(
            f"Error: Missing permissions configuration file, generating a new one."
        )
        write_permissions_config(default_data)
        return default_data
    except json.JSONDecodeError:
        logger.error(f"Error: Failed to decode JSON from {json_file_path}.")
        return {}


# Function to write to the JSON file
def write_permissions_config(data):
    try:
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        global permissionsData
        permissionsData = data
    except IOError as e:
        logger.error(f"Error: Failed to write to {json_file_path}\n{e}")


def reset_permissions(self: Plugin, player: Player):
    write_permissions_config(default_data)
    global permissionsData
    permissionsData = default_data
    self.logger.info("Permissions configuration has been reset to default.")
    send_custom(
        player,
        f"§cReset Complete!\n§eServer has been reloaded successfully!",
    )
    try:
        self.server.reload()
    except Exception as e:
        error_custom(player, f"Failed to reload server: {e}")
        return


### EXTRA UTILITIES ###


def strip_color_codes(text: str) -> str:
    # Regular expression to match Minecraft color codes
    color_code_pattern = re.compile(r"§[0-9a-fk-or]")
    # Substitute the color codes with an empty string
    return color_code_pattern.sub("", text)
