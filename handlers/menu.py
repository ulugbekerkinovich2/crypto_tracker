import json
import asyncio
from functools import partial
from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js


class TaskHandler:
    def __init__(self):
        self.__coins = ["BTC", "ETH"]

    @staticmethod
    def read_task_file():
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data["name"]] = data["price to alert"]
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(last_changes, file, indent=4)

    @staticmethod
    def delete_task_in_file(coin_name, update=True):
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[coin_name]

            with open("tasks.json", "w", encoding="utf-8") as file:
                json.dump(last_changes, file, indent=4)
        except KeyError:
            print("Ключ отсутствует в списке заданий")
        if update:
            run_js("location.reload()")

    @staticmethod
    def get_task_list():
        result = []
        tasks = TaskHandler.read_task_file()

        # Кажется будто можно сделать через lambda а не partial,
        # Но на самом деле нет, ибо lambda в этом случае сохранит везде последний объект,
        # И каждая кнопка будет работать только для него, вызывая последнюю монетку для всех
        for name, price in tasks.items():
            result.append([
                name,
                price,
                put_button(f"delete {name}", onclick=partial(TaskHandler.delete_task_in_file, name))
            ])

        put_table(
            result,
            header=["name", "price to alert", "delete?"]
        )
        put_button("Назад", onclick=lambda: run_js("location.reload()"))

    # Валидация форм для отправки
    @staticmethod
    def add_task_validate(data):
        if data is None or data == "":
            return "price", "Необходимо заполнить поле"

    async def add_task_in_list(self):
        coin_ticker = await inp.select("Выберите монету", self.__coins, multiple=False)
        price = await inp.input('Введите ожидаемую цену', validate=TaskHandler.add_task_validate)

        if all([coin_ticker, price]):
            toast("Задание успешно создано")
            await asyncio.sleep(1)
            run_js("location.reload()")
            TaskHandler.add_task_to_file({
                "name": coin_ticker.lower(),
                "price to alert": price.replace('.', '',).replace(',', '').lower()
            })

