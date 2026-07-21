from django.core.management.base import BaseCommand
from django.db.models import Q

from caretakers.models import Caretaker


class Command(BaseCommand):
    help = "Geocode city -> latitude/longitude for caretakers missing coordinates."

    def handle(self, *args, **options):
        caretakers = Caretaker.objects.filter(
            Q(latitude__isnull=True) | Q(longitude__isnull=True)
        )

        if not caretakers.exists():
            self.stdout.write(self.style.SUCCESS("Nothing to do — every caretaker already has coordinates."))
            return

        updated = 0
        for caretaker in caretakers:
            caretaker.save()  # save() re-geocodes automatically when lat/lng are missing
            if caretaker.latitude is not None and caretaker.longitude is not None:
                updated += 1
                self.stdout.write(f"Geocoded {caretaker.name} ({caretaker.city}) -> {caretaker.latitude}, {caretaker.longitude}")
            else:
                self.stdout.write(self.style.WARNING(f"Could not geocode {caretaker.name} ({caretaker.city})"))

        self.stdout.write(self.style.SUCCESS(f"Done. {updated} of {caretakers.count()} caretaker(s) geocoded."))
