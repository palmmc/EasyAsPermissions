from .Players.permissions import (
    player_add_permission,
    player_add_to_role,
    player_remove_from_role,
    player_remove_permission,
)
from .manager import permissions_manager
from .Manage.submit import submit_permission
from .Utils.utils import (
    read_permissions_config,
    write_permissions_config,
    error_custom,
    reset_permissions,
    send_custom,
)
from endstone._internal.endstone_python import (
    ColorFormat,
    Player,
    RenderType,
)
from endstone.command import Command, CommandSender
from endstone.event import event_handler
from endstone.plugin import Plugin
import re
import json


class EasyAsPermissions(Plugin):
    prefix = "EasyAsPermissions"
    api_version = "0.5"
    load = "POSTWORLD"

    commands = {
        "managepermissions": {
            "description": "Opens permissions manager.",
            "usages": ["/managepermissions"],
            "aliases": ["manageperms", "permsmanager", "permissionsmanager"],
            "permissions": ["easyas.permissions.manager"],
        },
        "resetpermissions": {
            "description": "Resets all EAP permissions.",
            "usages": ["/resetpermissions"],
            "aliases": ["resetperms"],
            "permissions": ["easyas.permissions.reset"],
        },
        "perm": {
            "description": "Manages player permissions.",
            "usages": [
                "/perm (create)<action: CreatePerm> <permission: str> [description: str] [default: str]",
                "/perm (delete)<action: DeletePerm> <permission: str>",
                "/perm (add|remove)<action: PermPlayer> <player: target> <permission: str>",
            ],
            "aliases": ["easyperm"],
            "permissions": ["easyas.command.perm"],
        },
        "role": {
            "description": "Manages player roles.",
            "usages": [
                "/role (create)<action: CreateRole> <role: str>",
                "/role (delete)<action: DeleteRole> <role: str>",
                "/role (add|remove)<action: RolePlayer> <player: target> <role: str>",
                "/role (permissions)<action: RolePerms> <role: str> (add|remove)[action: PermRole] [permission: str]",
            ],
            "aliases": ["easyrole", "group"],
            "permissions": ["easyas.command.role"],
        },
    }

    # Load Permissions Data
    permissionsData = read_permissions_config()
    try:
        for permission in permissionsData["permissions"]:
            if permission["default"] == "all":
                permission["default"] = True
        # Mandatory Permissions
        permissionsData["permissions"]["easyas.permissions.manager"] = {
            "description": "Permissions manager permission.",
            "default": "op",
        }
        permissionsData["permissions"]["easyas.permissions.reset"] = {
            "description": "Reset permissions permission.",
            "default": "op",
        }
        permissionsData["permissions"]["easyas.command.perm"] = {
            "description": "Modify permissions permission.",
            "default": "op",
        }
        permissionsData["permissions"]["easyas.command.role"] = {
            "description": "Modify roles permission.",
            "default": "op",
        }
    except Exception as e:
        pass

    def on_enable(self) -> None:
        self.register_events(self)

    def on_load(self):
        self.logger.info(
            f"""
        {ColorFormat.RED}                                                                                                 
      _____             _____     _____               _         _             
     |   __|___ ___ _ _|  _  |___|  _  |___ ___ _____|_|___ ___|_|___ ___ ___ 
     |   __| .'|_ -| | |     |_ -|   __| -_|  _|     | |_ -|_ -| | . |   |_ -|
     |_____|__,|___|_  |__|__|___|__|  |___|_| |_|_|_|_|___|___|_|___|_|_|___|   by palm1
                   |___|                                                      
                                                            
        {ColorFormat.RESET}"""
        )
        self.logger.info(
            f"\n> {ColorFormat.RED}{ColorFormat.BOLD}Welcome to EasyAsPermissions!{ColorFormat.RESET}\n> {ColorFormat.YELLOW}API Version: {self.api_version}{ColorFormat.RESET}\n> {ColorFormat.LIGHT_PURPLE}For help and updates, visit [ {ColorFormat.BLUE}https://github.com/palmmc/EasyAsPermissions {ColorFormat.LIGHT_PURPLE}]{ColorFormat.RESET}"
        )

    def on_command(self, sender: CommandSender, command: Command, args: list[str]):
        # You can also handle commands here instead of setting an executor in on_enable if you prefer
        server = self.server
        if not (isinstance(sender, Player)):
            server.logger.info("Only players can use this command.")
            return
        player = sender
        if command.name == "managepermissions":
            permissions_manager(self, player)
        elif command.name == "resetpermissions":
            reset_permissions(self, player)
        elif command.name == "perm":
            if args[0] == "create":
                if len(args) < 2:
                    error_custom(
                        player,
                        "Invalid usage: §4/permission create <permission: str> [description: str] [default: str]",
                    )
                    return
                permission = {
                    "name": args[1],
                    "description": args[2] if len(args) > 2 else "New permission.",
                    "default": args[3] if len(args) > 3 else "op",
                }
                submit_permission(self, player, permission)
            elif args[0] == "delete":
                if len(args) < 2:
                    error_custom(
                        player, "Invalid usage: §4/permission delete <permission: str>"
                    )
                    return
                del self.permissionsData["permissions"][args[1]]
                write_permissions_config(self.permissionsData)
                send_custom(
                    player, f"§bPermission §f'§6{args[1]}§f' §bhas been deleted."
                )
            elif args[0] in ["add", "remove"]:
                if len(args) < 3:
                    error_custom(
                        player,
                        "Invalid usage: §4/permission (add|remove) <player: Player> <permission: str>",
                    )
                    return
                if args[0] == "add":
                    try:
                        player_add_permission(self, player, args[2])
                        send_custom(
                            player,
                            f"§bPermission §f'§6{args[2]}§f' §bhas been added to §f{args[1]}§b.",
                        )
                    except Exception as e:
                        error_custom(player, f"Failed to add permission.")
                        self.logger.error(f"Failed to add permission: {e}")
                elif args[0] == "remove":
                    try:
                        player_remove_permission(self, player, args[2])
                        send_custom(
                            player,
                            f"§bPermission §f'§6{args[2]}§f' §bhas been removed from §f{args[1]}§b.",
                        )
                    except Exception as e:
                        error_custom(player, f"Failed to remove permission.")
                        self.logger.error(f"Failed to add permission: {e}")
        elif command.name == "role":
            if args[0] == "create":
                args[1] = args[1].lower()
                if len(args) < 2:
                    error_custom(player, "Invalid usage: §4/role create <role: str>")
                    return
                if args[1] in self.permissionsData["roles"]:
                    error_custom(player, "Role already exists.")
                    return
                self.permissionsData["roles"][args[1]] = {
                    "permissions": [],
                    "players": [],
                }
                write_permissions_config(self.permissionsData)
                send_custom(player, f"§6Role §f'§e{args[1]}§f' §6has been created.")
            elif args[0] == "delete":
                args[1] = args[1].lower()
                if len(args) < 2:
                    error_custom(player, "Invalid usage: §4/role delete <role: str>")
                    return
                if not args[1] in self.permissionsData["roles"]:
                    error_custom(player, "Role does not exist.")
                    return
                del self.permissionsData["roles"][args[1]]
                write_permissions_config(self.permissionsData)
                send_custom(player, f"§6Role §f'§e{args[1]}§f' §6has been deleted.")
            elif args[0] in ["add", "remove"]:
                args[2] = args[2].lower()
                if len(args) < 3:
                    error_custom(
                        player,
                        "Invalid usage: §4/role (add|remove) <player: Player> <role: str>",
                    )
                    return
                if not args[2] in self.permissionsData["roles"]:
                    error_custom(player, "Role does not exist.")
                    return
                if args[0] == "add":
                    player_add_to_role(self, server.get_player(args[1]), args[2])
                    send_custom(
                        player,
                        f"§6Role §f'§e{args[2]}§f' §6has been added to §f{args[1]}§6.",
                    )
                elif args[0] == "remove":
                    player_remove_from_role(self, server.get_player(args[1]), args[2])
                    send_custom(
                        player,
                        f"§6Role §f'§e{args[2]}§f' §6has been removed from §f{args[1]}§6.",
                    )
            elif args[0] == "permissions":
                args[1] = args[1].lower()
                if len(args) < 2:
                    error_custom(
                        player,
                        "Invalid usage: §4/role permissions <role: str>",
                    )
                    return
                elif len(args) == 2:
                    pass  # Placeholder
                elif len(args) > 2:
                    if not args[3] in self.permissionsData["permissions"]:
                        error_custom(player, "Permission does not exist.")
                    if args[2] == "add":
                        if (
                            args[3]
                            in self.permissionsData["roles"][args[1]]["permissions"]
                        ):
                            error_custom(player, "Role already has this permission.")
                            return
                        self.permissionsData["roles"][args[1]]["permissions"].append(
                            args[3]
                        )
                        write_permissions_config(self.permissionsData)
                        send_custom(
                            player,
                            f"§cPermission §f'§6{args[3]}§f' §chas been added to §e{args[1]}§c.",
                        )
                    elif args[2] == "remove":
                        if (
                            not args[3]
                            in self.permissionsData["roles"][args[1]]["permissions"]
                        ):
                            error_custom(player, "Role does not have this permission.")
                            return
                        self.permissionsData["roles"][args[1]]["permissions"].remove(
                            args[3]
                        )
                        write_permissions_config(self.permissionsData)
                        send_custom(
                            player,
                            f"§cPermission §f'§6{args[3]}§f' §chas been removed from §e{args[1]}§c.",
                        )
