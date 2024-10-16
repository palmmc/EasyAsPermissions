from .submit import submit_permission

from endstone.plugin import Plugin
from ..form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    MessageFormData,
    MessageFormResponse,
)
from endstone._internal.endstone_python import Player

from ..Manage.edit import (
    set_permission_description,
    set_permission_name,
)


def add_permission(self: Plugin, player: Player, permission):
    form = ActionFormData()
    form.title("Add Permission")
    form.button("Set Name")
    form.button("Set Description")
    form.button("Set Default")
    form.button("Submit")

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return confirm_exit_add_permission(self, player, permission)
        if result.selection == 0:
            set_permission_name(self, player, permission)
        elif result.selection == 1:
            set_permission_description(self, player, permission)
        elif result.selection == 2:
            set_permission_default(self, player, permission)
        elif result.selection == 3:
            submit_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def confirm_exit_add_permission(self: Plugin, player: Player, permission):
    form = MessageFormData()
    form.title("Confirm Exit")
    form.body("Are you sure you want to exit without saving?")
    form.button1("Submit")
    form.button2("Cancel")

    def exit_add_permission(
        self: Plugin, player: Player, result: MessageFormResponse, permission
    ):
        if result.canceled or result.selection == 0:
            return
        else:
            add_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: exit_add_permission(
            self, player, response, permission
        )
    )
