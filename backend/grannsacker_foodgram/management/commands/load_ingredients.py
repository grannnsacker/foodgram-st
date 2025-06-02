import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from grannsacker_foodgram.models import Ingredient


class Command(BaseCommand):
    help = "Load ingredients from JSON file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to JSON file with ingredients data"
        )

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                ingredients_data = json.load(f)

                if not isinstance(ingredients_data, list):
                    raise ValueError("JSON data should be an array")

                created_count = 0
                for item in ingredients_data:
                    try:
                        _, created = Ingredient.objects.get_or_create(
                            name=item["name"], measurement_unit=item["measurement_unit"]
                        )
                        if created:
                            created_count += 1
                    except KeyError as e:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Missing required field {e} in item: {item}"
                            )
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Ingredient already exists: {item['name']}"
                            )
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Loaded {created_count} new ingredients\n"
                        f"Total ingredients now: {Ingredient.objects.count()}"
                    )
                )

        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"Invalid JSON format in file {file_path}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing file: {str(e)}"))
