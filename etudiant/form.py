from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.models import User, Group

from .models import *
from structure.models import *
from django import forms

SEXE_MODELE = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),

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
class Etudiants_profil1(ModelForm):
    nomEtud = forms.CharField(label='Nom',widget=forms.TextInput(attrs={
        'class':'form-control',
    }))
    prenomEtud = forms.CharField(label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    sexEtud = forms.ChoiceField(label='Sexe', widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SEXE_MODELE)
    adresse = forms.CharField(label='Adresse', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    dateNaissance = forms.DateField(label='Date de naissance',widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker',
                                    'type':'date'
                                }))

    lieuNaissance = forms.CharField(label='Lieu de naissance', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    pere = forms.CharField(label='Nom du père', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    mere = forms.CharField(label='Nom de la mère', widget=forms.TextInput(attrs={
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
    dateCin = forms.DateField(label='Date de délivrance du CIN',widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker',
                                    'type':'date'
                                }))
    lieuCin = forms.CharField(label='Lieu de délivrance du CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    numTel = forms.CharField(label='Numéro de téléphone', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    pictureEtud = forms.ImageField(label='Image de profil',)
    class Meta:
        model = etudiants
        fields = '__all__'
        exclude = ['serieBacc','DateBacc','LyceeOrigine','utilisateur']

class formEmail(UserChangeForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    email = forms.EmailField(label="Adresse e-mail", widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username','email']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email','password1','password2']


class RelationForm(ModelForm):
    class Meta:
        model = relation
        fields='__all__'
        exclude = ['etudiant']

class RegisterEtudiantForm(ModelForm):
    nomEtud = forms.CharField(label='Nom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    prenomEtud = forms.CharField(label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    sexEtud = forms.ChoiceField(label='Sexe', widget=forms.Select(attrs={
        'class': 'form-control',
    }), choices=SEXE_MODELE)
    adresse = forms.CharField(label='Adresse', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    dateNaissance = forms.DateField(label='Date de naissance', widget=forms.TextInput(attrs=
    {
        'class': 'datepicker',
        'type': 'date'
    }))

    lieuNaissance = forms.CharField(label='Lieu de naissance', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    pere = forms.CharField(label='Nom du père', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    mere = forms.CharField(label='Nom de la mère', widget=forms.TextInput(attrs={
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
    dateCin = forms.DateField(label='Date de délivrance du CIN', widget=forms.TextInput(attrs=
    {
        'class': 'datepicker',
        'type': 'date'
    }))
    lieuCin = forms.CharField(label='Lieu de délivrance du CIN', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    serieBacc = forms.CharField(label="Série du Bacc", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    DateBacc = forms.DateField(label="Date d'obtention du Bacc", widget=forms.TextInput(attrs=
    {
        'class': 'datepicker',
        'type': 'date'
    }))
    LyceeOrigine = forms.CharField(label="Lycée d'origine", widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    numTel = forms.CharField(label='Numéro de téléphone', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    pictureEtud = forms.ImageField(label='Image de profil', )
    class Meta:
        model = etudiants
        fields = '__all__'
        exclude = ['utilisateur']

class AnneeForm(forms.Form):
    annee = forms.ChoiceField(label='Année scolaire', widget=forms.Select(attrs={
        'class': 'form-control  mx-auto',
        'style': 'width:30%;'
    }), choices=ANNEE_MODELE)


