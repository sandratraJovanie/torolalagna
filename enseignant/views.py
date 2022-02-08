import ast
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import *
from etudiant.models import *
from structure.models import ec
from etudiant.filters import etudiantsFilter, relationFilter
from .filters import *
from .form import *
from .filters import *


def home_teacher(request):
    if request.user.is_authenticated:

       Enseignants = enseignants.objects.get(utilisateur__id=request.user.id)

       if request.user.groups.filter(name='Responsables').exists():
           return redirect('accueil_resp', Enseignants.id)
       elif request.user.groups.filter(name='Enseignants').exists():
           return redirect('accueil_enseignant', Enseignants.id)
       else:
           return redirect('home_enseignant', )
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            Enseignants = enseignants.objects.get(utilisateur__id=user.id)

            if user is not None:
                login(request, user)
                if user.groups.filter(name='Responsables').exists():
                    return redirect('accueil_resp', Enseignants.id)
                elif user.groups.filter(name='Enseignants').exists():
                    return redirect('accueil_enseignant', Enseignants.id)
                else:
                    return redirect('home_enseignant',)
            else:
                messages.info(request, 'Nom d\'utilisateur et mot de passe non valide! Veuillez réessayer ou contacter l\'administrateur.')
                print(messages)

    return render(request, 'enseignant/index.html')


def deconnexion(request):
    logout(request)
    return redirect('home_enseignant')


