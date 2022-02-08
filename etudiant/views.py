from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import *
from structure.models import *
from .form import *
from .filters import *
import pandas as pd
 

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
#---------------------------Fin des importations--------------------------------------

def home(request):
   if request.user.is_authenticated:

      Etudiants = etudiants.objects.get(utilisateur__id=request.user.id)

      if request.user.groups.filter(name='Etudiants').exists():
         return redirect('accueil_student', Etudiants.id)
      else:
         return redirect('login', )
   else:
   #on récupère les valeurs entrées par lutilisateur et on le recherche dans la base de données
      if request.method=='POST':
         username=request.POST.get('username')
         password=request.POST.get('password')

         user=authenticate(request,username=username,password=password)
         Etudiants = etudiants.objects.get(utilisateur__id=user.id)

         #si on le trouve , on le redirige vers la page d'accueil de l'étudiant, sinon on le redirige vers la page de démarrage
         if user is not None:
            login(request,user)
            if user.groups.filter(name='Etudiants').exists():
               return redirect('accueil_student', Etudiants.id)
            else:
               return redirect('login', )

   return render(request, 'etudiant/index.html')

@login_required(login_url='login')
def deconnexion(request):
   logout(request)
   return redirect('login')

def inscription1(request):
   form =RegisterForm()
   if request.user.is_authenticated:
      Etudiants = etudiants.objects.get(utilisateur__id = request.user.id)
      return redirect('accueil_student',Etudiants.id)

   if request.method == 'POST':
      form = RegisterForm(request.POST)
      if form.is_valid():
         user=form.save()
         group = Group.objects.get(name='Etudiants')
         user.groups.add(group)
         print(user.groups)
         user.save()
         print("Formulaire enregistré!")
         return redirect("inscription1")
      else:
         print("Formulaire pas enregistrer!")
         form = RegisterForm()

   context = {'form':form,}
   return render(request, 'etudiant/suscribe.html', context)

def inscription2(request):
   form1 =RegisterEtudiantForm()
   print(request.user)
   if request.method=='POST':
      form1 = RegisterEtudiantForm(request.POST,request.FILES)

      if form1.is_valid():
         user1=form1.save()
         user1.utilisateur.add(request.user)
         user1.save()
         return redirect('inscription2')
      else:
         form1 = RegisterEtudiantForm()

   context = {'form1':form1,}
   return render(request, 'etudiant/suscribe1.html', context)

def inscription3(request):
   Etudiant = etudiants.objects.get(utilisateur=request.user)
   form2 = RelationForm()
   if request.method=='POST':
      form2 = RelationForm(request.POST)

      if form2.is_valid():
         user2=form2.save()
         user2.etudiant.add(Etudiant)
         user2.save()
         return redirect('accueil_student',pk_etud=Etudiant.id)

      else:
         form2 = RelationForm()

   context = {'form2':form2}
   return render(request, 'etudiant/suscribe2.html', context)




#---------------------------Accueil---------------------------
@login_required(login_url='login')#redirige l'utilisateur vers la page de connexion si il est pas connecté et tente d'accéder à la page d'accueil
def accueil(request,pk_etud):
   #on récupère l'id entré dans l'url pour recherché la table de l'étudiant
   Etudiants = etudiants.objects.get(id=pk_etud)
   relations = relation.objects.filter(etudiant__id = Etudiants.id).order_by('-id')
   uee=ue.objects.all()
   if uee:
      ues_parc = uee.filter(parcours__id = relations.parcours.id)
      ues=ues_parc.filter(annee_scolaire=relations.annee_scolaire)
      ecs= ec.objects.all()

      for ec in ecs:
         if ec.ue.id == ues.id:
            note, create = notes.objects.get_or_create(etudiant=Etudiants,ec=ec)

   context = {'Etudiants': Etudiants, }
   return render(request, 'etudiant/accueil.html', context)



#---------------------------Profil---------------------------
@login_required(login_url='login')
def profil(request, pk_etud):
   # on récupère l'id entré dans l'url pour recherché la table de l'étudiant
   Etudiants = etudiants.objects.get(id=pk_etud)
   context = {'Etudiants': Etudiants, }
   return render(request, 'etudiant/profil.html', context)





#---------------------------Update---------------------------
@login_required(login_url='login')
def update_profil(request, pk_etud):
   # on récupère l'id entré dans l'url pour recherché la table de l'étudiant
   Etudiants = etudiants.objects.get(id=pk_etud)
   form1 = Etudiants_profil1(instance=Etudiants)
   message = ''
   mess_color=False
   if request.method == 'POST':
      form1 = Etudiants_profil1(request.POST, request.FILES, instance=Etudiants)

      if form1.is_valid():
         form1.save()
         mess_color=True
         message = 'Modification effectué avec succès! ' \
                   'Nouvelles Informations enregistrées!'
      else:
          mess_color = False
          message = 'Erreur dans la saisie des informations!' \
                    'Veuillez entrer des informations valides!'

   context = {'Etudiants': Etudiants, 'form1': form1, 'message': message, 'mess_color':mess_color}
   return render(request, 'etudiant/update_profil.html', context)




