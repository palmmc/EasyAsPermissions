from .Manage.roles import manage_roles
from .Players.edit import edit_player
from endstone._internal.endstone_python import (
    Player,
)
import json
import os

from .form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    MessageFormData,
    MessageFormResponse,
    ModalFormData,
    ModalFormResponse,
)
from .Manage.add import add_permission
from .Manage.edit import edit_permission
from .Utils.utils import (
    error_custom,
    read_permissions_config,
    write_permissions_config,
    send_custom,
)

from endstone.plugin import Plugin

### PERMISSION MANAGER FUNCTIONALITY ###

permissionData = read_permissions_config()


def permissions_manager(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Permissions Manager")
    form.body("Click a permission to edit it.")
    form.button("Add Permission", "textures/ui/smithing-table-plus.png")
    form.button("Remove Permission", "textures/ui/dark_minus.png")
    form.button("Manage Roles", "textures/ui/up_arrow.png")
    form.button("Edit Player", "textures/ui/up_arrow.png")
    for permission_name in permissionData["permissions"].keys():
        permission = permissionData["permissions"][permission_name]
        form.button(
            f"{permission_name}\n{permission['description']}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        if result.selection == 0:
            add_permission(self, player, {})
        elif result.selection == 1:
            remove_permission(self, player)
        elif result.selection == 2:
            manage_roles(self, player)
        elif result.selection == 3:
            edit_player(self, player)
        else:
            permissions = permissionData["permissions"]
            permName = list(permissions.keys())[result.selection - 4]
            permission = permissions[permName]
            edit_permission(
                self,
                player,
                {
                    "name": permName,
                    "description": permission["description"],
                    "default": permission["default"],
                },
            )

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def remove_permission(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Remove permission")
    form.body("Click a permission to remove it.")
    for permission_name in permissionData["permissions"].keys():
        permission = permissionData["permissions"][permission_name]
        form.button(
            f"{permission_name}\n§7{permission['description']}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        permissions = permissionData["permissions"]
        permission = permissions[list(permissions.keys())[result.selection - 1]]
        confirm_remove_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def confirm_remove_permission(self: Plugin, player: Player, permission):
    form = MessageFormData()
    form.title("Confirm Removal")
    form.body(f"Are you sure you want to remove '{permission['name']}'?")
    form.button1("Yes")
    form.button2("No")

    def remove_permission(
        self: Plugin, player: Player, result: MessageFormResponse, permission
    ):
        if result.canceled or result.selection == 2:
            return
        else:
            permissionData["permissions"].pop(permission["name"])
            write_permissions_config(permissionData)
            send_custom(
                player,
                f"§cpermission §f'§6{permission['name']}§f' §chas been removed.\n§eAttempting to reload server...",
            )

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: remove_permission(
            self, player, response, permission
        )
    )