def suscribe_teachers(request):
    form = RegisterFormEns()

    if request.user.is_authenticated:
        Enseignants = enseignants.objects.get(utilisateur__id=request.user.id)
        return redirect('accueil_student', Enseignants.id)

    if request.method == 'POST':
        form = RegisterFormEns(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(id=1)
            user.groups.add(group)
            user.save()

            return redirect("suscribe_teachers1", user.id)
        else:

            form = RegisterFormEns()
    context = {'form': form, }
    return render(request, 'enseignant/suscribe_teacher.html', context)


def suscribe1(request, pk_user):
    form = RegisterEnseignant()
    user = User.objects.get(id=pk_user)
    if request.method == 'POST':
        form = RegisterEnseignant(request.POST, request.FILES)

        if form.is_valid():
            Enseignants = form.save()
            Enseignants.utilisateur = user
            Enseignants.save()
            return redirect('accueil_enseignant', Enseignants.id)
        else:
            form = RegisterEnseignant()
    context = {'form': form, }
    return render(request, 'enseignant/suscribe1.html', context)


@login_required(login_url='home_enseignant')
def accueil_enseignant(request, pk_ens):
    Enseignants = enseignants.objects.get(id=pk_ens)

    context = {'Enseignants': Enseignants, }
    return render(request, 'enseignant/accueil_teachers.html', context)


@login_required(login_url='home_enseignant')
def profil_enseignant(request, pk_ens):
    Enseignants = enseignants.objects.get(id=pk_ens)

    context = {'Enseignants': Enseignants, }
    return render(request, 'enseignant/profil_teachers.html', context)


@login_required(login_url='home_enseignant')
def update_profil_enseignants(request, pk_ens):
    Enseignants = enseignants.objects.get(id=pk_ens)
    form1 = Enseignants_profil1(instance=Enseignants)
    message = ''
    if request.method == 'POST':
        form1 = Enseignants_profil1(request.POST, request.FILES, instance=Enseignants)

        if form1.is_valid():
            form1.save()
            message = 'Modification effectué avec succès! ' \
                      'Nouvelles Informations enregistrées!'

    context = {'Enseignants': Enseignants, 'form1': form1, 'message': message}
    return render(request, 'enseignant/update_profil.html', context)

@login_required(login_url='home_enseignant')
def ajout_suivi(request,pk_etud):
    Enseignants = enseignants.objects.get(utilisateur__id = request.user.id)
    Etudiant = etudiants.objects.get(id = pk_etud)
    suivi= suivis.objects.create(enseignant = Enseignants, etudiant= Etudiant)
    if suivi:
        message = "Vous suivez maintenant l'étudiant {} {}".format(Etudiant.nomEtud,Etudiant.prenomEtud)

    context= {'Enseignants':Enseignants,'message':message}
    return render(request, 'enseignant/ajout_suivi.html',context)

@login_required(login_url='home_enseignant')
def supprime_suivi(request,pk_etud):
    Enseignants = enseignants.objects.get(utilisateur__id = request.user.id)
    Etudiant = etudiants.objects.get(id = pk_etud)
    suivi= suivis.objects.get(enseignant = Enseignants, etudiant= Etudiant)
    suivi.delete()

    message = "Vous ne suivez plus l'étudiant {} {}".format(Etudiant.nomEtud,Etudiant.prenomEtud)

    context= {'Enseignants':Enseignants,'message':message}
    return render(request, 'enseignant/supprime_suivi.html',context)

@login_required(login_url='home_enseignant')
def profil_etudiant_suivi(request, pk_etud):
    Enseignants = enseignants.objects.get(utilisateur__id=request.user.id)
    Etudiants = etudiants.objects.get(id=pk_etud)
    Suivis = suivis.objects.all()
    suivi = Suivis.filter(etudiant__id=pk_etud)
    relations = relation.objects.all()
    etud_relations = relations.filter(etudiant__id=pk_etud)

    if suivi:
        suit = True
        message = "Ne plus suivre cet étudiant"
    else:
        suit = False
        message = "Suivre cet étudiant"

    semestre = niveaux.objects.all()
    sem1 = semestre.get(nom='Semestre 1')
    sem2 = semestre.get(nom='Semestre 2')
    Notes = notes.objects.all()

    moyenne1, created = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem1)
    moyenne2 , created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem2)
    ecs = ec.objects.all()
    ecs1 = ecs.filter(classe="1ère Année")

    rel1 = "Semestre 1"
    rel2 = "Semestre 2"
    myfiltre = relationFilter(request.GET, queryset=semestre)
    rel = myfiltre.qs
    if request.GET:
        rel1 = rel[0]
        rel2 = rel[1]
        ecs1 = ecs.filter(classe=request.GET['classe'])
        moyenne1, created = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=rel1)
        moyenne2, created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=rel2)

    moyenneGeneral1 = float((moyenne1.moyenne + moyenne2.moyenne) / 2)

    orient = orientation.objects.filter(etudiant__id=Etudiants.id)

    m = {
        'GC': 'Génie Civil',
        'GM': 'Génie Mécanique',
        'GE': 'Génie Electrique',
        'STIC': "Sciences et Technologies de l'Information de la Communication ",
        'HE': 'Hydraulique et Energie',
        'BAT': 'Bâtiment',
        'TP': 'Travaux Public',
        'TR': 'Télécommunication et Réseau',
        'EII': 'Electronique Informatique Industriel',
        'MAE': 'Machine Electrique',
        'PTDE': 'Production,Transport et Distribution ELectrique',
        'ENR': 'Energie Nouvelle Renouvelable',
        'HIT': 'HIT',
        'MO': 'Mécanique Ouvrage',
        'MX': 'Mécatronique',
        'MI': 'Mécanique Industrielle',
    }
    context = {'Etudiants': Etudiants, 'suivi': suivi, 'message': message, 'etud_relations': etud_relations,
               'ecs': ecs1, 'sem1': sem1, 'sem2': sem2, 'moyenneGeneral1': moyenneGeneral1, 'moyenne1': moyenne1,
               'moyenne2': moyenne2,'suit':suit,'Enseignants':Enseignants,
               'Notes': Notes, 'myfiltre': myfiltre, 'rel1': rel1, 'rel2': rel2, 'orient': orient, 'm': m}
    return render(request, 'enseignant/profil_student.html', context)


@login_required(login_url='home_enseignant')
def suivis_enseignant(request, pk_ens):
    Enseignants = enseignants.objects.get(id=pk_ens)
    Suivis = suivis.objects.all()
    Etudiant = etudiants.objects.all()
    etudiants_suivis = Suivis.filter(enseignant__id=pk_ens)

    monFiltre = etudiantsFilter(request.GET, queryset=Etudiant)
    Etudiant = monFiltre.qs

    context = {'Enseignants': Enseignants, 'etudiants_suivis': etudiants_suivis, 'Etudiant': Etudiant,
               'monFiltre': monFiltre}
    return render(request, 'enseignant/suivis_teachers.html', context)


# Fin des views pour les enseignant


