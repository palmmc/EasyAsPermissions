from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin

from ..Utils.utils import (
    error_custom,
    send_custom,
    write_permissions_config,
    read_permissions_config,
)
from ..form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    ModalFormData,
    ModalFormResponse,
    MessageFormData,
    MessageFormResponse,
)


def manage_roles(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Manage Roles")
    form.body("Click a role to manage it.")
    form.button("Add Role", "textures/ui/smithing-table-plus.png")
    form.button("Remove Role", "textures/ui/dark_minus.png")
    permissionData = read_permissions_config()
    for role_name in permissionData["roles"].keys():
        role = permissionData["roles"][role_name]
        form.button(
            f"{role_name}\n§2Players: §8{len(role['players'])} §8| §1Permissions: §8{len(role['permissions'])}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        if result.selection == 0:
            add_role(self, player, {"players": [], "permissions": []})
        elif result.selection == 1:
            remove_role(self, player)
        else:
            roles = permissionData["roles"]
            roleName = list(roles.keys())[result.selection - 2]
            role = roles[roleName]
            edit_role(
                self,
                player,
                {
                    "name": roleName,
                    "players": role["players"],
                    "permissions": role["permissions"],
                },
            )

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def add_role(self: Plugin, player: Player, role):
    form = ModalFormData()
    form.title("Add Role")
    form.text_field("Role Name", "vip")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return manage_roles(self, player)
        permissionData = read_permissions_config()
        roleName = result.formValues[0]
        if roleName in permissionData["roles"]:
            error_custom(player, f"Role '{roleName}' already exists.")
            return
        permissionData["roles"][roleName] = {"players": [], "permissions": []}
        write_permissions_config(permissionData)
        send_custom(player, f"Role '{roleName}' has been added.")

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def remove_role(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Remove Role")
    form.body("Click a role to remove it.")
    permissionData = read_permissions_config()
    for role_name in permissionData["roles"].keys():
        role = permissionData["roles"][role_name]
        form.button(
            f"{role_name}\nPlayers: {len(role['players'])} | Permissions: {len(role['permissions'])}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return manage_roles(self, player)
        roles = permissionData["roles"]
        roleName = list(roles.keys())[result.selection]
        role = roles[roleName]
        confirm_remove_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def confirm_remove_role(self: Plugin, player: Player, role):
    form = MessageFormData()
    form.title("Confirm Removal")
    form.body(f"Are you sure you want to remove '{role['name']}'?")
    form.button1("Yes")
    form.button2("No")

    def remove_role(self: Plugin, player: Player, result: MessageFormResponse, role):
        permissionData = read_permissions_config()
        if result.canceled or result.selection == 2:
            return
        else:
            permissionData["roles"].pop(role["name"])
            write_permissions_config(permissionData)
            send_custom(
                player,
                f"§cRole §f'§6{role['name']}§f' §chas been removed.\n§eAttempting to reload server...",
            )

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: remove_role(
            self, player, response, role
        )
    )


def edit_role(self: Plugin, player: Player, role):
    form = ActionFormData()
    form.title("Edit: " + role["name"])
    form.button("Add Player")
    form.button("Remove Player")
    form.button("Add Permission")
    form.button("Remove Permission")
    form.button("Submit")

    def submit(self: Plugin, player: Player, result: ActionFormResponse, role):
        if result.canceled:
            return confirm_exit_edit_role(self, player, role)
        if result.selection == 0:
            add_player_to_role(self, player, role)
        elif result.selection == 1:
            remove_player_from_role(self, player, role)
        elif result.selection == 2:
            add_permission_to_role(self, player, role)
        elif result.selection == 3:
            remove_permission_from_role(self, player, role)
        elif result.selection == 4:
            submit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response, role
        )
    )


def confirm_exit_edit_role(self: Plugin, player: Player, role):
    form = MessageFormData()
    form.title("Confirm Exit")
    form.body("Are you sure you want to exit without saving?")
    form.button1("Submit")
    form.button2("Cancel")

    def exit_edit_role(self: Plugin, player: Player, result: MessageFormResponse, role):
        if result.canceled or result.selection == 0:
            return
        else:
            edit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: exit_edit_role(
            self, player, response, role
        )
    )


def add_player_to_role(self: Plugin, player: Player, role):
    form = ModalFormData()
    form.title("Add Player")
    form.text_field("Player Name", "Vincent")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return edit_role(self, player, role)
        playerName = result.formValues[0]
        if playerName in role["players"]:
            error_custom(player, f"Player '{playerName}' is already in the role.")
            return
        role["players"].append(playerName)
        edit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def remove_player_from_role(self: Plugin, player: Player, role):
    form = ActionFormData()
    form.title("Remove Player")
    form.body("Click a player to remove them.")
    for playerName in role["players"]:
        form.button(playerName, "textures/ui/user_icon_white.png")

    def submit(self: Plugin, player: Player, result: ActionFormResponse, role):
        if result.canceled:
            return edit_role(self, player, role)
        playerName = role["players"][result.selection]
        role["players"].remove(playerName)
        edit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(
            self, player, response, role
        )
    )


def add_permission_to_role(self: Plugin, player: Player, role):
    form = ModalFormData()
    form.title("Add Permission")
    form.text_field("Permission Name", "easyas.permission.example")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return edit_role(self, player, role)
        permissionName = result.formValues[0]
        if permissionName in role["permissions"]:
            error_custom(
                player, f"Permission '{permissionName}' is already in the role."
            )
            return
        role["permissions"].append(permissionName)
        edit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def remove_permission_from_role(self: Plugin, player: Player, role):
    form = ActionFormData()
    form.title("Remove Permission")
    form.body("Click a permission to remove it.")
    for permission_name in role["permissions"]:
        form.button(permission_name, "textures/ui/user_icon_white.png")

    def submit(self: Plugin, player: Player, result: ActionFormResponse, role):
        if result.canceled:
            return edit_role(self, player, role)
        permissionName = role["permissions"][result.selection]
        role["permissions"].remove(permissionName)
        edit_role(self, player, role)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(
            self, player, response, role
        )
    )


def submit_role(self: Plugin, player: Player, role):
    if "name" not in role:
        error_custom(player, "Incomplete permission: Property '§4name§c' is missing.")
        return
    permissionData = read_permissions_config()
    permissionData["roles"][role["name"]] = {
        "players": role["players"],
        "permissions": role["permissions"],
    }
    write_permissions_config(permissionData)
    send_custom(
        player,
        f"§aRole §f'§6{role['name']}§f' §ahas been saved.",
    )
