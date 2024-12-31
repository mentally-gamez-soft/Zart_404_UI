import reflex as rx

from Zart_404_UI.constantes import URLS
from Zart_404_UI.pages.base_page import base_page

from .state import ContactState


@rx.page(route=URLS["contact"])
def contact_page() -> rx.Component:
    contact_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="first_name",
                    placeholder="First Name",
                    required=True,
                    width="100%",
                ),
                rx.input(
                    name="last_name",
                    placeholder="Last Name",
                    required=True,
                    width="100%",
                ),
                width="100%",
            ),
            rx.input(
                name="email",
                type="email",
                placeholder="johndoe@here.com",
                required=True,
                width="100%",
            ),
            rx.text_area(name="message", placeholder="Message", required=True),
            rx.button("Submit", type="submit"),
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=False,
    )

    return base_page(
        rx.vstack(
            rx.heading("Contact Us", size="9"),
            rx.cond(ContactState.form_submitted, ContactState.thank_you, ""),
            rx.desktop_only(rx.box(contact_form, width="50vw")),
            rx.mobile_and_tablet(contact_form, width="85vw"),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
            id="about-page",
        ),
    )
