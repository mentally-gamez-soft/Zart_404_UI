import reflex as rx
import reflex_local_auth

from Zart_404_UI.constantes import URLS


class NavState(rx.State):

    def to_register(self):
        return rx.redirect(reflex_local_auth.routes.REGISTER_ROUTE)

    def to_login(self):
        return rx.redirect(reflex_local_auth.routes.LOGIN_ROUTE)

    def to_logout(self):
        return rx.redirect(URLS["logout"])

    def to_home(self):
        return rx.redirect(URLS["home"])

    def to_blogs(self):
        return rx.redirect(URLS["blogs"])

    def to_add_blog_post(self):
        return rx.redirect(URLS["add_blog_post"])

    def to_create_blog(self):
        return self.to_add_blog_post()

    def to_about(self):
        return rx.redirect(URLS["about"])

    def to_pricing(self):
        return rx.redirect(URLS["pricing"])

    def to_contact(self):
        return rx.redirect(URLS["contact"])
