import csv
from io import StringIO

from django.contrib.auth.models import User
from django.test import TestCase

from citation.export_data import PublicationCSVExporter
from citation.models import Author, Container, Publication, PublicationAuthors


class PublicationCSVExporterTests(TestCase):
    # commas are intentional: exercises CSV field quoting/escaping
    PUBLICATION_TITLE = "Model, with comma"
    CONTAINER_NAME = "Journal, with comma"
    CONTAINER_ISSN = "1234-5678"
    AUTHORS = (("Ada", "Zephyr"), ("Grace", "Alpha"))
    EXPECTED_AUTHOR_NAMES = "Grace Alpha; Ada Zephyr"

    def setUp(self):
        user = User.objects.create_user(username="csv-export-user")
        container = Container.objects.create(
            name=self.CONTAINER_NAME,
            issn=self.CONTAINER_ISSN,
        )
        publication = Publication.objects.create(
            title=self.PUBLICATION_TITLE,
            date_published_text="2019",
            container=container,
            added_by=user,
        )
        for given_name, family_name in self.AUTHORS:
            author = Author.objects.create(
                given_name=given_name,
                family_name=family_name,
                type=Author.INDIVIDUAL,
            )
            PublicationAuthors.objects.create(
                publication=publication,
                author=author,
                role=PublicationAuthors.RoleChoices.AUTHOR,
            )

    def test_rejects_nested_many_to_many_attribute_paths(self):
        self.assertTrue(PublicationCSVExporter.attribute_exists("platforms"))
        self.assertFalse(PublicationCSVExporter.attribute_exists("platforms__name"))

        with self.assertRaisesRegex(AttributeError, "platforms__name"):
            PublicationCSVExporter(attributes=["platforms__name"])

    def test_write_and_stream_keep_each_publication_in_one_csv_row(self):
        attributes = [
            "id",
            "title",
            "author_names",
            "container__issn",
            "container__name",
        ]
        exporter = PublicationCSVExporter(attributes=attributes)
        output = StringIO()

        exporter.write_all(output)
        written_rows = list(csv.reader(StringIO(output.getvalue())))
        streamed_rows = list(csv.reader(StringIO("".join(exporter.stream()))))

        self.assertEqual(written_rows, streamed_rows)
        self.assertEqual(written_rows[0], attributes)
        self.assertEqual(len(written_rows), 2)
        self.assertTrue(all(len(row) == len(attributes) for row in written_rows))
        self.assertEqual(written_rows[1][1], self.PUBLICATION_TITLE)
        self.assertEqual(written_rows[1][2], self.EXPECTED_AUTHOR_NAMES)
        self.assertEqual(written_rows[1][3], self.CONTAINER_ISSN)
        self.assertEqual(written_rows[1][4], self.CONTAINER_NAME)
