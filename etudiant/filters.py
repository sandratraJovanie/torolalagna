import django_filters
from django import forms

from .models import *
ANNEE = [
    ('1ère Année', '1ère Année'),
    ('2ème Année', '2ème Année'),
    ('3ème Année', '3ème Année'),
    ('4ème Année', '4ème Année'),
    ('5ème Année', '5ème Année'),

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


class etudiantsFilter(django_filters.FilterSet):
    nomEtud = django_filters.CharFilter(label='Nom', widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))
    prenomEtud =  django_filters.CharFilter(label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    class Meta:
        model = etudiants
        fields = ['nomEtud', 'prenomEtud']


class relationFilter(django_filters.FilterSet):
    classe = django_filters.ChoiceFilter(label='Veuillez sélectionner la classe pour faire la simulation', widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 ',
        'style': 'width:50%;',

    }), choices=ANNEE)
