import os
import uuid
import shutil
from wtforms import FileField
from sqladmin import Admin, ModelView
from app.admin.auth import AdminAuth
from app.db.base import engine
from app.company.models import Company, CompanyTranslation
from app.robots.models import Robot


UPLOAD_DIR = "uploads/companies"


def setup_admin(app):
    """Setup SQLAdmin panel with translations inline"""

    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key="SUPER_SECRET_KEY"),
    )

    class CompanyAdmin(ModelView, model=Company):
        column_list = [
            Company.defult_name,
            Company.slug,
            Company.type,
            Company.is_active,
            Company.created_at,
            Company.updated_at,
        ]

        form_columns = [
            Company.defult_name,
            Company.type,
            Company.is_active,
        ]

        # Inline translations → admin can add/edit per language directly
        inline_models = [CompanyTranslation]

    class CompanyTranslationAdmin(ModelView, model=CompanyTranslation):
        column_list = [
            CompanyTranslation.company_slug,
            CompanyTranslation.language,
            CompanyTranslation.name,
            CompanyTranslation.city,
            CompanyTranslation.country,
            CompanyTranslation.logo,
            CompanyTranslation.banner,
        ]

        # Render logo & banner as <input type="file">
        form_overrides = {
            "logo": FileField,
            "banner": FileField,
        }
        async def on_model_change(self, data, model, is_created, request):
            """Save uploaded files and update DB with path"""

            # Handle logo upload
            logo_file = data.get("logo")
            if logo_file and hasattr(logo_file, "file"):
                filename = f"{uuid.uuid4()}_{logo_file.filename}"
                filepath = os.path.join(UPLOAD_DIR, "logos", filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(logo_file.file, buffer)
                model.logo = filepath
                data["logo"] = filepath

            # Handle banner upload
            banner_file = data.get("banner")
            if banner_file and hasattr(banner_file, "file"):
                filename = f"{uuid.uuid4()}_{banner_file.filename}"
                filepath = os.path.join(UPLOAD_DIR, "banners", filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(banner_file.file, buffer)
                model.banner = filepath
                data["banner"] = filepath

            return await super().on_model_change(data, model, is_created, request)

    class RobotAdmin(ModelView, model=Robot):
        column_list = [Robot.slug, Robot.name, Robot.company_slug]

    # Register views
    admin.add_view(CompanyAdmin)
    admin.add_view(CompanyTranslationAdmin)
    admin.add_view(RobotAdmin)

    return admin
