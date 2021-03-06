# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-27 16:47
from __future__ import unicode_literals

import citation.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citation', '0008_add_reviewed_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='orcid',
            field=citation.fields.NonEmptyTextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='researcherid',
            field=citation.fields.NonEmptyTextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='type',
            field=models.TextField(choices=[('INDIVIDUAL', 'individual'), ('ORGANIZATION', 'organization')], default='INDIVIDUAL', max_length=64),
        ),
        migrations.AlterField(
            model_name='container',
            name='eissn',
            field=citation.fields.NonEmptyTextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='container',
            name='issn',
            field=citation.fields.NonEmptyTextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=citation.fields.NonEmptyTextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='isi',
            field=citation.fields.NonEmptyTextField(max_length=255, null=True),
        ),
    ]