# Début des views pour les responsables
@login_required(login_url='home_enseignant')
def accueil_resp(request, pk_resp):
    Responsable = responsables.objects.get(id=pk_resp)

    context = {'Responsable': Responsable}
    return render(request, 'responsables/accueil_resp.html', context)


@login_required(login_url='home_enseignant')
def profil_resp(request, pk_resp):
    Responsable = responsables.objects.get(id=pk_resp)

    context = {'Responsable': Responsable, }
    return render(request, 'responsables/profil_resp.html', context)


@login_required(login_url='home_enseignant')
def update_profil_resp(request,pk_resp):
    Enseignants = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(id=pk_resp)

    form1 = Enseignants_profil1(instance=Enseignants)
    message = ''
    if request.method == 'POST':
        form1 = Enseignants_profil1(request.POST, request.FILES, instance=Enseignants)

        if form1.is_valid():
            form1.save()
            message = 'Modification effectué avec succès! ' \
                      'Nouvelles Informations enregistrées!'

    context = {'Responsable':Responsable,'Enseignants': Enseignants, 'form1': form1, 'message': message}
    return render(request, 'responsables/update_profil.html', context)


@login_required(login_url='home_enseignant')
def suivis_resp(request, pk_resp):
    Responsable = responsables.objects.get(id=pk_resp)
    Suivis = suivis.objects.all()
    etudiants_suivis = Suivis.filter(etudiant__id=pk_resp)
    Etudiants = etudiants.objects.all()

    filtre = etudiantsFilter(request.GET, queryset=Etudiants)
    Etudiants = filtre.qs

    context = {'Responsable': Responsable, 'etudiants_suivis': etudiants_suivis, 'filtre': filtre,
               'Etudiants': Etudiants}
    return render(request, 'responsables/suivis_resp.html', context)

def ajout_suivi_resp(request,pk_etud):
    Enseignants = enseignants.objects.get(utilisateur__id = request.user.id)
    Responsable = responsables.objects.get(id=Enseignants.id)
    Etudiant = etudiants.objects.get(id = pk_etud)
    suivi= suivis.objects.create(enseignant = Enseignants, etudiant= Etudiant)
    if suivi:
        message = "Vous suivez maintenant l'étudiant {} {}".format(Etudiant.nomEtud,Etudiant.prenomEtud)

    context= {'Responsable': Responsable,'Enseignants':Enseignants,'message':message}
    return render(request, 'enseignant/ajout_suivi.html',context)

@login_required(login_url='home_enseignant')
def supprime_suivi_resp(request,pk_etud):
    Enseignants = enseignants.objects.get(utilisateur__id = request.user.id)
    Responsable = responsables.objects.get(id=Enseignants.id)
    Etudiant = etudiants.objects.get(id = pk_etud)
    suivi= suivis.objects.get(enseignant = Enseignants, etudiant= Etudiant)
    suivi.delete()

    message = "Vous ne suivez plus l'étudiant {} {}".format(Etudiant.nomEtud,Etudiant.prenomEtud)

    context= {'Responsable': Responsable,'Enseignants':Enseignants,'message':message}
    return render(request, 'enseignant/supprime_suivi.html',context)

