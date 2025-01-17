from datetime import datetime, timedelta
from typing import List, Tuple

import reflex as rx
import sqlalchemy.orm
from sqlmodel import select

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.models import AgendaModel, UserInfo
from Zart_404_UI.tools.utils import get_date_string, get_datetime

START_TIME = "00:00:00"
END_TIME = "23:59:59"
FORMAT_DATE = "%Y-%m-%d"


class AgendaFormState(rx.State):
    _available_countries = [
        "France",
        "Feroe",
        "Spain",
        "Maroc",
        "England",
    ]
    search_text: str = ""
    search_is_focused: bool = False

    @rx.event
    def handle_custom_on_blur(self, value: bool):
        self.search_is_focused = bool
        self._available_towns = self.get_available_towns(self.search_text)

    @rx.var(cache=False)
    def default_available_completions(self) -> list[str]:
        if (
            not self.search_is_focused
            or self.search_text == ""
            or self.search_text in self._available_countries
        ):
            return []
        return [
            option
            for option in self._available_countries
            if self.search_text.lower() in option.lower()
        ]

    # Additional management of a second field town
    _available_towns: list[str] = []
    search_towns: str = ""
    search_towns_is_focused: bool = False

    def get_available_towns(self, country: str) -> list[str]:
        if country in ("France"):
            return ["Paris", "Marseille", "Bastia", "Bordeaux", "Lille"]
        elif country in ("Spain"):
            return [
                "Jaen",
                "Madrid",
                "Barcelona",
                "Valecia",
                "Gijon",
                "Murcia",
                "Toledo",
                "Burgos",
            ]
        elif country in ("Maroc"):
            return [
                "Casablanca",
                "Fez",
                "Agadir",
            ]
        elif country in ("England"):
            return ["London", "Leicester", "Totenham", "Manchester"]

        else:
            return ["Unknown cities"]

    @rx.var(cache=False)
    def town_available_completions(self) -> list[str]:
        if (
            not self.search_towns_is_focused
            or self.search_towns == ""
            or self.search_towns in self._available_towns
        ):
            return []
        return [
            option
            for option in self._available_towns
            if self.search_towns.lower() in option.lower()
        ]


