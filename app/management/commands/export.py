import json
from django.core.management.base import BaseCommand, CommandError
from app.models import Groups


class Command(BaseCommand):
    help = "Exports a LINE group chat history to Discord format"

    def add_arguments(self, parser):
        parser.add_argument("group_name")

    def handle(self, *args, **options):
        group_name = options["group_name"]
        try:
            group = Groups.objects.get(name__iexact=group_name)
        except Groups.DoesNotExist:
            raise CommandError(f'Group "{group_name}" does not exist')

        with open(f"{group_name}.json", "w") as f:
            json.dump(group.to_discord(), f, indent=2)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported group "{group.name}"')
        )
