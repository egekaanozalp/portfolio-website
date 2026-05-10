from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_flexible_info_grid"),
    ]

    operations = [
        migrations.CreateModel(
            name="SkillCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Skill Category",
                "verbose_name_plural": "Skill Categories",
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="skill",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skills",
                to="core.skillcategory",
            ),
        ),
    ]
