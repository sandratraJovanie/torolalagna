from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_teacher, name='home_enseignant'),
    path('deconnexion/', views.deconnexion, name='logout1'),
    path('inscription/', views.suscribe_teachers, name='suscribe_teachers'),
    path('inscription1/<str:pk_user>', views.suscribe1, name='suscribe_teachers1'),
    path('accueil/<str:pk_ens>', views.accueil_enseignant, name='accueil_enseignant'),
    path('profil/<str:pk_ens>', views.profil_enseignant, name='profil_enseignant'),
    path('modif_profil/<str:pk_ens>', views.update_profil_enseignants,
         name='update_profil_enseignants'),
    path('suivis/ajout/<str:pk_etud>', views.ajout_suivi, name='ajout_suivi'),
    path('suivis/supprime/<str:pk_etud>', views.supprime_suivi, name='supprime_suivi'),
    path('suivis/<str:pk_ens>', views.suivis_enseignant, name='suivis_enseignant'),
    path('suivis/profil_etudiant/<str:pk_etud>', views.profil_etudiant_suivi,
         name='profil_etudiant_suivi'),

    # Chemin pour les enseignant responsables
    path('responsable/accueil/<str:pk_resp>', views.accueil_resp, name='accueil_resp'),
    path('responsable/profil/<str:pk_resp>', views.profil_resp, name='profil_resp'),
    path('responsable/modif_profil_resp/<str:pk_resp>', views.update_profil_resp,
         name='update_profil'),
    path('responsable/suivis/ajout/<str:pk_etud>', views.ajout_suivi_resp, name='ajout_suivi_resp'),
    path('responsable/suivis/supprime/<str:pk_etud>', views.supprime_suivi_resp, name='supprime_suivi_resp'),
    path('responsable/suivis/<str:pk_resp>', views.suivis_resp, name='suivis_resp'),
    path('responsable/suivis/profil_etudiant/<str:pk_etud>', views.profil_etudiant_suivi_resp,
         name='etudiant_suivi'),
    path('responsable/notes/<str:pk_resp>', views.notes_resp, name='notes_resp'),
    path('responsable/notes/modif_note/<str:pk_etud>', views.affiche_notes, name='ajout_notes'),
    path('responsable/ue/<str:pk_resp>', views.Ue, name='ue'),
    path('responsable/ue/ajout_ue/<str:pk_resp>', views.ajout_ue, name='ajout_ue'),
    path('responsable/ue/modif_ue/<str:pk_resp>', views.modif_ue, name='modif_ue'),
    path('responsable/ec/<str:pk_resp>', views.Ec, name='ec'),
    path('responsable/ec/ajout_ec/<str:pk_resp>', views.ajout_ec, name='ajout_ec'),
    path('responsable/ec/modif_ec/<str:pk_resp>', views.modif_ec, name='modif_ec'),
]
