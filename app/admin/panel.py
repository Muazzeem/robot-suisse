from sqladmin import Admin, ModelView

from app.admin.auth import AdminAuth
from app.db.base import engine

# Import models
from app.company.models import (
    Company,
    CompanyTranslation,
    CompanySocial,
    CompanyLocation,
    CompanyIndustry,
    CompanyCertification,
)
from app.robots.models import Robot


def setup_admin(app):
    """Setup SQLAdmin panel with all models"""

    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key="SUPER_SECRET_KEY"),
    )

    # -------------------------------
    # Company view (everything inline)
    # -------------------------------
    class CompanyAdmin(ModelView, model=Company):
        column_list = [
            Company.slug,
            Company.type,
            Company.is_active,
            Company.created_at,
        ]

        form_columns = [
            Company.slug,
            Company.type,
            Company.is_active,
            Company.website,
            Company.logo,
            Company.banner,
            "translations",
            "socials",
            "locations",
            "industries",
            "certifications",
        ]

        inline_models = [
            (CompanyTranslation, {
                "form_columns": [
                    CompanyTranslation.language,
                    CompanyTranslation.name,
                    CompanyTranslation.description,
                ],
                "form_args": {
                    "language": {
                        "choices": [
                            ("en", "English"),
                            ("de-CH", "Deutsch (Schweiz)"),
                            ("fr-CH", "Français (Suisse)"),
                            ("it-CH", "Italiano (Svizzera)"),
                        ]
                    }
                }
            }),
            (CompanySocial, {"form_columns": [CompanySocial.platform, CompanySocial.url]}),
            (CompanyLocation, {"form_columns": [
                CompanyLocation.address,
                CompanyLocation.city,
                CompanyLocation.state,
                CompanyLocation.country,
                CompanyLocation.postal_code,
            ]}),
            (CompanyIndustry, {"form_columns": [CompanyIndustry.industry]}),
            (CompanyCertification, {"form_columns": [CompanyCertification.certification]}),
        ]

    class RobotAdmin(ModelView, model=Robot):
        column_list = [Robot.slug, Robot.name]

    # -------------------------------
    # Register all views
    # -------------------------------
    admin.add_view(CompanyAdmin)
    admin.add_view(RobotAdmin)

    return admin
