import os
import json

from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin


### API FOR DEVELOPERS ###


# Permissions Manager
class PermissionsManager:
    """
    The PermissionsManager class is an API for developers to easily manage permissions through **EasyAsPermissions**.

    ### Arguments
    - `plugin` (Plugin) - *Your plugin.*

    ### Example
    ```python
    from endstone_easyaspermissions import PermissionsManager

    class MyPlugin(Plugin):
        manager = PermissionsManager(self)

        ## Create Permission ##
        def example_create_permission(self: Plugin, player: Player):
            manager.permissions.set_permission(
                "example.permission", "Example permission.", "op"
            )
            player.send_message("Permission created.")

    ```

    ```python

            ## Add Permission to Player ##
            def example_add_permission(self: Plugin, player: Player):
                manager.players.add_permission_to_player(player, "example.permission")
                player.send_message("Permission added to player.")

    ```

    ```python

            ## Role Example ##
            def example_role(self: Plugin, player: Player):
                manager.roles.set_role("newrole", [], ["Vincent"])
                manager.roles.add_permission_to_role("newrole", "example.permission")
                manager.players.add_role_to_player(player, "newrole")
                player.send_message("Role added to player.")

    ```
    """

    def __init__(self, plugin: Plugin):
        self._plugin: Plugin = plugin
        self._eap: Plugin = plugin.server.plugin_manager.get_plugin("EasyAsPermissions")
        self.players = self.PlayerManager(self)
        self.permissions = self.PermManager(self)
        self.roles = self.RoleManager(self)

    class PlayerManager:
        def __init__(self, permissions_manager):
            self._plugin: Plugin = permissions_manager.plugin
            self.manager: PermissionsManager = permissions_manager

        def add_permission_to_player(self, player: Player, permission: str):
            player.add_attachment(self._eap, permission, True)

        def remove_permission_from_player(self, player: Player, permission: str):
            player.add_attachment(self._eap, permission, False)

        def add_role_to_player(self, player: Player, role: str):
            permissionsData = read_permissions_config()
            permissionsData["roles"][role]["players"].append(player.name)
            role = permissionsData["roles"][role]
            for permission in role["permissions"]:
                self.add_permission_to_player(self._eap, player, permission)
            write_permissions_config(permissionsData)

        def remove_role_from_player(self, player: Player, role: str):
            permissionsData = read_permissions_config()
            permissionsData["roles"][role]["players"].remove(player.name)
            role = permissionsData["roles"][role]
            for permission in role["permissions"]:
                self.remove_permission_from_player(self._eap, player, permission)
            write_permissions_config(permissionsData)

    class PermManager:
        def __init__(self, permissions_manager):
            self._plugin: Plugin = permissions_manager.plugin
            self.manager: PermissionsManager = permissions_manager

        def set_permission(
            self,
            name: str,
            description: str = "New permission.",
            default: str = "op",
        ):
            permissionData = read_permissions_config()
            permissionData["permissions"][name] = {
                "description": description,
                "default": default,
            }
            write_permissions_config(permissionData)
            self._plugin.logger(
                "§c[EAC] §rPermission §a'§f{name}§a' §rhas been registered."
            )

        def delete_permission(self, name: str):
            permissionData = read_permissions_config()
            permissionData["permissions"].pop(name)
            write_permissions_config(permissionData)
            self._plugin.logger(
                "§c[EAC] §rPermission §a'§f{name}§a' §rhas been deleted."
            )

    class RoleManager:
        def __init__(self, permissions_manager):
            self._plugin: Plugin = permissions_manager.plugin
            self.manager: PermissionsManager = permissions_manager

        def set_role(
            self, name: str, permissions: list[str] = [], players: list[str] = []
        ):
            permissionData = read_permissions_config()
            permissionData["roles"][name] = {
                "permissions": permissions,
                "players": players,
            }
            write_permissions_config(permissionData)
            self._plugin.logger("§c[EAC] §rRole §a'§f{name}§a' §rhas been registered.")

        def delete_role(self, name: str):
            permissionData = read_permissions_config()
            permissionData["roles"].pop(name)
            write_permissions_config(permissionData)
            self._plugin.logger("§c[EAC] §rRole §a'§f{name}§a' §rhas been deleted.")

        def add_permission_to_role(self, role: str, permission: str):
            permissionData = read_permissions_config()
            permissionData["roles"][role]["permissions"].append(permission)
            write_permissions_config(permissionData)

        def remove_permission_from_role(self, role: str, permission: str):
            permissionData = read_permissions_config()
            permissionData["roles"][role]["permissions"].remove(permission)
            write_permissions_config(permissionData)


### PERMISSIONS CONFIGURATION MANAGEMENT ###


# Define the path to the JSON file
json_file_path = os.path.abspath("./config/permissions_manager.json")


# Function to read from the JSON file
def read_permissions_config():
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(
            f"Error: Permissions configuration file is missing; please reload once EAC has generated one."
        )
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_file_path}.")
        return {}


# Function to write to the JSON file
def write_permissions_config(data):
    try:
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        global permissionsData
        permissionsData = data
    except IOError as e:
        print(f"Error: Failed to write to {json_file_path}\n{e}")
