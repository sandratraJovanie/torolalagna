import django_filters
from django import forms

from etudiant.models import relation
from structure.models import *


ANNEE = [
    ('1ère Année', '1ère Année'),
    ('2ème Année', '2ème Année'),
    ('3ème Année', '3ème Année'),
    ('4ème Année', '4ème Année'),
    ('5ème Année', '5ème Année'),

]
ANNEE1 = [
    ('2ème Année', '2ème Année'),
    ('3ème Année', '3ème Année'),
    ('4ème Année', '4ème Année'),
    ('5ème Année', '5ème Année'),

]
SEMESTRE = [
    ('Semestre 1', 'Semestre 1'),
    ('Semestre 2', 'Semestre 2'),
    ('Semestre 3', 'Semestre 3'),
    ('Semestre 4', 'Semestre 4'),
    ('Semestre 5', 'Semestre 5'),
    ('Semestre 6', 'Semestre 6'),
    ('Semestre 7', 'Semestre 7'),
    ('Semestre 8', 'Semestre 8'),
    ('Semestre 9', 'Semestre 9'),
    ('Semestre 10', 'Semestre 10'),

]

ANNEE_MODELE = [
    ('2015-2016', '2015-2016'),
    ('2016-2017', '2016-2017'),
    ('2017-2018', '2017-2018'),
    ('2018-2019', '2018-2019'),
    ('2019-2020', '2019-2020'),
    ('2020-2021', '2020-2021'),
    ('2021-2022', '2021-2022'),
    ('2022-2023', '2022-2023'),
    ('2023-2024', '2023-2024'),
    ('2024-2025', '2024-2025'),
    ('2025-2026', '2025-2026'),
    ('2026-2027', '2026-2027'),
    ('2027-2028', '2027-2028'),
    ('2028-2029', '2028-2029'),
    ('2029-2030', '2029-2030'),

]


class relationFilter1(django_filters.FilterSet):
    annee_scolaire = django_filters.ChoiceFilter(label="Choisissez l'année universitaire", widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }),choices=ANNEE_MODELE)

class classeFilter1(django_filters.FilterSet):
    classe = django_filters.ChoiceFilter(label='Choisissez la classe', widget=forms.Select(attrs={
        'class': 'form-control mb-3 mx-auto p-2',
        'style':'width:50%'
    }), choices=ANNEE)

class classeFilter(django_filters.FilterSet):
    classe = django_filters.ChoiceFilter(label='Choisissez la classe', widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }), choices=ANNEE1)

class AnneeScolaireFilter(django_filters.FilterSet):
    annee_scolaire = django_filters.ChoiceFilter(label="Choisissez l'année universitaire", widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3',
    }),choices=ANNEE_MODELE)

class EcFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(label="Nom de l'EC", widget=forms.TextInput(attrs={
        'class': 'form-control mx-auto mb-3',
    }))

