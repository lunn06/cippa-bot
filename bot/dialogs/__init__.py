from aiogram_dialog import Dialog

from . import main


def get_dialogs() -> list[Dialog]:
    return [
        main.get_dialog()
    ]
