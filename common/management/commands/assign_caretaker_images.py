from django.core.management.base import BaseCommand

from caretakers.models import Caretaker


DEMO_CARETAKER_IMAGES = (
    "caretakers/woman1.png",
    "caretakers/man1.png",
    "caretakers/woman2.png",
    "caretakers/man2.png",
    "caretakers/woman3.png",
    "caretakers/man3.png",
    "caretakers/man4.png",
    "caretakers/man5.png",
    "caretakers/man6.png",
)


class Command(BaseCommand):
    help = "Assign demo media images to caretakers that do not already have a profile picture."

    def handle(self, *args, **kwargs):
        caretakers = Caretaker.objects.order_by("pk")
        updated = 0

        for index, caretaker in enumerate(caretakers):
            if caretaker.profile_pic:
                continue

            caretaker.profile_pic = DEMO_CARETAKER_IMAGES[index % len(DEMO_CARETAKER_IMAGES)]
            caretaker.save(update_fields=["profile_pic"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Assigned images to {updated} caretaker(s)."))
