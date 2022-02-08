//pagination du questionnaire
//chercher les éléments de la pagination du questionnaire

const pages = document.querySelectorAll(".page");
const nbPages = pages.length;//nombre de page du formulaire
let pageActive = 1;
let content = document.querySelector(".nbre");
let element1 = "";


//Chargement de la page
window.onload = () =>{

	//affichage de la première page
	document.querySelector(".page").style.display ="initial";
	
	//on affiche les numéros de page
	pages.forEach((page,index)=>{
		//on crée l'élément "numéro de page"
		let element = document.createElement("p");
		element.classList.add("page-num");
		
		
		if (pageActive===(index+1)){
			element.classList.add("active");
			element.innerHTML = "Page "+(index+1)+"/"+nbPages;
			element1=element;
			content.appendChild(element1);	
				
		};
		
	});

	//on gère les boutons "suivant"
	let btnSuivant = document.querySelectorAll(".suivant");
	for(let bouton of btnSuivant){
		bouton.addEventListener("click", pageSuivante);
	};
	//on gère les boutons "précédent"
	let btnPrecedent = document.querySelectorAll(".precedent");
	for(let bouton of btnPrecedent){
		bouton.addEventListener("click", pagePrecedente);
	};


};

function pageSuivante(){
	pageActive++;
	element1.innerHTML="Page "+(pageActive)+"/"+nbPages;
	content.replaceChild(element1,element1);
	for(let page of pages){
		page.style.display="none";
	};
	

	this.parentElement.nextElementSibling.style.display="initial";


};

function pagePrecedente(){
	pageActive--;
	element1.innerHTML="Page "+(pageActive)+"/"+nbPages;
	content.replaceChild(element1,element1);

	for(let page of pages){
		page.style.display="none";
	};

	this.parentElement.previousElementSibling.style.display="initial";

};



