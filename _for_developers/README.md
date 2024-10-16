***
# EasyAsPermissions API
**EasyAsPermissions** has its own API that developers can include in their plugins to use its features.

***
## Adding to Plugin
1) Download `eap_api.py` latest [release](../../releases).
2) Drop it into your plugin at the same level as your entry point script.
3) Add the following import to the top of your script:
   <br><br>
   ```python
   from .eap_api.py import PermissionsManager
   ```
5) And you're done!
***
# Usage
The API includes many useful implementations that can be used to manage player permissions.

Here is a list of all of available methods and attributes that can be used:
# `class` PermissionsManager
Parent class for permissions management.

#### `Example:`
```python
from .eap_api import PermissionsManager

class MyPlugin(Plugin):
    manager = PermissionsManager(self)
```

- ## `attr` players
  > Contains player-based permission methods.
  - ### `def` add_permission_to_player
    > #### `player: Player`, `permission: str`
    > 
    > Grants a permission to a player.
  - ### `def` remove_permission_from_player
    > #### `player: Player`, `permission: str`
    > 
    > Revokes a permission from a player.
  - ### `def` add_role_to_player
    > #### `player: Player`, `role: str`
    > 
    > Applies a player to a role, granting them all associated permissions.
  - ### `def` remove_role_from_player
    > #### `player: Player`, `role: str`
    > 
    > Removes a player from a role, revoking all associated permissions.
  ### `example.py`
  ```python
  ## Registering Permissions ##
  def example_create_permission(self: Plugin, player: Player):
      manager.permissions.set_permission(
          "example.permission", "Example permission.", "op"
      )
      player.send_message("Permission created.")
  ```

- ## `attr` permissions
  > Contains methods for managing permissions.
  - ### `def` set_permission
    > #### `name: str`, `description?: str`, `default?: str`
    > 
    > Registers or updates a permission with the given name, description, and default access level.
  - ### `def` delete_permission
    > #### `name: str`
    > 
    > Deletes a permission.
  ### `example.py`
  ```python
  ## Adding Permissions to Players ##
  def example_add_permission(self: Plugin, player: Player):
      manager.players.add_permission_to_player(player, "example.permission")
      player.send_message("Permission added to player.")
  ```

- ## `attr` roles
  > Contains methods for managing roles.
  - ### `def` set_role
    > #### `name: str`, `permissions: list[str]`, `players: list[str]`
    > 
    > Registers or updates a role with the given name, permissions, and players.
  - ### `def` delete_role
    > #### `name: str`
    > 
    > Deletes a role.
  - ### `def` add_permission_to_role
    > #### `role: str`, `permission: str`
    > 
    > Adds a permission to a role.
  - ### `def` remove_permission_from_role
    > #### `role: str`, `permission: str`
    > 
    > Removes a permission from a role.

  ### `example.py`
  ```python
  ## Using Roles ##
  def example_role(self: Plugin, player: Player):
      manager.roles.set_role("newrole", [], ["Vincent"])
      manager.roles.add_permission_to_role("newrole", "example.permission")
      manager.players.add_role_to_player(player, "newrole")
      player.send_message("Role added to player.")
  ```
***
`?` = Optional
