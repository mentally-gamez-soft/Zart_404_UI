import reflex as rx

from Zart_404_UI.constantes import URLS


class NavState(rx.State):

    def to_home(self):
        return rx.redirect(URLS["home"])

    def to_about(self):
        return rx.redirect(URLS["about"])

    def to_pricing(self):
        return rx.redirect(URLS["pricing"])

    def to_contact(self):
        return rx.redirect(URLS["contact"])
