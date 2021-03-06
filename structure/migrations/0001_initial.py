# Generated by Django 4.0.2 on 2022-02-08 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='etablissements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('adresse', models.CharField(max_length=100, verbose_name='Adresse')),
                ('ville', models.CharField(max_length=50, verbose_name='Nom de la ville')),
            ],
            options={
                'verbose_name': 'Etablissement',
                'verbose_name_plural': 'Etablissements',
            },
        ),
        migrations.CreateModel(
            name='mentions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('etablissement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.etablissements')),
            ],
            options={
                'verbose_name': 'Mention',
                'verbose_name_plural': 'Mentions',
            },
        ),
        migrations.CreateModel(
            name='niveaux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('classe', models.CharField(choices=[('1ère Année', '1ère Année'), ('2ème Année', '2ème Année'), ('3ème Année', '3ème Année'), ('4ème Année', '4ème Année'), ('5ème Année', '5ème Année')], max_length=20, verbose_name='Classe')),
            ],
            options={
                'verbose_name': 'Niveau',
                'verbose_name_plural': 'Niveaux',
            },
        ),
        migrations.CreateModel(
            name='parcours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('mention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.mentions')),
            ],
            options={
                'verbose_name': 'Parcours',
                'verbose_name_plural': 'Parcours',
            },
        ),
        migrations.CreateModel(
            name='ue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('annee_scolaire', models.CharField(choices=[('2015-2016', '2015-2016'), ('2016-2017', '2016-2017'), ('2017-2018', '2017-2018'), ('2018-2019', '2018-2019'), ('2019-2020', '2019-2020'), ('2020-2021', '2020-2021'), ('2021-2022', '2021-2022'), ('2022-2023', '2022-2023'), ('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030')], max_length=20, verbose_name='Année scolaire')),
                ('classe', models.CharField(choices=[('1ère Année', '1ère Année'), ('2ème Année', '2ème Année'), ('3ème Année', '3ème Année'), ('4ème Année', '4ème Année'), ('5ème Année', '5ème Année')], max_length=20, verbose_name='Classe')),
                ('credit', models.IntegerField(verbose_name='Crédit')),
                ('isValid', models.BooleanField(default=False, verbose_name='Validé')),
                ('niveaux', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.niveaux')),
                ('parcours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.parcours')),
            ],
            options={
                'verbose_name': 'UE',
                'verbose_name_plural': 'UE',
            },
        ),
        migrations.CreateModel(
            name='ec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('annee_scolaire', models.CharField(choices=[('2015-2016', '2015-2016'), ('2016-2017', '2016-2017'), ('2017-2018', '2017-2018'), ('2018-2019', '2018-2019'), ('2019-2020', '2019-2020'), ('2020-2021', '2020-2021'), ('2021-2022', '2021-2022'), ('2022-2023', '2022-2023'), ('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030')], max_length=20, verbose_name='Année scolaire')),
                ('classe', models.CharField(choices=[('1ère Année', '1ère Année'), ('2ème Année', '2ème Année'), ('3ème Année', '3ème Année'), ('4ème Année', '4ème Année'), ('5ème Année', '5ème Année')], max_length=20, verbose_name='Classe')),
                ('coefficient', models.IntegerField(verbose_name='Coefficient')),
                ('isValid', models.BooleanField(default=False, verbose_name='Validé')),
                ('niveaux', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.niveaux')),
                ('ue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.ue')),
            ],
            options={
                'verbose_name': 'EC',
                'verbose_name_plural': 'EC',
            },
        ),
    ]
