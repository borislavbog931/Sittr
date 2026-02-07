import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from services.models import Service, PetType
from caretakers.models import Caretaker
from requests.models import HireRequest
from reviews.models import Review
from decimal import Decimal
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with realistic data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        self.clear_data()

        self.stdout.write('Creating new data...')
        fake = Faker()

        # Create PetTypes
        pet_type_names = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Hamster', 'Fish', 'Reptile', 'Guinea Pig']
        pet_types = []
        for name in pet_type_names:
            pet_types.append(PetType.objects.create(name=name))
        self.stdout.write(f'{len(pet_types)} Pet types created.')

        # Create Services
        service_data = [
            ('Dog Walking', 'A refreshing walk in the park or neighborhood.'),
            ('Pet Sitting (Daily)', 'Full day pet sitting at your home or ours.'),
            ('Grooming (Basic)', 'Basic grooming including bath, brush, and nail trim.'),
            ('Overnight Care', 'Overnight stay at your home for extended care.'),
            ('Vet Visit Transport', 'Safe and reliable transport to and from vet appointments.'),
            ('Basic Training', 'Introduction to basic commands and good behavior.'),
            ('Fish Feeding', 'Daily feeding and tank check for aquatic pets.'),
            ('Puppy Socialization', 'Help your puppy learn to interact with other dogs and people.'),
        ]
        services = []
        for name, desc in service_data:
            services.append(Service.objects.create(name=name, description=desc))
        self.stdout.write(f'{len(services)} Services created.')

        # Create Caretakers
        all_caretakers = []
        num_caretakers = 10
        for _ in range(num_caretakers):
            name = fake.name()
            caretaker = Caretaker.objects.create(
                name=name,
                email=fake.email(),
                phone_number=fake.phone_number(),
                city=fake.city(),
                bio=fake.paragraph(nb_sentences=5, variable_nb_sentences=True),
                price_per_hour=Decimal(random.randint(20, 50)),
                active=fake.boolean(chance_of_getting_true=80)
            )
            # Assign random pet types
            num_pet_types = random.randint(1, len(pet_types))
            caretaker.pet_types.add(*random.sample(pet_types, num_pet_types))
            
            # Assign random services
            num_services = random.randint(1, len(services))
            caretaker.services.add(*random.sample(services, num_services))
            all_caretakers.append(caretaker)
        self.stdout.write(f'{num_caretakers} Caretakers created.')

        # Create HireRequests - keeping initial two for now, as per instruction to skip expanding this point
        if all_caretakers and pet_types and services:
            HireRequest.objects.create(
                caretaker=all_caretakers[0],
                client_name=fake.name(),
                pet_type=random.choice(pet_types),
                service=random.choice(services),
                start_date=fake.date_between(start_date='+5d', end_date='+10d'),
                end_date=fake.date_between(start_date='+11d', end_date='+15d'),
                status='new',
            )
            HireRequest.objects.create(
                caretaker=all_caretakers[1],
                client_name=fake.name(),
                pet_type=random.choice(pet_types),
                service=random.choice(services),
                start_date=fake.date_between(start_date='+15d', end_date='+20d'),
                end_date=fake.date_between(start_date='+21d', end_date='+25d'),
                status='accepted',
            )
            self.stdout.write('Initial Hire requests created.')
        else:
            self.stdout.write('Not enough data to create initial hire requests.')


        # Create Reviews
        num_reviews = 25
        for _ in range(num_reviews):
            caretaker = random.choice(all_caretakers)
            Review.objects.create(
                caretaker=caretaker,
                reviewer_name=fake.name(),
                rating=random.randint(7, 10),
                comment=fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            )
        self.stdout.write(f'{num_reviews} Reviews created.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))

    def clear_data(self):
        Review.objects.all().delete()
        HireRequest.objects.all().delete()
        Caretaker.objects.all().delete()
        Service.objects.all().delete()
        PetType.objects.all().delete()
