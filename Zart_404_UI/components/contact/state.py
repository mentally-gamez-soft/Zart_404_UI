import asyncio

import reflex as rx

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.models import ContactEntryModel


class ContactState(UserSessionState):
    form_data: dict = {}
    form_submitted: bool = False

    def is_valid_form(self) -> bool:
        """Validate the form."""
        return all(
            self.form_data.get(field)
            for field in ["first_name", "last_name", "email", "message"]
        )

    @rx.var(cache=False)
    def thank_you(self) -> str:
        return "Thank {} you for your submission!".format(
            self.form_data.get("first_name", "")
        )

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        if self.is_valid_form():
            with rx.session() as session:
                contact_entry = ContactEntryModel(**form_data)
                session.add(contact_entry)
                session.commit()

                self.form_submitted = True
                yield

            await asyncio.sleep(0.5)
            self.form_submitted = False
            yield
