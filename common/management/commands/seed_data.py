import random
from django.core.management.base import BaseCommand
from services.models import Service, PetType
from caretakers.models import Caretaker
from requests.models import HireRequest
from reviews.models import Review
from decimal import Decimal
from faker import Faker


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
    help = 'Seeds the database with realistic data.'

    def add_arguments(self, parser):
        parser.add_argument('--caretakers', type=int, default=10)
        parser.add_argument('--reviews', type=int, default=25)
        parser.add_argument('--requests', type=int, default=2)
        parser.add_argument(
            '--append',
            action='store_true',
            help='Append data instead of clearing existing records first.',
        )

    def handle(self, *args, **kwargs):
        num_caretakers = kwargs['caretakers']
        num_reviews = kwargs['reviews']
        num_requests = kwargs['requests']
        append_mode = kwargs['append']

        if not append_mode:
            self.stdout.write('Clearing old data...')
            self.clear_data()

        fake = Faker()
        self.stdout.write('Creating new data...')

        pet_types = self.ensure_pet_types()
        services = self.ensure_services()
        all_caretakers = list(Caretaker.objects.all())

        start_index = len(all_caretakers)
        for index in range(num_caretakers):
            caretaker = self.create_caretaker(
                fake=fake,
                pet_types=pet_types,
                services=services,
                image_index=start_index + index,
            )
            all_caretakers.append(caretaker)
        self.stdout.write(f'{num_caretakers} Caretakers created.')

        if all_caretakers and pet_types and services:
            for _ in range(num_requests):
                self.create_hire_request(fake, all_caretakers)
            self.stdout.write(f'{num_requests} Hire requests created.')
        else:
            self.stdout.write('Not enough data to create hire requests.')


        for _ in range(num_reviews):
            self.create_review(fake, all_caretakers)
        self.stdout.write(f'{num_reviews} Reviews created.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))

    def ensure_pet_types(self):
        pet_type_names = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Hamster', 'Fish', 'Reptile', 'Guinea Pig']
        pet_types = []
        created = 0

        for name in pet_type_names:
            pet_type, was_created = PetType.objects.get_or_create(name=name)
            pet_types.append(pet_type)
            created += int(was_created)

        self.stdout.write(f'{created} Pet types created.')
        return pet_types

    def ensure_services(self):
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
        created = 0

        for name, desc in service_data:
            service, was_created = Service.objects.get_or_create(
                name=name,
                defaults={'description': desc},
            )
            services.append(service)
            created += int(was_created)

        self.stdout.write(f'{created} Services created.')
        return services

    def create_caretaker(self, fake, pet_types, services, image_index):
        intro_sentences = [
            "A lifelong animal lover, I've been caring for pets for over 10 years.",
            "Passionate about paws and purrs, I offer dedicated and loving pet care.",
            "Your furry, feathered, or scaled friends are in safe hands with me!",
            "Experienced and reliable, I provide top-notch care for all types of pets.",
            "I believe every pet deserves the best, and I strive to provide just that.",
        ]
        outro_sentences = [
            "I look forward to meeting your beloved companions!",
            "References available upon request.",
            "Let's chat about how I can help care for your pets.",
            "Dedicated to providing peace of mind for pet parents.",
            "Committed to the well-being and happiness of your pets.",
        ]

        name = fake.unique.name()
        city = fake.city()
        caretaker = Caretaker.objects.create(
            name=name,
            email=fake.unique.email(),
            phone_number=self.fit_phone_number(fake.phone_number()),
            city=city,
            bio=(
                f"{random.choice(intro_sentences)} "
                f"{fake.paragraph(nb_sentences=3, variable_nb_sentences=True)} "
                f"{random.choice(outro_sentences)}"
            ),
            price_per_hour=Decimal(random.randint(20, 50)),
            active=fake.boolean(chance_of_getting_true=80),
            profile_pic=DEMO_CARETAKER_IMAGES[image_index % len(DEMO_CARETAKER_IMAGES)],
        )
        caretaker.pet_types.add(*random.sample(pet_types, random.randint(1, len(pet_types))))
        caretaker.services.add(*random.sample(services, random.randint(1, len(services))))
        return caretaker

    def create_hire_request(self, fake, caretakers):
        caretaker = random.choice(caretakers)
        caretaker_pet_types = list(caretaker.pet_types.all())
        caretaker_services = list(caretaker.services.all())
        start_date = fake.date_between(start_date='+3d', end_date='+30d')
        end_date = fake.date_between(start_date=start_date, end_date='+40d')

        HireRequest.objects.create(
            caretaker=caretaker,
            client_name=fake.name(),
            client_email=fake.email(),
            client_phone=self.fit_phone_number(fake.phone_number()),
            pet_type=random.choice(caretaker_pet_types),
            service=random.choice(caretaker_services),
            start_date=start_date,
            end_date=end_date,
            notes=fake.sentence(nb_words=12),
            status=random.choice([
                HireRequest.STATUS_NEW,
                HireRequest.STATUS_REVIEWED,
                HireRequest.STATUS_ACCEPTED,
                HireRequest.STATUS_REJECTED,
            ]),
        )

    def create_review(self, fake, caretakers):
        caretaker = random.choice(caretakers)

        positive_comments = [
            "Absolutely wonderful! Our pet loved their time with {caretaker_name}.",
            "Highly recommend! {caretaker_name} was punctual and very caring.",
            "Fantastic service. {caretaker_name} went above and beyond.",
            "Our pet was so happy and well-cared for. Thank you, {caretaker_name}!",
            "Excellent communication and reliable. Will definitely rebook with {caretaker_name}.",
            "Professional and kind. {caretaker_name} made us feel at ease.",
            "The best pet sitter we've ever had! {caretaker_name} is truly amazing.",
            "Very attentive and our pet felt comfortable right away with {caretaker_name}.",
        ]
        neutral_comments = [
            "Good service overall. {caretaker_name} did what was expected.",
            "Reliable, no major issues. {caretaker_name} took care of things.",
            "Competent and efficient. {caretaker_name} got the job done.",
        ]
        critical_comments = [
            "Service was okay, but communication could be improved with {caretaker_name}.",
            "Our pet was fine, but felt {caretaker_name} could have been more engaging.",
            "Some minor issues, but {caretaker_name} addressed them eventually.",
        ]

        comment_type = random.choices(['positive', 'neutral', 'critical'], weights=[0.7, 0.2, 0.1], k=1)[0]
        if comment_type == 'positive':
            comment_template = random.choice(positive_comments)
            rating = random.randint(8, 10)
        elif comment_type == 'neutral':
            comment_template = random.choice(neutral_comments)
            rating = random.randint(6, 7)
        else:
            comment_template = random.choice(critical_comments)
            rating = random.randint(4, 6)

        Review.objects.create(
            caretaker=caretaker,
            reviewer_name=fake.name(),
            rating=rating,
            comment=comment_template.format(caretaker_name=caretaker.name) + " " + fake.sentence(nb_words=10),
        )

    def fit_phone_number(self, phone_number):
        return phone_number[:20]

    def clear_data(self):
        Review.objects.all().delete()
        HireRequest.objects.all().delete()
        Caretaker.objects.all().delete()
        Service.objects.all().delete()
        PetType.objects.all().delete()
