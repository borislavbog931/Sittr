import random
from django.core.management.base import BaseCommand
from services.models import Service, PetType
from caretakers.models import Caretaker
from requests.models import HireRequest
from reviews.models import Review
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with realistic data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        self.clear_data()

        self.stdout.write('Creating new data...')
        
        # Create PetTypes
        pet_types = [
            PetType.objects.create(name='Dog'),
            PetType.objects.create(name='Cat'),
            PetType.objects.create(name='Bird'),
        ]
        self.stdout.write('Pet types created.')

        # Create Services
        services = [
            Service.objects.create(name='Dog Walking', description='A walk in the park.', price=Decimal('25.00')),
            Service.objects.create(name='Pet Sitting', description='Full day pet sitting.', price=Decimal('100.00')),
            Service.objects.create(name='Grooming', description='Full grooming service.', price=Decimal('50.00')),
        ]
        self.stdout.write('Services created.')

        # Create Caretakers
        caretaker1 = Caretaker.objects.create(
            name='Liam Garcia',
            email='liam.garcia@example.com',
            phone_number='123-456-7890',
            city='New York',
            bio='I love animals and have been a caretaker for 5 years.',
            price_per_hour=Decimal('30.00'),
        )
        caretaker1.pet_types.add(pet_types[0], pet_types[1]) # Dogs and Cats
        caretaker1.services.add(services[0], services[1]) # Dog Walking and Pet Sitting
        self.stdout.write('Caretaker 1 created.')

        caretaker2 = Caretaker.objects.create(
            name='Olivia Martinez',
            email='olivia.martinez@example.com',
            phone_number='098-765-4321',
            city='Los Angeles',
            bio='Experienced with all kinds of birds.',
            price_per_hour=Decimal('40.00'),
        )
        caretaker2.pet_types.add(pet_types[2]) # Birds
        caretaker2.services.add(services[1], services[2]) # Pet Sitting and Grooming
        self.stdout.write('Caretaker 2 created.')

        # Create HireRequests
        HireRequest.objects.create(
            caretaker=caretaker1,
            client_name='Alice',
            pet_type=pet_types[0],
            service=services[0],
            start_date='2026-03-01',
            end_date='2026-03-05',
            status='new',
        )
        HireRequest.objects.create(
            caretaker=caretaker2,
            client_name='Bob',
            pet_type=pet_types[2],
            service=services[2],
            start_date='2026-03-10',
            end_date='2026-03-11',
            status='accepted',
        )
        self.stdout.write('Hire requests created.')

        # Create Reviews
        Review.objects.create(caretaker=caretaker1, reviewer_name='Charlie', rating=9, comment='Liam was great with my dog!')
        Review.objects.create(caretaker=caretaker1, reviewer_name='Diana', rating=10, comment='Excellent service.')
        Review.objects.create(caretaker=caretaker2, reviewer_name='Eve', rating=8, comment='Olivia took good care of my parrot.')
        Review.objects.create(caretaker=caretaker2, reviewer_name='Frank', rating=9, comment='Very professional and friendly.')
        self.stdout.write('Reviews created.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))

    def clear_data(self):
        Review.objects.all().delete()
        HireRequest.objects.all().delete()
        Caretaker.objects.all().delete()
        Service.objects.all().delete()
        PetType.objects.all().delete()
