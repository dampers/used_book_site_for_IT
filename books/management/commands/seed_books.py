import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from books import models as book_models


class Command(BaseCommand):

    help = "This command creates books"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many books you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_user = user_models.User.objects.all()
        seeder.add_entity(
            book_models.Book,
            number,
            {
                "seller": lambda x: random.choice(all_user),
                "price": lambda x: random.randint(0, 50000),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for pk in created_clean:
            book = book_models.Book.objects.get(pk=pk)
            for i in range(3, 15):
                book_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    book=book,
                    file=f"/book_photos/{random.randint(1,31)}.webp",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} books created!"))
