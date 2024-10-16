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
    from .eap_api.py import PermissionsManager

    class MyPlugin(Plugin):
        manager = PermissionsManager(self)

        ## Registering Permissions ##
        def example_create_permission(self: Plugin, player: Player):
            manager.permissions.set_permission(
                "example.permission", "Example permission.", "op"
            )
            player.send_message("Permission created.")

    ```

    ```python

            ## Adding Permissions to Players ##
            def example_add_permission(self: Plugin, player: Player):
                manager.players.add_permission_to_player(player, "example.permission")
                player.send_message("Permission added to player.")

    ```

    ```python

            ## Using Roles ##
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
        """
        Contains player-based permission methods.
        """
        self.permissions = self.PermManager(self)
        """
        Contains methods for managing permissions.
        """
        self.roles = self.RoleManager(self)
        """
        Contains methods for managing roles.
        """

    class PlayerManager:
        def __init__(self, permissions_manager):
            self._plugin: Plugin = permissions_manager.plugin
            self.manager: PermissionsManager = permissions_manager
            """
            PermissionsManager object.
            """

        def add_permission_to_player(self, player: Player, permission: str):
            """
            Grants a permission to a player.
            """
            player.add_attachment(self._eap, permission, True)

        def remove_permission_from_player(self, player: Player, permission: str):
            """
            Revokes a permission from a player.
            """
            player.add_attachment(self._eap, permission, False)

        def add_role_to_player(self, player: Player, role: str):
            """
            Applies a player to a role, granting them all associated permissions.
            """
            permissionsData = read_permissions_config()
            permissionsData["roles"][role]["players"].append(player.name)
            role = permissionsData["roles"][role]
            for permission in role["permissions"]:
                self.add_permission_to_player(self._eap, player, permission)
            write_permissions_config(permissionsData)

        def remove_role_from_player(self, player: Player, role: str):
            """
            Removes a player from a role, revoking all associated permissions.
            """
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
            """
            PermissionsManager object.
            """

        def set_permission(
            self,
            name: str,
            description: str = "New permission.",
            default: str = "op",
        ):
            """
            Registers or updates a permission with the given name, description, and default access level.
            """
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
            """
            Deletes a permission.
            """
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
            """
            PermissionsManager object.
            """

        def set_role(
            self, name: str, permissions: list[str] = [], players: list[str] = []
        ):
            """
            Registers or updates a role with the given name, permissions, and players.
            """
            permissionData = read_permissions_config()
            permissionData["roles"][name] = {
                "permissions": permissions,
                "players": players,
            }
            write_permissions_config(permissionData)
            self._plugin.logger("§c[EAC] §rRole §a'§f{name}§a' §rhas been registered.")

        def delete_role(self, name: str):
            """
            Deletes a role.
            """
            permissionData = read_permissions_config()
            permissionData["roles"].pop(name)
            write_permissions_config(permissionData)
            self._plugin.logger("§c[EAC] §rRole §a'§f{name}§a' §rhas been deleted.")

        def add_permission_to_role(self, role: str, permission: str):
            """
            Adds a permission to a role.
            """
            permissionData = read_permissions_config()
            permissionData["roles"][role]["permissions"].append(permission)
            write_permissions_config(permissionData)

        def remove_permission_from_role(self, role: str, permission: str):
            """
            Removes a permission from a role.
            """
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