@login_required(login_url='home_enseignant')
def profil_etudiant_suivi_resp(request, pk_etud):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    Etudiants = etudiants.objects.get(id=pk_etud)

    Suivis = suivis.objects.all()
    suivi = Suivis.filter(etudiant__id=pk_etud)
    relations = relation.objects.all()
    Notes = notes.objects.all()
    Moyennes = moyenne.objects.all()
    Niveaux = niveaux.objects.all()
    sem1 = Niveaux.get(nom='Semestre 1')
    sem2 = Niveaux.get(nom='Semestre 2')
    ecs = ec.objects.all()
    ecs1 = ecs.filter(classe="1ère Année")
    moyenne1, created = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem1)
    moyenne2, created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem2)

    filtre = classeFilter1(request.GET, queryset=Niveaux)
    N = filtre.qs
    if request.GET:
        sem1 = N[0]
        sem2 = N[1]
        ecs1 = ecs.filter(classe=request.GET['classe'])
        moyenne1, created = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem1)
        moyenne2, created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=sem2)
    moyenneGeneral1 = float((moyenne1.moyenne + moyenne2.moyenne) / 2)

    orient = orientation.objects.filter(etudiant__id=Etudiants.id)

    m = {
        'GC': 'Génie Civil',
        'GM': 'Génie Mécanique',
        'GE': 'Génie Electrique',
        'STIC': "Sciences et Technologies de l'Information de la Communication ",
        'HE': 'Hydraulique et Energie',
        'BAT': 'Bâtiment',
        'TP': 'Travaux Public',
        'TR': 'Télécommunication et Réseau',
        'EII': 'Electronique Informatique Industriel',
        'MAE': 'Machine Electrique',
        'PTDE': 'Production,Transport et Distribution ELectrique',
        'ENR': 'Energie Nouvelle Renouvelable',
        'HIT': 'HIT',
        'MO': 'Mécanique Ouvrage',
        'MX': 'Mécatronique',
        'MI': 'Mécanique Industrielle',}

    etud_relations = relations.filter(etudiant__id=pk_etud)

    if suivi:
        message = "Ne plus suivre cet étudiant"
    else:
        message = "Suivre cet étudiant"

    context = {'Responsable': Responsable,'Etudiants': Etudiants, 'suivi': suivi, 'message': message,
               'etud_relations': etud_relations,'filtre':filtre,'sem1':sem1,'sem2':sem2,'orient': orient, 'm': m,
               'moyenneGeneral1': moyenneGeneral1, 'moyenne1': moyenne1,'moyenne2': moyenne2,'ecs': ecs1,'Notes': Notes
               }
    return render(request, 'responsables/profil_student.html', context)


