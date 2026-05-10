from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_skillcategory"),
    ]

    operations = [
        migrations.RemoveField(model_name="skill", name="percentage"),
        migrations.AddField(
            model_name="skill",
            name="rating",
            field=models.PositiveSmallIntegerField(
                default=3,
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
            ),
        ),
    ]
