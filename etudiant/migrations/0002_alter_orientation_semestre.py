# Generated by Django 4.0.2 on 2022-02-08 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
        ('etudiant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orientation',
            name='semestre',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='structure.niveaux'),
        ),
    ]