@login_required(login_url='home_enseignant')
def Ue(request, pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    uee = ue.objects.all().order_by('niveaux')
    semestre = niveaux.objects.all()

    if Responsable.parcours.nom == 'TCI':
        sem1 = semestre.get(nom='Semestre 1')
        sem2 = semestre.get(nom='Semestre 2')

    else:
        print("Oups!!Il n'y a encore rien pour le moment")

    count1 = 0
    count2 = 0

    filtre = AnneeScolaireFilter(request.GET, queryset=uee)
    UE = filtre.qs
    for sem in UE:
        if sem.niveaux == sem1:
            count1 += 1
        else:
            count2 += 1
    print('count1 :', count1)
    print("count2 :", count2)
    context = {'Responsable': Responsable, 'filtre': filtre,
               'UE': UE, 'count1': count1, 'count2': count2, 'sem1': sem1, 'sem2': sem2}
    return render(request, 'responsables/ue.html', context)


@login_required(login_url='home_enseignant')
def ajout_ue(request,pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    Etudiants = relation.objects.filter(parcours__id=Responsable.parcours.id)
    erreur=''
    form = UEForm1()
    if request.method == 'POST':
        form = UEForm1(request.POST)

        if form.is_valid():
            NewUe = form.save()
            print(NewUe)
        else:
            erreur = form.errors.items()
            print(erreur)
            form= UEForm1()


    context = {'Responsable': Responsable, 'form':form, 'erreur':erreur}
    return render(request, 'responsables/ajout_ue.html',context)

@login_required(login_url='home_enseignant')
def modif_ue(request,pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    UE = ue.objects.get(id=pk_resp)
    form = UEForm1(instance=UE)
    if request.method == 'POST':
        form = UEForm1(request.POST,instance=UE)
        if form.is_valid():
            form.save()
            return redirect('ec',Responsable.id)
        else :
            messages.error(request, "Error")
            form= UEForm1(instance=UE)
    context = {'Responsable': Responsable, 'form':form}
    return render(request, 'responsables/modif_ue.html',context)



@login_required(login_url='home_enseignant')
def Ec(request, pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    ecc = ec.objects.all().order_by('niveaux')
    semestre = niveaux.objects.all()
    Etudiants = relation.objects.filter(parcours__id=Responsable.parcours.id)


    if Responsable.parcours.nom == 'TCI':
        sem1 = semestre.get(nom='Semestre 1')
        sem2 = semestre.get(nom='Semestre 2')
    elif Responsable.parcours.nom =='GC2' | Responsable.parcours.nom =='GE2' | Responsable.parcours.nom =='GM2':
        sem1 = semestre.get(nom='Semestre 3')
        sem2 = semestre.get(nom='Semestre 4')
    elif Responsable.parcours.nom == 'GC3' | Responsable.parcours.nom == 'GE3' | Responsable.parcours.nom == 'GM3' | Responsable.parcours.nom == 'STIC3' | Responsable.parcours.nom == 'HE3':
        sem1 = semestre.get(nom='Semestre 5')
        sem2 = semestre.get(nom='Semestre 6')
    else:
        print("Oups!!Il n'y a encore rien pour le moment")

    count1=0
    count2=0

    filtre = AnneeScolaireFilter(request.GET, queryset=ecc)
    EC = filtre.qs
    for sem in EC:
        if sem.niveaux == sem1:
            count1+=1
        else:
            count2+=1
    print('count1 :',count1)
    print("count2 :",count2)
    context = {'Responsable': Responsable,'filtre':filtre,
               'EC': EC,'count1':count1,'count2':count2,'sem1':sem1,'sem2':sem2, }
    return render(request, 'responsables/ec.html', context)

@login_required(login_url='home_enseignant')
def ajout_ec(request,pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    Etudiants = relation.objects.filter(parcours__id=Responsable.parcours.id)

    form = ECForm1()
    if request.method == 'POST':
        form = ECForm1(request.POST)
        if form.is_valid():
            NewEc = form.save()
            print(NewEc)
            for etud in Etudiants:
                notesEtud, created = notes.objects.get_or_create(etudiants_id=etud.id, ec= NewEc)
                print(notesEtud)
        else :
            messages.error(request, "Error")
            form= ECForm1()
    context = {'Responsable': Responsable, 'form':form}
    return render(request, 'responsables/ajout_ec.html',context)

@login_required(login_url='home_enseignant')
def modif_ec(request,pk_resp):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    EC = ec.objects.get(id=pk_resp)
    form = ECForm(instance=EC)
    if request.method == 'POST':
        form = ECForm(request.POST,instance=EC)
        if form.is_valid():
            form.save()
            return redirect('ec',Responsable.id)
        else :
            messages.error(request, "Error")
            form= ECForm(instance=EC)
    context = {'Responsable': Responsable, 'form':form}
    return render(request, 'responsables/modif_ec.html',context)




@login_required(login_url='home_enseignant')
def notes_resp(request, pk_resp):
    Responsable = responsables.objects.get(id=pk_resp)
    Suivis = suivis.objects.all()
    etudiants_suivis = Suivis.filter(etudiant__id=pk_resp)
    rel = relation.objects.all()
    relations = relation.objects.filter(parcours__id=Responsable.parcours.id)

    filtre = relationFilter1(request.GET, queryset=rel)
    rel = filtre.qs
    if request.GET:
        relations = rel.filter(annee_scolaire=request.GET['annee_scolaire'])

    context = {'Responsable': Responsable, 'etudiants_suivis': etudiants_suivis, 'filtre': filtre,
               'relations': relations}
    return render(request, 'responsables/notes.html', context)


@login_required(login_url='home_enseignant')
def affiche_notes(request, pk_etud):
    Enseignant = enseignants.objects.get(utilisateur__id=request.user.id)
    Responsable = responsables.objects.get(enseignant__id=Enseignant.id)
    Etudiants = etudiants.objects.get(id=pk_etud)
    relations = relation.objects.all()
    etud_relations = relations.filter(etudiant__id=pk_etud).order_by('-id')
    total_rel = etud_relations.count()

    annee_scolaire = etud_relations[0].annee_scolaire
    ecs = ec.objects.all()

    Suivis = suivis.objects.all()
    suivi = Suivis.filter(etudiant__id=pk_etud)

    semestre = niveaux.objects.all()
    myfiltre = classeFilter(request.GET, queryset=semestre)
    if suivi:
        message = "Ne plus suivre cet étudiant"
    else:
        message = "Suivre cet étudiant"

    if Responsable.parcours.nom == 'TCI':
        TCI = True
        sem1 = semestre.get(nom='Semestre 1')
        sem2 = semestre.get(nom='Semestre 2')
        Notes = notes.objects.all()
        Moyennes = moyenne.objects.all()

        moyenne1, create = Moyennes.get_or_create(etudiant=Etudiants,semestre=sem1)
        moyenne2, create2 = Moyennes.get_or_create(etudiant=Etudiants,semestre=sem2)

        ecs1 = ec.objects.filter(classe="1ère Année")

        rel1 = "Semestre 1"
        rel2 = "Semestre 2"
    else:
        TCI = False
        rel = myfiltre.qs

    if request.GET:
        rel1 = rel[0]
        rel2 = rel[1]
        sem1 = semestre.get(nom=rel1)
        sem2 = semestre.get(nom=rel2)
        ecs1 = ec.objects.filter(classe=request.GET['classe'])
        moyenne1, created = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=rel1)
        moyenne2, created2 = moyenne.objects.get_or_create(etudiant=Etudiants, semestre=rel2)
    moyenneGeneral1 = float((moyenne1.moyenne + moyenne2.moyenne) / 2)

    if request.POST:
        Totalcoeff =[]
        Totalcoeff1 = []
        Totalc = 0
        Totalc1 = 0
        MOY = 0
        MOY1 = 0
        NTcoeff =[]
        nt=0
        NTcoeff1 = []
        nt1 = 0
        for ecc in ecs1:
            if ecc.niveaux.id == sem1.id:
                for note in Notes:
                    if note.ec.nom == ecc.nom:
                        Note = notes.objects.get(ec__id = ecc.id)
                        noteTp = 'noteT' + ecc.nom
                        notePartiel = 'noteP' + ecc.nom


                        tp = request.POST[noteTp].split(',')
                        tp = '.'.join(tp)
                        p = request.POST[notePartiel].split(',')
                        p = '.'.join(p)

                        NTP = round(float(tp),2)

                        NP = round(float(p),2)

                        if NTP == 0.0:
                            NT = NP
                        else:
                            NT = round((NTP / 3) + ((NP * 2) / 3),2)
                            if NT >= 10.0:
                                ecc.isValid = True
                                ecc.save()
                        NTcoeff.append(round(NT * ecc.coefficient,2))
                        Totalcoeff.append(ecc.coefficient)

                        Note.notesTP=NTP
                        Note.notesPartiel=NP
                        Note.notesTotal=NT
                        Note.etudiants.id = Etudiants.id
                        Note.save()


            if ecc.niveaux.id == sem2.id:
                for note in Notes:
                    if note.ec.nom == ecc.nom:
                        Note1 = notes.objects.get(ec__id = ecc.id)
                        noteTp = 'noteT' + ecc.nom
                        notePartiel = 'noteP' + ecc.nom

                        tp1 = request.POST[noteTp].split(',')
                        tp1 = '.'.join(tp1)
                        p1 = request.POST[notePartiel].split(',')
                        p1 = '.'.join(p1)

                        NTP1 = round(float(tp1),2)

                        NP1 = round(float(p1),2)

                        if NTP1 == 0.0:
                            NT1 = NP1
                        else:
                            NT1 = round((NTP1 / 3) + ((NP1 * 2) / 3),2)
                            if NT1 >= 10.0:
                                ecc.isValid = True
                                ecc.save()
                        NTcoeff1.append(round(NT1 * ecc.coefficient, 2))
                        Totalcoeff1.append(ecc.coefficient)

                        Note1.notesTP=NTP1
                        Note1.notesPartiel=NP1
                        Note1.notesTotal=NT1
                        Note1.etudiants.id = Etudiants.id
                        Note1.save()
        Totalc = sum(Totalcoeff)
        nt = sum(NTcoeff)
        MOY = round(nt,2)/Totalc
        Totalc1 = sum(Totalcoeff1)
        nt1 = sum(NTcoeff1)
        MOY1 = round(nt1, 2) / Totalc1
        moyenne1.moyenne=round(MOY,2)
        moyenne1.save()
        moyenne2.moyenne = round(MOY1, 2)
        moyenne2.save()
        moyenneGeneral1 = float((moyenne1.moyenne + moyenne2.moyenne) / 2)


    context = {'TCI': TCI, 'Responsable': Responsable, 'Etudiants': Etudiants, 'suivi': suivi, 'message': message,
               'ecs': ecs1, 'sem1': sem1, 'sem2': sem2, 'moyenneGeneral1': moyenneGeneral1, 'moyenne1': moyenne1,
               'moyenne2': moyenne2,
               'Notes': Notes, 'myfiltre': myfiltre, 'rel1': rel1, 'rel2': rel2, 'annee': annee_scolaire,
               'etude': etud_relations,
               'total': total_rel,
               }
    return render(request, 'responsables/notes_etudiant.html', context)

# Fin des views pour les responsables
