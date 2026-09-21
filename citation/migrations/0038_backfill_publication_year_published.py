import re

from django.db import migrations

YEAR_PUBLISHED_REGEX = re.compile(r"(?<!\d)\d{4}(?!\d)")


def backfill_year_published(apps, schema_editor):
    Publication = apps.get_model("citation", "Publication")
    updates = []
    for pub in Publication.objects.exclude(date_published_text="").iterator():
        match = YEAR_PUBLISHED_REGEX.search(pub.date_published_text)
        year = int(match.group(0)) if match else None
        if year is not None:
            pub.year_published = year
            updates.append(pub)
    Publication.objects.bulk_update(updates, ["year_published"], batch_size=1000)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("citation", "0037_publication_year_published"),
    ]

    operations = [
        migrations.RunPython(backfill_year_published, noop),
    ]
