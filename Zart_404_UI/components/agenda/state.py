from datetime import datetime
from typing import List, Tuple

import reflex as rx
import sqlalchemy.orm
from sqlmodel import select

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.models import AgendaModel, UserInfo
from Zart_404_UI.tools.utils import get_datetime

START_TIME = "00:00:00"
END_TIME = "23:59:59"


class AgendaState(UserSessionState):
    calendar: List["AgendaModel"] = []
    form_data: dict = {}
    agenda: List[Tuple[Tuple[str, str], Tuple[datetime, datetime]]] = (
        []
    )  # serves as a cached version of the agenda to reduce SQL calls, [("Paris",("2024-01-01", "20240201"))]

    limit: int = 20  # pagination on article list

    edit_mode_agenda_active: bool = False
    edit_mode_agenda_id: int = -1

    def handle_click_speed_dial(self, index: int, action: str):
        print(f"clicked for id {index} with action {action}")
        if action in ("Delete"):
            self.remove_agenda_from_calendar(index)

        elif action in ("Modify"):
            self.active_edit_mode_agenda(index)

    def remove_agenda_from_calendar(self, idx: int):
        agenda_to_remove = self.calendar[idx]
        self.delete_agenda_from_db(agenda_to_remove)
        del self.calendar[idx]

    def active_edit_mode_agenda(self, idx: int):
        self.edit_mode_agenda_id = idx
        self.edit_mode_agenda_active = True

    def deactive_edit_mode_agenda(self):
        self.edit_mode_agenda_id = -1
        self.edit_mode_agenda_active = False

    def load_calendar(self, *args, **kwargs):
        """Load user calendar."""
        lookup_args = ()

        with rx.session() as session:
            self.calendar = session.exec(
                select(AgendaModel).options(
                    sqlalchemy.orm.joinedload(AgendaModel.userinfo).joinedload(
                        UserInfo.local_user
                    )
                )
                # .where(lookup_args)
                .limit(self.limit)
            ).all()

    def set_limit_and_reload(self, limit: int = 5):
        self.limit = limit
        self.load_calendar()
        yield

    def record_agenda_in_db(
        self, country: str, town: str, from_date: datetime, to_date: datetime
    ):
        """Add a new agenda to the DB."""
        with rx.session() as session:
            new_agenda = AgendaModel(
                country=country,
                town=town,
                from_date=from_date,
                to_date=to_date,
            )
            session.add(new_agenda)
            session.commit()
            session.refresh(new_agenda)
            self.calendar.append(new_agenda)

    def delete_agenda_from_db(self, agenda: AgendaModel):
        with rx.session() as session:
            session.delete(agenda)
            session.commit()

    def is_correct_dates(self, from_date: datetime, to_date: datetime) -> bool:
        return from_date < to_date

    def is_overlapping_agenda(
        self, from_date: datetime, to_date: datetime
    ) -> dict:
        """Get an agenda in between to 2 dates"""
        temp_agenda = None
        # A new agenda can't exist in between an already existing booked agenda
        with rx.session() as session:
            temp_agenda = session.exec(
                select(AgendaModel)
                .where((AgendaModel.from_date >= from_date))
                .where(AgendaModel.to_date <= to_date)
            ).one_or_none()
        if temp_agenda is not None:
            return {
                "status": True,
                "message": "The chosen dates are already booked !",
            }

        # A new created agenda can't include a date from an already existing booked agenda
        with rx.session() as session:
            temp_agenda = session.exec(
                select(AgendaModel)
                .where((AgendaModel.from_date <= from_date))
                .where(AgendaModel.to_date >= to_date)
            ).one_or_none()
        if temp_agenda is not None:
            return {
                "status": True,
                "message": "The chosen dates are already booked !",
            }

        return {"status": False, "message": ""}

    def add_entry_to_agenda(
        self, country: str, town: str, from_date: datetime, to_date: datetime
    ) -> dict:
        return self.agenda.append(((country, town), (from_date, to_date)))

    def delete_entry_from_agenda(
        self, country: str, town: str, from_date: datetime, to_date: datetime
    ) -> dict:
        return self.agenda.remove(((country, town), (from_date, to_date)))

    @rx.var(cache=False)
    def display_date(self) -> str:
        return datetime.now().strftime(
            "%Y-%m-%d"
        )  # format for the day YYYY-MM-DD

    def validate_entry_data(
        self, from_date: datetime, to_date: datetime
    ) -> bool:
        return (
            self.is_correct_dates(from_date=from_date, to_date=to_date)
            and not self.is_overlapping_agenda(
                from_date=from_date, to_date=to_date
            )["status"]
        )

    def handle_submit(self, form_data: dict):
        self.form_data = form_data

        country = self.form_data.pop("country")
        town = self.form_data.pop("town")

        from_date = get_datetime(self.form_data.pop("from_date"), START_TIME)
        to_date = get_datetime(self.form_data.pop("to_date"), END_TIME)

        if self.validate_entry_data(from_date=from_date, to_date=to_date):
            # self.add_entry_to_agenda(
            #     country=country,
            #     town=town,
            #     from_date=from_date,
            #     to_date=to_date,
            # )
            self.record_agenda_in_db(
                country=country,
                town=town,
                from_date=from_date,
                to_date=to_date,
            )

        # post_id = form_data.pop("id")
        # publish_date = None
        # publish_time = None
        # if "publish_date" in form_data:
        #     publish_date = form_data.pop("publish_date")
        # if "publish_time" in form_data:
        #     publish_time = form_data.pop("publish_time")
        # publish_input_string = f"{publish_date} {publish_time}"
        # final_publish_date = None

        # try:
        #     final_publish_date = datetime.strptime(
        #         publish_input_string, "%Y-%m-%d %H:%M:%S"
        #     )
        # except ValueError as e:
        #     final_publish_date = None

        # publish_status = False

        # if "publish_status" in form_data:
        #     publish_status = form_data.pop("publish_status") == "on"

        # updated_data = {**form_data}
        # updated_data["publish_active"] = publish_status
        # updated_data["publish_date"] = final_publish_date

        # self.edit_post(post_id, updated_data)
        # return self.to_blog_post()


