import re

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.requests import ensure_user_fullname, ensure_user_city, ensure_user_preschool, ensure_user_position
from bot.states import MainSG

NAME_RE = re.compile(r"^\w{1,32} \w{1,32} ?\w{1,32}?$")
ACCEPTED_LETTER_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя -"
ACCEPTED_ERROR_STR = "ascii"


def name_factory(text: str) -> str:
    text = text.strip()
    if any(c.lower() not in ACCEPTED_LETTER_LOWER for c in text):
        raise ValueError(ACCEPTED_ERROR_STR)
    if NAME_RE.fullmatch(text):
        return text
    raise ValueError(text)


async def name_on_success(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        name: str,
        **_kwargs,
) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await ensure_user_fullname(session, message.from_user.id, name)

    await dialog_manager.switch_to(MainSG.city)


async def name_on_error(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError,
        **_kwargs,
) -> None:
    error_arg = error.args[0]
    if error_arg == ACCEPTED_ERROR_STR:
        await message.answer("Допустимы только буквы кириллицы")
        return

    dialog_manager.dialog_data["invalid_name"] = error_arg
    await dialog_manager.switch_to(MainSG.clear_name)


async def clear_name_button_on_click(
        callback: CallbackQuery,
        _button: Button,
        dialog_manager: DialogManager,
        **_kwargs,
) -> None:
    session = dialog_manager.middleware_data["session"]
    invalid_name = dialog_manager.dialog_data["invalid_name"]
    await ensure_user_fullname(session, callback.from_user.id, invalid_name)

    await dialog_manager.switch_to(MainSG.city)


def city_factory(text: str) -> str:
    text = text.strip()
    if any(c.lower() not in ACCEPTED_LETTER_LOWER for c in text):
        raise ValueError(ACCEPTED_ERROR_STR)
    if text[0].isupper():
        return text
    raise ValueError(text)


async def city_on_success(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        city: str,
        **_kwargs,
) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await ensure_user_city(session, message.from_user.id, city)

    await dialog_manager.switch_to(MainSG.preschool)


async def city_on_error(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError,
        **_kwargs,
) -> None:
    error_arg = error.args[0]
    if error_arg == ACCEPTED_ERROR_STR:
        await message.answer("Допустимы только буквы кириллицы")
        return

    dialog_manager.dialog_data["invalid_city"] = error_arg
    await dialog_manager.switch_to(MainSG.clear_city)


async def clear_city_button_on_click(
        callback: CallbackQuery,
        _button: Button,
        dialog_manager: DialogManager,
        **_kwargs,
) -> None:
    session = dialog_manager.middleware_data["session"]
    invalid_city = dialog_manager.dialog_data["invalid_city"]
    await ensure_user_city(session, callback.from_user.id, invalid_city)

    await dialog_manager.switch_to(MainSG.preschool)


def accepted_factory(text: str) -> str:
    text = text.strip()
    if any(c.lower() not in ACCEPTED_LETTER_LOWER for c in text):
        raise ValueError(ACCEPTED_ERROR_STR)
    return text


async def accepted_on_error(
        message: Message,
        _widget: ManagedTextInput,
        _dialog_manager: DialogManager,
        error: ValueError,
        **_kwargs,
) -> None:
    error_arg = error.args[0]
    if error_arg == ACCEPTED_ERROR_STR:
        await message.answer("Допустимы только буквы кириллицы")
        return


async def preschool_on_success(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        preschool: str,
        **_kwargs,
) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await ensure_user_preschool(session, message.from_user.id, preschool)

    await dialog_manager.switch_to(MainSG.position)


async def position_on_success(
        message: Message,
        _widget: ManagedTextInput,
        dialog_manager: DialogManager,
        position: str,
        **_kwargs,
) -> None:
    session: AsyncSession = dialog_manager.middleware_data["session"]
    await ensure_user_position(session, message.from_user.id, position)

    await dialog_manager.switch_to(MainSG.final)


async def final_on_input(
        message: Message,
        _widget: ManagedTextInput,
        _dialog_manager: DialogManager,
        _: str,
        **_kwargs,
) -> None:
    await message.answer(
        "Вы завершили опрос! Если хотите пройти его ещё раз, чтобы обновить данные, нажмите на команду -> /start",
    )
