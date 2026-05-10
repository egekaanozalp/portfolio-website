from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_add_aboutsection"),
    ]

    operations = [
        migrations.RemoveField(model_name="aboutsection", name="specialization"),
        migrations.RemoveField(model_name="aboutsection", name="experience_level"),
        migrations.RemoveField(model_name="aboutsection", name="education"),
        migrations.RemoveField(model_name="aboutsection", name="languages"),
        migrations.AddField(model_name="aboutsection", name="info1_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 1 label")),
        migrations.AddField(model_name="aboutsection", name="info1_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 1 value")),
        migrations.AddField(model_name="aboutsection", name="info2_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 2 label")),
        migrations.AddField(model_name="aboutsection", name="info2_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 2 value")),
        migrations.AddField(model_name="aboutsection", name="info3_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 3 label")),
        migrations.AddField(model_name="aboutsection", name="info3_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 3 value")),
        migrations.AddField(model_name="aboutsection", name="info4_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 4 label")),
        migrations.AddField(model_name="aboutsection", name="info4_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 4 value")),
        migrations.AddField(model_name="aboutsection", name="info5_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 5 label")),
        migrations.AddField(model_name="aboutsection", name="info5_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 5 value")),
        migrations.AddField(model_name="aboutsection", name="info6_label", field=models.CharField(blank=True, default="", max_length=100, verbose_name="Item 6 label")),
        migrations.AddField(model_name="aboutsection", name="info6_value", field=models.CharField(blank=True, default="", max_length=200, verbose_name="Item 6 value")),
    ]
