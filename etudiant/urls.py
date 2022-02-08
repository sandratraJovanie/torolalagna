from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='login'),
    path('deconnexion/', views.deconnexion, name='logout'),
    path('inscription/', views.inscription1, name='inscription'),
    path('inscription1/', views.inscription2, name='inscription1'),
    path('inscription2/', views.inscription3, name='inscription2'),
    path('accueil/<str:pk_etud>', views.accueil, name='accueil_student'),
    path('profil/<str:pk_etud>', views.profil,name='profil_student'),
    path('modification_profil/<str:pk_etud>', views.update_profil, name='update_profil_student'),
    path('modification_profil2/<str:pk_etud>', views.update_profil1, name='update_profil_student2'),
    path('etudes/<str:pk_etud>', views.etudes_student,name='etudes_student'),
    path('notes/<str:pk_etud>', views.notes_student,name='notes_student'),
    path('change_classe/<str:pk_etud>', views.change_classe, name='change_classe'),
    path('questions/<str:pk_etud>', views.questionnaires_student,name='questions_student'),
    path('questions/score/<str:pk_etud>', views.score, name='score'),
    path('simulation/<str:pk_etud>', views.simulation,name='simulation'),
    path('orientation/<str:pk_etud>', views.orientation_student,name='orientation_student'),
]
