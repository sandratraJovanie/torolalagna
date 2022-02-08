from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django  import forms
from .models import enseignants
from etudiant.models import *
from structure.models import *
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

SEXE_MODELE = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),

]
class Enseignants_profil1(ModelForm):
    nom = forms.CharField(label='Nom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    prenom = forms.CharField(label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    sexe = forms.ChoiceField(label='Sexe', widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SEXE_MODELE)
    adresse = forms.CharField(label='Adresse', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    paysOrigine = forms.CharField(label="Pays d'origine", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    nationalite = forms.CharField(label='Nationalité', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    cin = forms.CharField(label='CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    datecin = forms.DateField(label='Date de délivrance du CIN',widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker',
                                    'type':'date'
                                }))
    lieucin = forms.CharField(label='Lieu de délivrance du CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    numTel = forms.CharField(label='Numéro de téléphone', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    picture = forms.ImageField(label='Image de profil', )
    class Meta:
        model = enseignants
        fields = '__all__'
        exclude = ['utilisateur']


class RelationForm(ModelForm):
    annee_scolaire = forms.ChoiceField(label="Année scolaire de l'étudiant", widget=forms.Select(attrs={
        'class': 'form-select p-2 mb-3',
    }), choices=ANNEE_MODELE)
    classe = forms.ChoiceField(label="Classe de l'étudiant", widget=forms.Select(attrs={
        'class': 'form-select p-2 mb-3',
    }), choices=ANNEE)

    class Meta:
        model = relation
        fields = '__all__'
        exclude = ['etudiant', 'etablissements', 'parcours', 'mentions']

class RegisterFormEns(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email','password1','password2']


class RegisterEnseignant(ModelForm):
    nom = forms.CharField(label='Nom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    prenom = forms.CharField(label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    sexe = forms.ChoiceField(label='Sexe', widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SEXE_MODELE)
    adresse = forms.CharField(label='Adresse', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    paysOrigine = forms.CharField(label="Pays d'origine", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    nationalite = forms.CharField(label='Nationalité', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    cin = forms.CharField(label='CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    datecin = forms.DateField(label='Date de délivrance du CIN', widget=forms.TextInput(attrs=
    {
        'class': 'datepicker',
        'type': 'date'
    }))
    lieucin = forms.CharField(label='Lieu de délivrance du CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    numTel = forms.CharField(label='Numéro de téléphone', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    picture = forms.ImageField(label='Image de profil', )

    class Meta:
        model = enseignants
        fields = '__all__'
        exclude = ['utilisateur']


class ECForm(ModelForm):
    annee_scolaire = forms.ChoiceField(label="Choisissez l'année universitaire", widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3',
    }), choices=ANNEE_MODELE)
    classe = forms.ChoiceField(label='Choisissez la classe', widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }), choices=ANNEE)
    ue = forms.ModelChoiceField(label="Choisissez l'UE", queryset=ue.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }))
    niveaux = forms.ModelChoiceField(label="Choisissez le semestre de l'EC", queryset=niveaux.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }))
    nom = forms.CharField(label="Entrez le nom de l'EC", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    coefficient = forms.IntegerField(label="Entrez le coefficient de l'EC", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = ec
        fields ='__all__'
        exclude = ['isValid']

class ECForm1(ModelForm):
    annee_scolaire = forms.ChoiceField(label="Choisissez l'année universitaire", widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3',
    }), choices=ANNEE_MODELE)
    classe = forms.ChoiceField(label='Choisissez la classe', widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }), choices=ANNEE)
    niveaux = forms.ModelChoiceField(label="Choisissez le semestre de l'EC", queryset=niveaux.objects.all(),widget=forms.Select(attrs={
       'class': 'form-control mx-auto mb-3 p-2',
     }))
    ue = forms.ModelChoiceField(label="Choisissez l'UE", queryset=ue.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }))
    nom = forms.CharField(label="Entrez le nom de l'EC", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    coefficient = forms.IntegerField(label="Entrez le coefficient de l'EC", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = ec
        fields ='__all__'
        exclude = ['isValid',]


class UEForm1(ModelForm):
    annee_scolaire = forms.ChoiceField(label="Choisissez l'année universitaire", widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3',
    }), choices=ANNEE_MODELE)
    classe = forms.ChoiceField(label='Choisissez la classe', widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }), choices=ANNEE)
    niveaux = forms.ModelChoiceField(label="Choisissez le semestre de l'UE", queryset=niveaux.objects.all(),widget=forms.Select(attrs={
       'class': 'form-control mx-auto mb-3 p-2',
     }))
    parcours = forms.ModelChoiceField(label="Entrez le parcours de l'UE",queryset=parcours.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control mx-auto mb-3 p-2',
    }))
    nom = forms.CharField(label="Entrez le nom de l'UE", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    credit = forms.IntegerField(label="Entrez le credit de l'UE", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = ue
        fields ='__all__'
        exclude = ['isValid',]


