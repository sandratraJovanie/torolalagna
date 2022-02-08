from django.contrib.auth.models import User,Group
from django.db import models
from etudiant.models import etudiants
from structure.models import parcours

SEXE_MODELE = [
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),
]

class enseignants(models.Model):
    utilisateur = models.OneToOneField(User,on_delete=models.CASCADE)
    nom=models.CharField("Nom",max_length=100)
    prenom=models.CharField("Prénom",max_length=200)
    sexe=models.CharField("Genre",max_length=20,  blank=False,choices=SEXE_MODELE)
    nationalite=models.CharField("Nationalité",max_length=50)
    paysOrigine=models.CharField("Pays d'origine",max_length=50)
    cin=models.CharField("Numéro du CIN",max_length=15,unique=True)
    datecin=models.DateField("Date de délivrance du CIN")
    lieucin=models.CharField("Lieu de délivrance du CIN",max_length=50)
    numTel=models.CharField("Numéro de téléphone",max_length=10,unique=True)
    adresse=models.CharField("Adresse",max_length=120)

    picture = models.ImageField("Image de profil",upload_to='media/image_profils/enseignants',null=True,default='media/image_profils/avatar.jpg ')


    class Meta:
        verbose_name='Enseignant'
        verbose_name_plural = 'Enseignants'

    def __str__(self):
        return "{} {}".format(self.nom, self.prenom)


class responsables(models.Model):
    enseignant = models.OneToOneField(enseignants,on_delete=models.CASCADE)
    parcours = models.OneToOneField(parcours,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Responsable'
        verbose_name_plural = 'Responsables'

    def __str__(self):
        return "{} - {} {}".format(self.parcours.nom,self.enseignant.nom, self.enseignant.prenom)


class suivis(models.Model):
    enseignant = models.ForeignKey(enseignants, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(etudiants, on_delete=models.CASCADE)
    date = models.DateTimeField("Date de suivi",auto_now_add=True)

    class Meta:
        verbose_name='Suivis'
        verbose_name_plural = 'Suivis'

    def __str__(self):
        return "{} {} - {} {}".format(self.enseignant.nom, self.enseignant.prenom,self.etudiant.nomEtud,self.etudiant.prenomEtud)
