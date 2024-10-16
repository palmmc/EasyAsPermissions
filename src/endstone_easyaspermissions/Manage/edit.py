from .submit import submit_permission

from endstone.plugin import Plugin
from ..form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    MessageFormData,
    MessageFormResponse,
    ModalFormData,
    ModalFormResponse,
)
from endstone._internal.endstone_python import Player


def edit_permission(self: Plugin, player: Player, permission):
    form = ActionFormData()
    form.title("Edit: " + permission["name"])
    form.button("Set Name")
    form.button("Set Description")
    form.button("Set Default")
    form.button("Submit")

    def submit(self: Plugin, player: Player, result: ActionFormResponse, permission):
        if result.canceled:
            return confirm_exit_edit_permission(self, player, permission)
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
            self, player, response, permission
        )
    )


def confirm_exit_edit_permission(self: Plugin, player: Player, permission):
    form = MessageFormData()
    form.title("Confirm Exit")
    form.body("Are you sure you want to exit without saving?")
    form.button1("Submit")
    form.button2("Cancel")

    def exit_edit_permission(
        self: Plugin, player: Player, result: MessageFormResponse, permission
    ):
        if result.canceled or result.selection == 0:
            return
        else:
            edit_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: exit_edit_permission(
            self, player, response, permission
        )
    )


def set_permission_default(self: Plugin, player: Player, permission):
    form = ModalFormData()
    form.title("Set Permission Default")
    types = ["op", "all"]
    if "default" in permission:
        form.dropdown("Default Allowed", types, types.index(permission["default"]))
    else:
        form.dropdown("Default Allowed", types)

    def submit(self: Plugin, player: Player, result: ModalFormResponse, permission):
        if result.canceled:
            return edit_permission(self, player, permission)
        permission["default"] = types[int(result.formValues[0])]
        edit_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(
            self, player, response, permission
        )
    )


def set_permission_description(self: Plugin, player: Player, permission):
    form = ModalFormData()
    form.title("Set Permission Description")
    if "description" in permission:
        form.text_field(
            "Description", permission["description"], permission["description"]
        )
    else:
        form.text_field("Description", "...")

    def submit(self: Plugin, player: Player, result: ModalFormResponse, permission):
        if result.canceled:
            return edit_permission(self, player, permission)
        permission["description"] = result.formValues[0]
        edit_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(
            self, player, response, permission
        )
    )


def set_permission_name(self: Plugin, player: Player, permission):
    form = ModalFormData()
    form.title("Set Permission Name")
    if "name" in permission:
        form.text_field("Name", permission["name"], permission["name"])
    else:
        form.text_field("Name", "easyas.permission.example")

    def submit(self: Plugin, player: Player, result: ModalFormResponse, permission):
        if result.canceled:
            return edit_permission(self, player, permission)
        permission["name"] = result.formValues[0]
        edit_permission(self, player, permission)

    form.show(player).then(
        lambda player=Player, response=ModalFormResponse: submit(
            self, player, response, permission
        )
    )
