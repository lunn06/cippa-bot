from typing import Any

from aiogram_dialog import DialogManager


async def name_getter(**_kwargs) -> dict[str, Any]:
    return {
        "text": "Укажите ваше ФИО"
    }


async def clear_name_getter(dialog_manager: DialogManager, **_kwargs) -> dict[str, Any]:
    invalid_name = dialog_manager.dialog_data["invalid_name"]
    return {
        "text": f"Коректно ли ФИО: {invalid_name}",
        "accept_button_text": "ФИО верно",
        "back_button_text": "Ввести ФИО заново",
    }


async def city_getter(**_kwargs) -> dict[str, Any]:
    return {
        "text": "В каком городе(населённом пункте) вы работаете?"
    }


async def clear_city_getter(dialog_manager: DialogManager, **_kwargs) -> dict[str, Any]:
    invalid_city = dialog_manager.dialog_data["invalid_city"]
    return {
        "text": f"Коректно ли название города: {invalid_city}",
        "accept_button_text": "Корректно",
        "back_button_text": "Ввести город заново",
    }


async def preschool_getter(**_kwargs) -> dict[str, Any]:
    return {
        "text": "В какой организации дошкольного образования вы работаете?"
    }


async def position_getter(**_kwargs) -> dict[str, Any]:
    return {
        "text": "Какую должность вы занимаете в указанной организации?"
    }


async def final_getter(**_kwargs) -> dict[str, Any]:
    return {
        "text": '''
Спасибо за проходение опроса! Присоединяйтесь к нам в наших социальных сетях:
✅ https://t.me/ru_smart_toy
''',
    }
