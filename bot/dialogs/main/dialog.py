from aiogram.types import Message, User
from aiogram_dialog import Dialog, Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.text import Format
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import ensure_user
from bot.dialogs.main.getters import (
    name_getter,
    clear_name_getter,
    city_getter,
    clear_city_getter,
    position_getter,
    preschool_getter,
    final_getter,
)
from bot.dialogs.main.handlers import (
    name_factory,
    name_on_success,
    name_on_error,
    clear_name_button_on_click,
    city_factory,
    city_on_success,
    city_on_error,
    clear_city_button_on_click,
    position_on_success,
    preschool_on_success,
    final_on_input,
    accepted_factory,
    accepted_on_error,
)
from bot.states import MainSG


async def start_handler(
        message: Message,
        dialog_manager: DialogManager,
        event_from_user: User,
        session: AsyncSession,
        **_kwargs,
) -> None:
    await message.answer("Здравствуйте! Перед переходом в наши социальные сети пройдите небольшой опрос")
    await ensure_user(session, event_from_user.id, event_from_user.username)

    await dialog_manager.start(
        state=MainSG.name,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )


def get_dialog() -> Dialog:
    name_window = Window(
        Format("{text}"),
        TextInput(
            id="name_text_input",
            type_factory=name_factory,
            on_success=name_on_success,
            on_error=name_on_error,
        ),
        getter=name_getter,
        state=MainSG.name
    )

    clear_name_window = Window(
        Format("{text}"),
        Button(
            Format("{accept_button_text}"),
            id="clear_name_accept_button",
            on_click=clear_name_button_on_click,
        ),
        SwitchTo(
            Format("{back_button_text}"),
            id="clear_name_back_button",
            state=MainSG.name,
        ),
        getter=clear_name_getter,
        state=MainSG.clear_name,
    )

    city_window = Window(
        Format("{text}"),
        TextInput(
            id="city_text_input",
            type_factory=city_factory,
            on_success=city_on_success,
            on_error=city_on_error,
        ),
        getter=city_getter,
        state=MainSG.city
    )

    clear_city_window = Window(
        Format("{text}"),
        Button(
            Format("{accept_button_text}"),
            id="clear_city_accept_button",
            on_click=clear_city_button_on_click,
        ),
        SwitchTo(
            Format("{back_button_text}"),
            id="clear_city_back_button",
            state=MainSG.city,
        ),
        getter=clear_city_getter,
        state=MainSG.clear_city,
    )

    preschool_window = Window(
        Format("{text}"),
        TextInput(
            id="preschool_text_input",
            type_factory=accepted_factory,
            on_success=preschool_on_success,
            on_error=accepted_on_error,
        ),
        getter=preschool_getter,
        state=MainSG.preschool,
    )

    position_window = Window(
        Format("{text}"),
        TextInput(
            id="position_text_input",
            type_factory=accepted_factory,
            on_success=position_on_success,
            on_error=accepted_on_error,
        ),
        getter=position_getter,
        state=MainSG.position,
    )

    final_window = Window(
        Format("{text}"),
        TextInput(
            id="final_text_input",
            on_success=final_on_input,
        ),
        getter=final_getter,
        state=MainSG.final,
    )

    return Dialog(
        name_window,
        clear_name_window,
        city_window,
        clear_city_window,
        preschool_window,
        position_window,
        final_window,
    )
