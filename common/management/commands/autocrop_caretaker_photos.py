from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from PIL import Image

from caretakers.models import Caretaker
from common.image_utils import autocrop_blank_margin


class Command(BaseCommand):
    help = (
        "Auto-crop the blank background margin around a caretaker's profile "
        "photo. Writes a '<name>_cropped<ext>' copy next to the original by "
        "default; pass --apply to overwrite the caretaker's actual photo."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--caretaker",
            help="Slug of a single caretaker to process. Omit to process every caretaker with a photo.",
        )
        parser.add_argument(
            "--padding", type=int, default=10,
            help="Padding in pixels kept around the detected subject (default: 10).",
        )
        parser.add_argument(
            "--threshold", type=int, default=30,
            help="Sensitivity for detecting the background color (default: 30).",
        )
        parser.add_argument(
            "--apply", action="store_true",
            help="Overwrite the original photo instead of writing a '_cropped' copy.",
        )

    def handle(self, *args, **options):
        caretakers = Caretaker.objects.exclude(profile_pic="").order_by("name")
        if options["caretaker"]:
            caretakers = caretakers.filter(slug=options["caretaker"])
            if not caretakers.exists():
                raise CommandError(f"No caretaker with slug '{options['caretaker']}' has a photo.")

        processed = 0
        for caretaker in caretakers:
            source_path = Path(caretaker.profile_pic.path)
            if not source_path.exists():
                self.stdout.write(self.style.WARNING(f"Skipping {caretaker.name}: file not found ({source_path})"))
                continue

            with Image.open(source_path) as image:
                cropped = autocrop_blank_margin(image, padding=options["padding"], threshold=options["threshold"])

                if cropped.size == image.size:
                    self.stdout.write(f"{caretaker.name}: no blank margin detected, skipped.")
                    continue

                if options["apply"]:
                    cropped.save(source_path)
                    self.stdout.write(self.style.SUCCESS(
                        f"{caretaker.name}: cropped {image.size} -> {cropped.size}, saved in place."
                    ))
                else:
                    out_path = source_path.with_name(f"{source_path.stem}_cropped{source_path.suffix}")
                    cropped.save(out_path)
                    self.stdout.write(self.style.SUCCESS(
                        f"{caretaker.name}: cropped {image.size} -> {cropped.size}, saved to {out_path.name}."
                    ))

            processed += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {processed} caretaker photo(s)."))
