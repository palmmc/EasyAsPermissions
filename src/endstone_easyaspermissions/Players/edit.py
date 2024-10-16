from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin

from ..Utils.utils import (
    error_custom,
    send_custom,
)
from ..form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    ModalFormData,
    ModalFormResponse,
)

from .permissions import (
    player_add_permission,
    player_remove_permission,
    player_add_to_role,
    player_remove_from_role,
)


def edit_player(self: Plugin, player: Player):
    form = ModalFormData()
    form.title("Edit Player")
    form.text_field("Enter a name to edit:", "Vincent")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return
        playerName = result.formValues[0]
        permplayer = self.server.get_player(playerName)
        if permplayer is None:
            error_custom(
                player, f"Player '§4{playerName}§c' is not online or does not exist."
            )
            return
        edit_player_permissions(self, player, permplayer)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def edit_player_permissions(self: Plugin, player: Player, permplayer: Player):
    form = ActionFormData()
    form.title(f"Edit: {permplayer.name}")
    form.button("Add Permission", "textures/ui/smithing-table-plus.png")
    form.button("Remove Permission", "textures/ui/dark_minus.png")
    form.button("Add Role", "textures/ui/smithing-table-plus.png")
    form.button("Remove Role", "textures/ui/dark_minus.png")

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        if result.selection == 0:
            add_player_permission(self, player, permplayer)
        elif result.selection == 1:
            remove_player_permission(self, player, permplayer)
        elif result.selection == 2:
            add_player_role(self, player, permplayer)
        elif result.selection == 3:
            remove_player_role(self, player, permplayer)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def add_player_permission(self: Plugin, player: Player, permplayer: Player):
    form = ModalFormData()
    form.title("Add Permission")
    form.text_field("Permission Name", "easyas.permission.example")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return
        permissionName = result.formValues[0]
        try:
            player_add_permission(self, permplayer, permissionName)
            send_custom(
                player,
                f"§bPermission §f'§6{result.formValues[0]}§f' §bhas been added to §f{permplayer.name}§b.",
            )
        except Exception as e:
            error_custom(player, f"Failed to add permission.")
            self.logger.error(f"Failed to add permission: {e}")

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def remove_player_permission(self: Plugin, player: Player, permplayer: Player):
    form = ModalFormData()
    form.title("Remove Permission")
    form.text_field("Permission Name", "easyas.permission.example")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return
        permissionName = result.formValues[0]
        try:
            player_remove_permission(self, permplayer, permissionName)
            send_custom(
                player,
                f"§bPermission §f'§6{result.formValues[0]}§f' §bhas been removed from §f{permplayer.name}§b.",
            )
        except Exception as e:
            error_custom(player, f"Failed to remove permission.")
            self.logger.error(f"Failed to remove permission: {e}")

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def add_player_role(self: Plugin, player: Player, permplayer: Player):
    form = ModalFormData()
    form.title("Add Role")
    form.text_field("Role Name", "vip")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return
        roleName = result.formValues[0]
        try:
            player_add_to_role(self, permplayer, roleName)
            send_custom(
                player,
                f"§6Role §f'§6{roleName}§f' §6has been added to §f{permplayer.name}§6.",
            )
        except Exception as e:
            error_custom(player, f"Failed to add role.")
            self.logger.error(f"Failed to add role: {e}")

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )


def remove_player_role(self: Plugin, player: Player, permplayer: Player):
    form = ModalFormData()
    form.title("Remove Role")
    form.text_field("Role Name", "vip")

    def submit(self: Plugin, player: Player, result: ModalFormResponse):
        if result.canceled:
            return
        roleName = result.formValues[0]
        try:
            player_remove_from_role(self, permplayer, roleName)
            send_custom(
                player,
                f"§6Role §f'§6{roleName}§f' §6has been removed from §f{permplayer.name}§6.",
            )
        except Exception as e:
            error_custom(player, f"Failed to remove role.")
            self.logger.error(f"Failed to remove role: {e}")

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(self, player, response)
    )
