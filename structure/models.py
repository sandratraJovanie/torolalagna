from django.db import models

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

class etablissements(models.Model):
    nom=models.CharField("Nom",max_length=100)
    adresse=models.CharField("Adresse",max_length=100)
    ville=models.CharField("Nom de la ville",max_length=50)

    class Meta:
        verbose_name='Etablissement'
        verbose_name_plural = 'Etablissements'

    def __str__(self):
        return "{} - {}".format(self.nom,self.ville)

class mentions(models.Model):
    nom=models.CharField("Nom",max_length=100)
    etablissement = models.ForeignKey(etablissements,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Mention'
        verbose_name_plural = 'Mentions'

    def __str__(self):
        return "{} - {}".format(self.etablissement.nom,self.nom)


class parcours(models.Model):
    nom = models.CharField("Nom",max_length=100)
    mention = models.ForeignKey(mentions, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Parcours'
        verbose_name_plural = 'Parcours'

    def __str__(self):
        return "{} - {}".format(self.mention.nom,self.nom)

class niveaux(models.Model):
    nom = models.CharField("Nom",max_length=100)
    classe = models.CharField("Classe",max_length=20, choices=ANNEE)
    class Meta:
        verbose_name='Niveau'
        verbose_name_plural = 'Niveaux'

    def __str__(self):
        return "{} - {}".format(self.classe,self.nom)


class ue(models.Model):
    nom = models.CharField("Nom", max_length=100)
    annee_scolaire = models.CharField("Année scolaire",max_length=20, choices=ANNEE_MODELE)
    classe = models.CharField("Classe",max_length=20, choices=ANNEE)
    niveaux = models.ForeignKey(niveaux, on_delete=models.CASCADE)
    parcours = models.ForeignKey(parcours, on_delete=models.CASCADE)
    credit= models.IntegerField("Crédit")
    isValid= models.BooleanField("Validé",default=False)


    class Meta:
        verbose_name='UE'
        verbose_name_plural = 'UE'

    def __str__(self):
        return "{} - {}".format(self.parcours.nom,self.nom)



class ec(models.Model):
    nom = models.CharField("Nom",max_length=100)
    annee_scolaire = models.CharField("Année scolaire",max_length=20, choices=ANNEE_MODELE)
    classe = models.CharField("Classe",max_length=20, choices=ANNEE)
    niveaux = models.ForeignKey(niveaux,on_delete=models.CASCADE)
    ue = models.ForeignKey(ue, on_delete=models.CASCADE)
    coefficient = models.IntegerField("Coefficient")
    isValid = models.BooleanField("Validé",default=False)

    class Meta:
        verbose_name='EC'
        verbose_name_plural = 'EC'

    def __str__(self):
        return "{} - {}".format(self.ue.nom,self.nom)
