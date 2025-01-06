from typing import Optional

import reflex as rx
import reflex_local_auth
import sqlmodel

from .models import UserInfo


class UserSessionState(reflex_local_auth.LocalAuthState):

    @rx.var(cache=True)
    def authenticated_username(self) -> str:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username.capitalize()

    @rx.var(cache=True)
    def authenticated_user_info(self) -> Optional[UserInfo]:
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            result = session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()

            if result is None:
                return None
            print(result)
            local_user = result.local_user
            # print(self.user_name)
            return result

    def on_load(self):
        # if not self.is_authenticated:
        #    return reflex_local_auth.LoginState.register
        print(self.authenticated_user_info)
        print(self.authenticated_user_info.local_user)

    def execute_logout(self):
        self.do_logout()
        self.user_name = None
        return rx.redirect("/")


class CustomRegisterState(reflex_local_auth.RegistrationState):
    # This event handler must be named something besides `handle_registration`!!!
    def handle_registration_email(self, form_data):
        registration_result = self.handle_registration(form_data)
        if self.new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        created_from_ip="0.0.0.0",  # self.router.headers.get(                   "x_forwarded_for",                self.router.session.client_ip,   ),
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return registration_result
