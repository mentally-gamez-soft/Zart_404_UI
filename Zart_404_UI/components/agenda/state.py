from datetime import datetime, timedelta
from typing import List, Tuple

import reflex as rx
import sqlalchemy.orm
from sqlmodel import select

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.models import AgendaModel, UserInfo
from Zart_404_UI.service import get_all_countries, get_cities_of_country
from Zart_404_UI.tools.utils import get_date_string, get_datetime

START_TIME = "00:00:00"
END_TIME = "23:59:59"
FORMAT_DATE = "%Y-%m-%d"


class AgendaFormState(rx.State):
    raw_countries = []
    _available_countries = []
    _available_countries_iso = []

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

        elif len(self._available_countries) == 0:
            self.raw_countries = get_all_countries()
            self._available_countries = [
                country["name"] for country in self.raw_countries
            ]
            self._available_countries_iso = [
                country["iso2"] for country in self.raw_countries
            ]

        if len(self.search_text) >= 3:
            return [
                option
                for option in self._available_countries
                if self.search_text.lower() in option.lower()
            ]
        else:
            return []

    # Additional management of a second field town
    _available_towns: list[str] = []
    search_towns: str = ""
    search_towns_is_focused: bool = False

    def get_available_towns(self, country: str) -> list[str]:
        idx = -1
        try:
            idx = self._available_countries.index(country)
        except:
            idx = -1

        if idx > 0:
            country_iso_code = self._available_countries_iso[idx]
            return get_cities_of_country(country_iso_2=country_iso_code)

        return []

    @rx.var(cache=False)
    def town_available_completions(self) -> list[str]:
        if (
            not self.search_towns_is_focused
            or self.search_towns == ""
            or self.search_towns in self._available_towns
        ):
            return []

        if len(self.search_towns) >= 5:
            return [
                option
                for option in self._available_towns
                if self.search_towns.lower() in option.lower()
            ]

        return []


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

    @rx.var(cache=True)
    def edit_from_date(self) -> str:
        return self.datetime_to_date_string(date=self.edit_agenda.from_date)

    @rx.var(cache=True)
    def edit_to_date(self) -> str:
        return self.datetime_to_date_string(date=self.edit_agenda.to_date)

    @rx.event
    def handle_click_speed_dial(self, index: int, action: str):
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
        self.edit_agenda = self.calendar[idx]

    def deactive_edit_mode_agenda(self):
        self.edit_mode_agenda_id = -1
        self.edit_mode_agenda_active = False
        self.edit_agenda = None

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

    def update_agenda(
        self, country: str, town: str, from_date: datetime, to_date: datetime
    ):
        with rx.session() as session:
            self.edit_agenda.country = country
            self.edit_agenda.town = town
            self.edit_agenda.from_date = from_date
            self.edit_agenda.to_date = to_date
            session.add(self.edit_agenda)
            session.commit()
            session.refresh(self.edit_agenda)

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
        if date == "":
            return None

        if date_origin in ("TO"):
            return get_datetime(date, END_TIME)
        return get_datetime(date, START_TIME)

    def datetime_to_date_string(self, date: datetime):
        return get_date_string(date)

    def is_correct_dates(self, from_date: datetime, to_date: datetime) -> bool:
        return from_date < to_date

    def is_overlapping_agenda(
        self, from_date: datetime, to_date: datetime, edit_mode: bool = False
    ) -> dict:
        """Get an agenda in between to 2 dates"""
        temp_agenda = None
        lookup_args = (
            (
                AgendaModel.userinfo_id == self.userinfo_id,
                AgendaModel.id != self.edit_agenda.id,
            )
            if edit_mode
            else (AgendaModel.userinfo_id == self.userinfo_id,)
        )

        # A new agenda can't exist in between an already existing booked agenda
        with rx.session() as session:
            temp_agenda = session.exec(
                select(AgendaModel)
                .where((AgendaModel.from_date >= from_date))
                .where(AgendaModel.to_date <= to_date)
                .where(*lookup_args)
            ).first()
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
                .where(*lookup_args)
            ).first()
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
        if from_date == "" or from_date is None:
            return False

        if to_date is None:
            to_date = from_date + timedelta(days=1)
            self.agenda_to_date = self.datetime_to_date_string(to_date)

        return (
            self.is_correct_dates(from_date=from_date, to_date=to_date)
            and not self.is_overlapping_agenda(
                from_date=from_date,
                to_date=to_date,
                edit_mode=self.edit_mode_agenda_active,
            )["status"]
        )

    @rx.event
    def handle_cancel(self):
        self.deactive_edit_mode_agenda

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data

        country = self.form_data.pop("country")
        town = self.form_data.pop("town")

        from_date = self.date_string_to_datetime(
            self.form_data.pop("from_date"), date_origin="FROM"
        )
        to_date = self.date_string_to_datetime(self.form_data.pop("to_date"))

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
            self.update_agenda(
                country=country,
                town=town,
                from_date=from_date,
                to_date=to_date,
            )

        self.deactive_edit_mode_agenda()
