from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin
from ..Utils.utils import (
    read_permissions_config,
    write_permissions_config,
    send_custom,
    error_custom,
)


def submit_permission(self: Plugin, player: Player, permission):
    if "name" not in permission:
        error_custom(player, "Incomplete permission: Property '§4name§c' is missing.")
        return
    if "description" not in permission:
        permission["description"] = "New permission."
    if "default" not in permission:
        permission["default"] = "op"
    permissionData = read_permissions_config()
    permissionData["permissions"][permission["name"]] = {
        "description": permission["description"],
        "default": permission["default"],
    }
    write_permissions_config(permissionData)
    send_custom(
        player,
        f"§aPermission §f'§6{permission['name']}§f' §ahas been saved.\n§eServer has been reloaded successfully!",
    )
    try:
        self.server.reload()
    except Exception as e:
        error_custom(player, f"Failed to reload server: {e}")
        return
