from django.core.management.base import BaseCommand
from wagtail.images.models import Image
from wagtail.models import Page
from home.models import CompanyPage, CompanyDetailPage
import requests
from io import BytesIO
from django.core.files import File
import json
import os

class Command(BaseCommand):
    help = "Create CompanyDetailPage from JSON data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--json-file',
            type=str,
            default='companies.json',
            help='Path to JSON file containing company data'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        # Check if file exists
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f"JSON file '{json_file}' not found"))
            return

        # Load JSON data
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                companies_data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON format: {e}"))
            return

        # Get the parent page
        parent = CompanyPage.objects.first()

        if not parent:
            self.stdout.write(self.style.ERROR("Parent CompanyPage not found"))
            return

        # Process each company
        created_count = 0
        failed_count = 0

        for company_data in companies_data:
            try:
                # Check if page already exists
                existing_page = CompanyDetailPage.objects.filter(title=company_data["name"]).first()
                if existing_page:
                    self.stdout.write(self.style.WARNING(f"Page '{company_data['name']}' already exists. Skipping..."))
                    continue
                # Build StreamField content
                body_content = [
                    {
                        "type": "company_header",
                        "value": {
                            "title": {
                                "en": company_data["name"]
                            },
                            "website": company_data.get("link", ""),
                            "email": company_data.get("email", ""),
                            "phone": company_data.get("phone", ""),
                        }
                    },
                    {
                        "type": "company_details",
                        "value": {
                            "description": {
                                "en": company_data.get("description", "")
                            }
                        }
                    },
                ]

                # Add contacts if they exist
                if company_data.get("contact_persons"):
                    body_content.append({
                        "type": "contacts",
                        "value": {
                            "contacts": [
                                {
                                    "name": {"en": p["name"]},
                                    "description": {"en": f"<h4>{p.get('job_title', '')}</h4><p>{p.get('email', '')}<br/>{p.get('phone', '')}</p>"},
                                    "avatar": p.get("avatar", "")
                                } for p in company_data["contact_persons"]
                            ]
                        }
                    })
                description = company_data.get("description", "")
                short_desc = description[:200] + ("..." if len(description) > 200 else "")    

                page = CompanyDetailPage(
                    title=company_data["name"],
                    company_name=[{"type": "name", "value": {"en": company_data["name"]}}],
                    short_description=[{"type": "description", "value": {"en": short_desc}}],
                    logo=company_data.get("logo"),
                    banner=company_data.get("banner_image"),
                    body=body_content
                )

                # Add page as child of parent
                parent.add_child(instance=page)
                page.save_revision().publish()
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Page '{page.title}' created successfully!"))

            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f"✗ Failed to create page for '{company_data.get('name', 'Unknown')}': {e}"))

        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Total companies processed: {len(companies_data)}"))
        self.stdout.write(self.style.SUCCESS(f"Successfully created: {created_count}"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"Failed: {failed_count}"))
