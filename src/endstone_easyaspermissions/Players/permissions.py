from ..Utils.utils import read_permissions_config, write_permissions_config
from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin


def player_add_permission(self: Plugin, player: Player, permission: str):
    player.add_attachment(self, permission, True)


def player_remove_permission(self: Plugin, player: Player, permission: str):
    player.add_attachment(self, permission, False)


def player_add_to_role(self: Plugin, player: Player, role: str):
    permissionsData = read_permissions_config()
    permissionsData["roles"][role]["players"].append(player.name)
    role = permissionsData["roles"][role]
    for permission in role["permissions"]:
        player_add_permission(self, player, permission)
    write_permissions_config(permissionsData)


def player_remove_from_role(self: Plugin, player: Player, role: str):
    permissionsData = read_permissions_config()
    permissionsData["roles"][role]["players"].remove(player.name)
    role = permissionsData["roles"][role]
    for permission in role["permissions"]:
        player_remove_permission(self, player, permission)
    write_permissions_config(permissionsData)