#---------------------------Update---------------------------
@login_required(login_url='login')
def update_profil1(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   user = User.objects.get(id=Etudiants.utilisateur.id)
   form = formEmail(instance=user)
   message = ''
   mess_color = False
   if request.method == 'POST':
      form = formEmail(request.POST, request.FILES, instance=user)

      if form.is_valid():
         form.save()
         mess_color = True
         message = 'Modification effectué avec succès! ' \
                   'Nouvelles Informations enregistrées!'
      else:
          mess_color = False
          message = 'Erreur dans la saisie des informations!' \
                    'Veuillez entrer des informations valides!'

   context = {'Etudiants': Etudiants, 'form1': form, 'message': message,'mess_color':mess_color}
   return render(request, 'etudiant/update_profil2.html', context)




#----------------------------Etude-------------------------------------
@login_required(login_url='login')
def etudes_student(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   relations = relation.objects.all()
   etud_relations = relations.filter(etudiant__id=pk_etud)

   context = {'Etudiants': Etudiants, 'etud_relations':etud_relations}
   return render(request, 'etudiant/etudes.html', context)




#-------------------------------Note------------------------------------
@login_required(login_url='login')
def notes_student(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   relations = relation.objects.all()
   etud_relations = relations.filter(etudiant__id=pk_etud)

   semestre = niveaux.objects.all()
   sem1 = semestre.get(nom='Semestre 1')
   sem2 = semestre.get(nom='Semestre 2')
   Notes = notes.objects.all()

   Moyennes = moyenne.objects.all()

   moyenne1 = Moyennes.get(semestre__id=sem1.id)
   moyenne2 = Moyennes.get(semestre__id=sem2.id)

   ecs1 = ec.objects.filter(classe="1ère Année")

   rel1="Semestre 1"
   rel2 = "Semestre 2"
   myfiltre = relationFilter(request.GET, queryset=semestre)
   rel = myfiltre.qs
   if request.GET:
      rel1 = rel[0]
      rel2 = rel[1]
      ecs1 = ec.objects.filter(classe=request.GET['classe'])
      moyenne1,created = moyenne.objects.get_or_create(etudiant= Etudiants,semestre=rel1)
      moyenne2, created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=rel2)

   moyenneGeneral1=float((moyenne1.moyenne+moyenne2.moyenne)/2)


   context = {'Etudiants': Etudiants,'etud_relations':etud_relations,'ecs':ecs1,'sem1':sem1
              ,'sem2':sem2,'moyenneGeneral1':moyenneGeneral1,'moyenne1':moyenne1,'moyenne2':moyenne2,
              'Notes':Notes,'myfiltre':myfiltre,'rel1':rel1,'rel2':rel2}
   return render(request, 'etudiant/notes.html', context)


#--------------------------Change_classe-----------------------------
@login_required(login_url='login')
def change_classe(request,pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   relations = relation.objects.all()
   #on filtre toutes les relations de l'étudiant avec l'établissement par ordre décroissant
   etud_relations = relations.filter(etudiant__id=pk_etud).order_by('-id')
   #on récupère l'année scolaire pour l'élément 0 de la table et qui correspond à la dernière relation de l'étudiant et de l'établissement
   an=str(etud_relations[0].annee_scolaire)
   #on le sépare grâce au séparateur "-" et ensuite on rajoute 1 de chaque côté pour avoir l'année scolaire suivante
   ann=an.split("-")
   an1=int(ann[0])+1
   an2=int(ann[1])+1
   nextAnnee = [str(an1),str(an2)]
   nextAnnee = "-".join(nextAnnee)

   nomParcoursActuel = ''
   nomParcoursPossible = []
   anneeSuivant=''
   message = ''
   anneeScolaire=AnneeForm()
   mess_color = True

   #on teste le nom du parcours actuel de l'étudiant
   if etud_relations[0].parcours.nom == 'TCI':
      anneeSuivant='2ème année'
      nomParcoursActuel='Tronc Commun Industriel (TCI)'
      nomParcoursPossible=['Génie Civil','Génie Mécanique','Génie Electrique']
   elif etud_relations[0].parcours.nom == 'Génie Civil':
      anneeSuivant = '3ème année'
      nomParcoursActuel = 'Génie Civil (GC)'
      nomParcoursPossible = ['Génie Civil',]
   elif etud_relations[0].parcours.nom == 'Génie Mécanique':
      anneeSuivant = '3ème année'
      nomParcoursActuel = 'Génie Mécanique (GM)'
      nomParcoursPossible = ['Génie Mécanique','Hydraulique et Energiétique']
   elif etud_relations[0].parcours.nom == 'Génie Electrique':
      anneeSuivant = '3ème année'
      nomParcoursActuel = 'Génie Electrique (GE)'
      nomParcoursPossible = ['Génie Electrique', "Science et Technologie de l'Information et de la Communication"]
   else:
      anneeSuivant = '4ème année'
      nomParcoursActuel = ''
      nomParcoursPossible = []

   #on récupère les valeurs saisies par l'étudiant
   if request.GET:
      annee=request.GET['annee']
      parcourss=request.GET['parcours']
      #on teste si la valeur pour l'année scolaire suivant choisi par l'étudiant est différent que celle de la variable nextAnnee
      if annee != nextAnnee:
         mess_color = False
         #on affiche un message d'erreur dans ce cas
         message = "Erreur! Vous devez choisir l'année scolaire suivante qui est {0}".format(nextAnnee)

      # on recherche le parcours dans la base de données avec le nom du parcours choisi par l'étudiant
      parc = parcours.objects.get(nom=parcourss)
      # on tire l'id de la mention du parcours choisi
      ment = parc.mention.id
      # on recherche l'id de la mention dans la base
      mm = mention.objects.get(id=ment)
      # on tire l'id de l'établissement
      etab = mm.etablissement.id
      #on crée une nouvelle relation de l'étudiant avec les informations ci-dessus
      rel = relation.objects.create(etudiant__id=Etudiants.id,etablissements__id=etab,
                                    mentions__id=ment,parcours__id=parc.id,annee_scolaire=annee,
                                    classe=anneeSuivant)
      message = "Modifications enregistrées avec succés!"



   context = {'Etudiants': Etudiants, 'nomParcoursActuel':nomParcoursActuel,'nomParcoursPossible':nomParcoursPossible,
              'anneeSuivant':anneeSuivant,'anneeScolaire':anneeScolaire,'message':message,'rel':rel,'mess_color':mess_color}
   return render(request, 'etudiant/change_classe.html', context)

#-----------------------------Questionnaire-----------------------------------
@login_required(login_url='login')
def questionnaires_student(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   Semestre =''
   Mention = ''
   if request.POST:
      Semestre=request.POST['semestre']
      Mention=request.POST['mention']

   context = {'Etudiants': Etudiants,'Semestre':Semestre,'Mention':Mention }
   return render(request, 'etudiant/questionnaires.html', context)

def score(request,pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   Score =0

   if request.POST:
      radio = int(request.POST['radio'])
      radio1 = int(request.POST['radio1'])
      radio2 = int(request.POST['radio2'])
      radio3 = int(request.POST['radio3'])
      radio4 = int(request.POST['radio4'])
      radio5 = int(request.POST['radio5'])
      radio6 = int(request.POST['radio6'])
      radio7 = int(request.POST['radio7'])
      radio8 = int(request.POST['radio8'])
      radio9 = int(request.POST['radio9'])
      radio10 = int(request.POST['radio10'])
      radio11 = int(request.POST['radio11'])
      radio12 = int(request.POST['radio12'])
      radio13 = int(request.POST['radio13'])
      radio14 = int(request.POST['radio14'])
      Semestre = request.POST['checkbox']

      Score = radio + radio1 + radio2 + radio3 + radio4 + radio5 + radio6 + radio7 + radio8 + radio9 + radio10 + radio11 + radio12 + radio13 + radio14

   else:
      score=0

   context = {'Etudiants': Etudiants,'Score':Score,'Semestre':Semestre }
   return render(request, 'etudiant/score.html', context)



#----------------------------Simulation---------------------------
@login_required(login_url='login')
def simulation(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   relations = relation.objects.all()
   semestre=niveaux.objects.all()
   sem1=semestre.get(id=1)

   etud_relations = relations.filter(etudiant__id=pk_etud)
   ecs1 = ec.objects.filter(classe="1ère Année")

   rel1 = "Semestre 1"
   rel2 = "Semestre 2"
   myfiltre = relationFilter(request.GET, queryset=semestre)
   rel = myfiltre.qs
   if request.GET:
      rel1 = rel[0]
      rel2 = rel[1]
      ecs1 = ec.objects.filter(classe=request.GET['classe'])
   total_ec = ecs1.count()

   #Simulation
   dataset = pd.read_excel(
      "C:\\Users\\Joel Alphonsin\\PycharmProjects\\djangoProject\\projet\\static\\test-excel97-2003.xls")
   dataset.Filieres_Choisies = dataset.Filieres_Choisies.map({'GC': 0, 'GM': 1, 'GE': 2})
   X = dataset.drop(['Filieres_Choisies'], axis=1)
   x= len(X.columns)-1
   y = dataset.Filieres_Choisies
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
   model = RandomForestClassifier(criterion='gini', random_state=0)
   model.fit(X_train, y_train)
   message = {}
   #on récupère les entrées
   if request.POST:
      note1 = float(request.POST['note1'])
      note2 = float(request.POST['note2'])
      note3 = float(request.POST['note3'])
      note4 = float(request.POST['note4'])
      note5 = float(request.POST['note5'])
      note6 = float(request.POST['note6'])
      note7 = float(request.POST['note7'])
      note8 = float(request.POST['note8'])
      note9 = float(request.POST['note9'])
      note10 = float(request.POST['note10'])
      note11 = float(request.POST['note11'])
      note12 = float(request.POST['note12'])
      note13 = float(request.POST['note13'])
      note14 = float(request.POST['note14'])
      note15 = float(request.POST['note15'])
      score = float(request.POST['score'])

      #on prédit les pourcentages pour chaque parcours avec les valeurs d'entrées
      tab = np.array([[note1, note2, note3, note4, note5, note6, note7, note8, note9, note10, note11, note12, note13
                            , note14, note15, score]])
      pred = model.predict_proba(tab)
      message = {
            'GC': (pred[0][0]) * 100,
            'GM': (pred[0][1]) * 100,
            'GE': (pred[0][2]) * 100,
      }

   context = {'Etudiants': Etudiants, 'message': message, 'etud_relations':etud_relations,'ecs':ecs1,'sem1':sem1
              ,'myfiltre':myfiltre,'rel1':rel1,'rel2':rel2,'x':x,'total_ec':total_ec}
   return render(request, 'etudiant/simulation.html', context)



@login_required(login_url='login')
def orientation_student(request, pk_etud):
   Etudiants = etudiants.objects.get(id=pk_etud)
   tab1 = []
   SemestreQuestionnaire=request.POST['checkbox']
   semestre = niveaux.objects.all()
   Notes = notes.objects.all()
   note = Notes.filter(etudiants__id=pk_etud)
   if SemestreQuestionnaire == 'Semestre 2-Semestre 3':
      sem1 = semestre.get(nom='Semestre 1')
      sem2 = semestre.get(nom='Semestre 2')
      ecs1 = ec.objects.filter(classe="1ère Année")
      ec1 = ecs1.filter(niveaux__id=sem1.id)
      total_ec = ecs1.count()
      for ecs in ec1:
         for n in note:
            if n.ec.nom == ecs.nom:
               tab1.append(n.notesTotal)
      ec2 = ecs1.filter(niveaux__id=sem2.id)
      for ecs in ec2:
         for n in note:
            if n.ec.nom == ecs.nom:
               tab1.append(n.notesTotal)

      tab1.append(int(request.POST['Score']))
      # Simulation
      dataset = pd.read_excel(
         "C:\\Users\\Joel Alphonsin\\PycharmProjects\\djangoProject\\projet\\static\\test-excel97-2003.xls")
      dataset.Filieres_Choisies = dataset.Filieres_Choisies.map({'GC': 0, 'GM': 1, 'GE': 2})
      X = dataset.drop(['Filieres_Choisies'], axis=1)
      x = len(X.columns) - 1
      y = dataset.Filieres_Choisies
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
      model = RandomForestClassifier(criterion='gini', random_state=0)
      model.fit(X_train, y_train)

      m = {
         'GC':'Génie Civil',
         'GM':'Génie Mécanique',
         'GE':'Génie Electrique',
         'STIC': "Sciences et Technologies de l'Information de la Communication ",
         'HE':'Hydraulique et Energie'
      }

      tab = np.array([tab1])
      pred = model.predict_proba(tab)

      message = {
         'GC': (pred[0][0]) * 100,
         'GM': (pred[0][1]) * 100,
         'GE': (pred[0][2]) * 100,
      }
      pourcentage1 = round((pred[0][0]) * 100,2)
      pourcentage2 = round((pred[0][1]) * 100,2)
      pourcentage3 = round((pred[0][2]) * 100,2)
      orient,create=orientation.objects.get_or_create(etudiant=Etudiants,semestre=sem2,parcOptimal1='GC',
                                                      parcOptimal2='GM',parcOptimal3='GE',)
      orient.pourcentage1 = pourcentage1
      orient.pourcentage2 = pourcentage2
      orient.pourcentage3 = pourcentage3
      orient.save()

   context = {'Etudiants': Etudiants,'orient':orient,'m':m,'sem2':sem2 }
   return render(request, 'etudiant/orientation.html', context)


