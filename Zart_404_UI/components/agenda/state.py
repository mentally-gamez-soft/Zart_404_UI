from datetime import datetime
from typing import List, Tuple

import reflex as rx

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.tools.utils import get_datetime

START_TIME = "00:00:00"
END_TIME = "23:59:59"


class AgendaState(UserSessionState):
    form_data: dict = {}
    agenda: List[Tuple[Tuple[str, str], Tuple[datetime, datetime]]] = (
        []
    )  # [("Paris",("2024-01-01", "20240201"))]

    def add_entry_to_agenda(
        self, country: str, town: str, start_date: datetime, end_date: datetime
    ) -> dict:
        return self.agenda.append(((country, town), (start_date, end_date)))

    def delete_entry_from_agenda(
        self, country: str, town: str, start_date: datetime, end_date: datetime
    ) -> dict:
        return self.agenda.remove(((country, town), (start_date, end_date)))

    @rx.var
    def display_date(self) -> str:
        return datetime.now().strftime(
            "%Y-%m-%d"
        )  # format for the day YYYY-MM-DD

    def validate_entry_data(
        self, start_date: datetime, end_date: datetime
    ) -> bool:
        return start_date < end_date

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print("form_data submitted: ", form_data)
        print("agenda avant update:", self.agenda)

        start_date = get_datetime(self.form_data.pop("start_date"), START_TIME)
        end_date = get_datetime(self.form_data.pop("end_date"), END_TIME)

        if self.validate_entry_data(start_date=start_date, end_date=end_date):
            self.add_entry_to_agenda(
                country=self.form_data.pop("country"),
                town=self.form_data.pop("town"),
                start_date=start_date,
                end_date=end_date,
            )
            print("agenda apres update:", self.agenda)

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
