from django.db import models
from django.contrib.auth.models import User

from structure.models import *

SEXE_MODELE = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),

]
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
class etudiants(models.Model):
    utilisateur = models.OneToOneField(User,on_delete=models.CASCADE)
    nomEtud = models.CharField("Nom",max_length=100)
    prenomEtud= models.CharField("Prénom(s)",max_length=200)
    dateNaissance= models.DateField("Date de naissance")
    lieuNaissance= models.CharField("Lieu de naissance",max_length=100)
    sexEtud=models.CharField("Genre",max_length=20,  blank=False,choices=SEXE_MODELE)
    nationalite= models.CharField("Nationalité",max_length=100)
    paysOrigine= models.CharField("Pays d'origine",max_length=100)
    cin= models.CharField("Numéro du CIN",max_length=15,unique=True)
    dateCin= models.DateField("Date de délivrance du CIN")
    lieuCin= models.CharField("Lieu de délivrance du CIN",max_length=100)
    adresse= models.CharField("Adresse",max_length=100)
    numTel=models.CharField("Numéro du téléphone",max_length=10,unique=True)

    mere= models.CharField("Nom et prénom(s) de la mère",max_length=100)
    pere= models.CharField("Nom et prénom(s) du père",null=True,max_length=100)
    serieBacc = models.CharField("Série du BACC",max_length=50)
    DateBacc = models.DateField("Date d'obtention du BACC",)
    LyceeOrigine = models.CharField("Lycée d'origine",max_length=100)


    pictureEtud = models.ImageField("Image de profil",upload_to='media/image_profils/etudiants',
                                    null=True,default='static/image/avatar.jpg ')

    class Meta:
        verbose_name='Etudiant'
        verbose_name_plural = 'Etudiants'

    def __str__(self):
        return "{} {}".format(self.nomEtud,self.prenomEtud)


class orientation(models.Model):
    parcOptimal1= models.CharField("Choix n° 1",max_length=100,default='none')
    pourcentage1=models.FloatField("Pourcentage du choix n° 1",default=0.0)
    parcOptimal2 = models.CharField("Choix n° 2",max_length=100,default='none')
    pourcentage2 = models.FloatField("Pourcentage du choix n° 2",default=0.0)
    parcOptimal3 = models.CharField("Choix n° 3",max_length=100,default='none')
    pourcentage3 = models.FloatField("Pourcentage du choix n° 3",default=0.0)

    semestre= models.OneToOneField(niveaux,on_delete=models.CASCADE,unique=True)

    etudiant = models.ForeignKey(etudiants, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Orientation'
        verbose_name_plural = 'Orientations'

    def __str__(self):
        return self.etudiants.nomEtud

class relation(models.Model):

    etudiant = models.ForeignKey(etudiants,on_delete=models.CASCADE)
    etablissements = models.ForeignKey(etablissements, on_delete=models.CASCADE)
    mentions = models.ForeignKey(mentions, on_delete=models.CASCADE)
    parcours = models.ForeignKey(parcours, on_delete=models.CASCADE)

    annee_scolaire = models.CharField("Année scolaire",max_length=20, choices=ANNEE_MODELE,)
    classe = models.CharField("Classe",max_length=20,choices=ANNEE)
    date = models.DateTimeField("Date d'inscription",auto_now_add=True)

    class Meta:
        verbose_name='Relation'
        verbose_name_plural = 'Relations'

    def __str__(self):
        return "{} - {} {}".format(self.etablissements.nom, self.etudiant.nomEtud,self.etudiant.prenomEtud)

class notes(models.Model):
    notesTP = models.FloatField("Note du TP",default=0.0)
    notesPartiel = models.FloatField("Note du partiel",default=0.0)
    notesTotal = models.FloatField("Note totale",default=0.0)
    ec= models.OneToOneField(ec, on_delete=models.CASCADE)
    etudiants=models.ForeignKey(etudiants,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Note'
        verbose_name_plural = 'Notes'

class moyenne(models.Model):
    etudiant =models.ForeignKey(etudiants,on_delete=models.CASCADE)
    moyenne=models.FloatField("Moyenne",default=0.0)
    semestre=models.ForeignKey(niveaux,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Moyenne'
        verbose_name_plural = 'Moyennes'

    def __str__(self):
        return " Moyenne de {} {} pour le {}".format(self.etudiant.nomEtud,self.etudiant.prenomEtud,self.semestre.nom)

