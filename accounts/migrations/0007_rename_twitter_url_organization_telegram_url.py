# Generated by Django 5.2.2 on 2025-07-18 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_organization_facebook_url_organization_github_url_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="organization",
            old_name="twitter_url",
            new_name="telegram_url",
        ),
    ]