class AgendaState(UserSessionState):
    calendar: List["AgendaModel"] = []
    form_data: dict = {}
    agenda_from_date: str = ""
    agenda_to_date: str = ""
    is_valid_agenda: bool = True

    edit_agenda: AgendaModel = None

    limit: int = 20  # pagination on article list

    edit_mode_agenda_active: bool = False
    edit_mode_agenda_id: int = -1

    @rx.event
    def handle_click_speed_dial(self, index: int, action: str):
        if action in ("Delete"):
            self.remove_agenda_from_calendar(index)

        elif action in ("Modify"):
            self.active_edit_mode_agenda(index)
            print("modif - index ", index)

    def remove_agenda_from_calendar(self, idx: int):
        agenda_to_remove = self.calendar[idx]
        self.delete_agenda_from_db(agenda_to_remove)
        del self.calendar[idx]

    def active_edit_mode_agenda(self, idx: int):
        self.edit_mode_agenda_id = idx
        self.edit_mode_agenda_active = True
        self.edit_agenda = self.calendar[idx]

    def deactive_edit_mode_agenda(self):
        self.edit_mode_agenda_id = -1
        self.edit_mode_agenda_active = False

    def load_calendar(self, *args, **kwargs):
        """Load user calendar."""
        lookup_args = AgendaModel.userinfo_id == self.userinfo_id

        with rx.session() as session:
            self.calendar = session.exec(
                select(AgendaModel)
                .options(
                    sqlalchemy.orm.joinedload(AgendaModel.userinfo).joinedload(
                        UserInfo.local_user
                    )
                )
                .where(lookup_args)
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
            new_agenda.userinfo_id = self.userinfo_id
            session.add(new_agenda)
            session.commit()
            session.refresh(new_agenda)
            self.calendar.append(new_agenda)

    def delete_agenda_from_db(self, agenda: AgendaModel):
        with rx.session() as session:
            session.delete(agenda)
            session.commit()

    def date_string_to_datetime(self, date: str, date_origin: str = "TO"):
        if date_origin in ("TO"):
            return get_datetime(date, END_TIME)
        return get_datetime(date, START_TIME)

    def datetime_to_date_string(self, date: datetime):
        return get_date_string(date)

    def is_correct_dates(self, from_date: datetime, to_date: datetime) -> bool:
        print("from date -> ", from_date, " , to date -> ", to_date)
        return from_date < to_date

    def is_overlapping_agenda(
        self, from_date: datetime, to_date: datetime
    ) -> dict:
        """Get an agenda in between to 2 dates"""
        temp_agenda = None
        lookup_args = AgendaModel.userinfo_id == self.userinfo_id

        # A new agenda can't exist in between an already existing booked agenda
        with rx.session() as session:
            temp_agenda = session.exec(
                select(AgendaModel)
                .where((AgendaModel.from_date >= from_date))
                .where(AgendaModel.to_date <= to_date)
                .where(lookup_args)
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
                .where(lookup_args)
            ).one_or_none()
        if temp_agenda is not None:
            return {
                "status": True,
                "message": "The chosen dates are already booked !",
            }

        return {"status": False, "message": ""}

    @rx.event
    def handle_on_change_from_date(self, value):
        self.agenda_from_date = value
        # self.agenda_to_date = self.display_date_from_date(datetime.strptime(self.agenda_from_date, FORMAT_DATE)  + timedelta(days=1))

        start_date = self.date_string_to_datetime(
            date=self.agenda_from_date, date_origin="FROM"
        )
        end_date = self.date_string_to_datetime(date=self.agenda_to_date)
        self.is_valid_agenda = self.validate_entry_date(
            from_date=start_date, to_date=end_date
        )
        print(
            "handle_on_change_from_date: is valid date ", self.is_valid_agenda
        )

    @rx.event
    def handle_on_change_to_date(self, value):
        self.agenda_to_date = value

        start_date = self.date_string_to_datetime(
            date=self.agenda_from_date, date_origin="FROM"
        )
        end_date = self.date_string_to_datetime(date=self.agenda_to_date)
        self.is_valid_agenda = self.validate_entry_date(
            from_date=start_date, to_date=end_date
        )
        print("handle_on_change_to_date: is valid date ", self.is_valid_agenda)

    def display_date_from_date(self, date: datetime) -> str:
        return date.strftime(FORMAT_DATE)

    @rx.var(cache=False)
    def display_date(self) -> str:
        return datetime.now().strftime(
            FORMAT_DATE
        )  # format for the day YYYY-MM-DD

    def validate_entry_date(
        self, from_date: datetime, to_date: datetime
    ) -> bool:
        if to_date is None:
            to_date = from_date + timedelta(days=1)
            self.agenda_to_date = self.datetime_to_date_string(to_date)

        return (
            self.is_correct_dates(from_date=from_date, to_date=to_date)
            and not self.is_overlapping_agenda(
                from_date=from_date, to_date=to_date
            )["status"]
        )

    def handle_submit(self, form_data: dict):
        self.deactive_edit_mode_agenda()
        print(form_data)
        self.form_data = form_data

        country = self.form_data.pop("country")
        town = self.form_data.pop("town")

        from_date = self.date_string_to_datetime(
            self.form_data.pop("from_date"), date_origin="FROM"
        )  # get_datetime(self.form_data.pop("from_date"), START_TIME)
        to_date = self.date_string_to_datetime(
            self.form_data.pop("to_date")
        )  # get_datetime(self.form_data.pop("to_date"), END_TIME)

        if (
            self.validate_entry_date(from_date=from_date, to_date=to_date)
            and not self.edit_mode_agenda_active
        ):
            self.record_agenda_in_db(
                country=country,
                town=town,
                from_date=from_date,
                to_date=to_date,
            )

        elif (
            self.validate_entry_date(from_date=from_date, to_date=to_date)
            and self.edit_mode_agenda_active
        ):
            self.deactive_edit_mode_agenda()

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
