from django.contrib.auth.models import User
from django.test import TestCase

from citation.models import AuditCommand, Container, Publication


class PublicationYearPublishedTests(TestCase):
    """Covers year_published derivation from the range of date_published_text
    formats produced by bibtex import, crossref lookups, zotero import, and
    manual entry (see bibtex/entry/api.py, bibtex/ref/api.py,
    management/commands/zotero_import.py)."""

    # (date_published_text, expected year_published)
    CASES = (
        ("2019", 2019),  # bibtex/crossref plain year
        ("", None),  # blank field
        ("n.d.", None),  # no date available
        ("in press", None),  # forthcoming, no year yet
        ("2019-01-15", 2019),  # zotero ISO date
        ("January 15, 2019", 2019),  # zotero long-form date
        ("circa 1998", 1998),  # approximate date
        ("\u00a9 2020", 2020),  # copyright-prefixed year
        ("2019-2020", 2019),  # year range, first match wins
        ("Presented 2019, published 2020", 2019),  # multiple years, first match wins
        ("Vol. 12, No. 3 (2019)", 2019),  # year alongside other short numbers
        ("   ", None),  # whitespace only
        ("ISBN 1201995", None),  # 4-digit run embedded in a longer digit run
        ("Report No. 1234", 1234),  # known limitation: any bare 4-digit token matches
        # observed in production catalog.sql (citation_publication.date_published_text):
        ("JUN 2014", 2014),  # all-caps abbreviated month
        ("OCT-DEC 2014", 2014),  # all-caps abbreviated month range
        ("MAY 14 2002", 2002),  # all-caps abbreviated month, day, year (no comma)
        ("1008", 1008),  # known limitation: implausible year still matches, e.g. data-entry typo for 2008
    )

    def setUp(self):
        self.user = User.objects.create_user(username="year-published-user")
        self.container = Container.objects.create(name="Year Published Journal")

    def test_year_published_derivation_across_date_formats(self):
        for date_published_text, expected_year in self.CASES:
            with self.subTest(date_published_text=date_published_text):
                publication = Publication.objects.create(
                    title="Sample",
                    date_published_text=date_published_text,
                    added_by=self.user,
                    container=self.container,
                )
                publication.refresh_from_db()
                self.assertEqual(publication.year_published, expected_year)

    def test_year_published_recomputed_on_update(self):
        publication = Publication.objects.create(
            title="Sample",
            date_published_text="2019",
            added_by=self.user,
            container=self.container,
        )
        self.assertEqual(publication.year_published, 2019)

        publication.date_published_text = "2021"
        publication.save()
        publication.refresh_from_db()
        self.assertEqual(publication.year_published, 2021)

    def test_year_published_recomputed_via_log_update(self):
        publication = Publication.objects.create(
            title="Sample",
            date_published_text="2019",
            added_by=self.user,
            container=self.container,
        )
        audit_command = AuditCommand.objects.create(
            creator=self.user, action=AuditCommand.Action.MANUAL
        )

        publication.log_update(audit_command=audit_command, date_published_text="2022")
        publication.refresh_from_db()
        self.assertEqual(publication.year_published, 2022)
