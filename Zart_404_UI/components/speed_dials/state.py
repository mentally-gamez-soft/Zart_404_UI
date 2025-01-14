from typing import List, Tuple

import reflex as rx


class SpeedDialState(rx.State):

    item_is_open: bool = False
    items: List[Tuple[str, str]] = [
        ("trash-2", "Delete"),
        ("pencil", "Modify"),
    ]

    @rx.var(cache=True)
    def list_items(self):
        return self.items

    def add_item(self, icon_name: str, action_verb: str):
        self.items.append((icon_name, action_verb))

    @rx.event
    def handle_click_speed_dial(self, *args, **kwargs):
        for k, v in kwargs.items():
            print(f"clicked speed dial key:{k} , value {v}")

    @rx.var(cache=False)
    def is_open(self):
        return self.item_is_open

    def toggle_true(self):
        self.item_is_open = True

    def toggle_false(self):
        self.item_is_open = False

    @rx.event
    def toggle(self, value: bool):
        self.item_is_open = value
