# Generated by Django 5.2.2 on 2025-07-18 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_rename_descriptions_project_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="check_out_link",
            new_name="demo_url",
        ),
        migrations.AddField(
            model_name="project",
            name="github_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