class SpeedDialHorizontal(rx.State):  # (rx.ComponentState):
    is_open: bool = False

    @rx.var
    def f_is_open(self):
        return self.is_open

    def toggle_true(self):
        self.is_open = True

    def toggle_false(self):
        self.is_open = False

    @rx.event
    def toggle(self, value: bool):
        self.is_open = value

    # @classmethod
    # def get_component(cls, **props):
    #     def menu_item(icon: str, text: str) -> rx.Component:
    #         return rx.tooltip(
    #             rx.icon_button(
    #                 rx.icon(icon, padding="2px"),
    #                 variant="soft",
    #                 color_scheme="gray",
    #                 size="3",
    #                 cursor="pointer",
    #                 radius="full",
    #             ),
    #             side="top",
    #             content=text,
    #         )

    #     def menu() -> rx.Component:
    #         return rx.hstack(
    #             menu_item("copy", "Copy"),
    #             menu_item("download", "Download"),
    #             menu_item("share-2", "Share"),
    #             position="absolute",
    #             bottom="0",
    #             spacing="2",
    #             padding_right="10px",
    #             right="100%",
    #             direction="row-reverse",
    #             align_items="center",
    #         )

    #     return rx.box(
    #         rx.box(
    #             rx.icon_button(
    #                 rx.icon(
    #                     "plus",
    #                     style={
    #                         "transform": rx.cond(
    #                             cls.is_open,
    #                             "rotate(45deg)",
    #                             "rotate(0)",
    #                         ),
    #                         "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
    #                     },
    #                     class_name="dial",
    #                 ),
    #                 variant="solid",
    #                 color_scheme="green",
    #                 size="3",
    #                 cursor="pointer",
    #                 radius="full",
    #                 position="relative",
    #             ),
    #             rx.cond(
    #                 cls.is_open,
    #                 menu(),
    #             ),
    #             position="relative",
    #         ),
    #         on_mouse_enter=cls.toggle(True),
    #         on_mouse_leave=cls.toggle(False),
    #         on_click=cls.toggle(~cls.is_open),
    #         style={"bottom": "15px", "right": "15px"},
    #         position="absolute",
    #         # z_index="50",
    #         **props,
    #     )
