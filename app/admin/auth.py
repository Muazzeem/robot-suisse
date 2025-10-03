from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Called when user submits the login form"""
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        # ⚠️ Replace with your own user check (DB, env vars, etc.)
        if username == "admin" and password == "secret":
            request.session.update({"user": username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Called when user clicks logout"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Called on each request to check if user is logged in"""
        return "user" in request.session
