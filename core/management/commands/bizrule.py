from django.core.management.base import BaseCommand

from core.biz_rule import main


class Command(BaseCommand):
    help = "Ingests Random API Data"

    def handle(self, *args, **options):
        main()

        self.stdout.write(self.style.SUCCESS('Successfully run'))
