from typing import List, Tuple

import reflex as rx


class SpeedDialState(rx.State):

    item_is_open: bool = False

    actions: List[str] = ["Delete", "Modify"]

    @rx.var(cache=False)
    def list_actions(self) -> List[str]:
        return self.actions

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
