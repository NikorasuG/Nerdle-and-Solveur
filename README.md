# Nerdle Clone V1.0
## Sommaire

- [À propos](#apropos)
- [Description](#description)
- [Déploiement](#deploiement)
- [Explications](#explication)

## À propos <a name="apropos"></a>

Une application web sur le concept du Nerdle avec un solveur.

## Description <a name="description"></a>

Le but de ce projet est de créer une application web basée sur le concept de Nerdle avec un solveur. Pour le moment, un seul solveur très simple est disponible, d'autres seront probablement ajoutés dans le futur. D'autres modes de jeu ou difficultés pourront également être ajoutés dans le futur.



## Déploiement <a name="deploiement"></a>
### Prérequis

Vous aurez besoin de [Python](https://www.python.org/downloads/) version 3.11.4 et [Node.js](https://nodejs.org/en/download/) version 20.5.1 pour faire fonctionner le projet.

### Installation

Pour installer le front : 
aller dans ```NerdleApp\front``` et exécuter les commandes suivantes : 
```
npm install
npm run dev
```

Pour installer le back :
aller dans ```NerdleApp\back``` et exécuter les commandes suivantes :

```
pip install -r requirements.txt
flask run
```
Enfin il faut creer un fichier ```.env``` par copy du fichier ```.env.example``` et définir le secret.


## Explication

### Règles du jeu

Elles sont disponibles sur la page d'accueil du site, mais je les remets ici
au cas où.

Dans ce jeu l'ordinateur choisit une équation à résoudre, et vous devez la trouver. Pour ce faire vous devez proposer une équation, si ce n'est pas l'équation attendue, les caractères correctement placés seront affichés en vert, les caractères présents mais mal placés seront en jaune et les caractères qui ne sont pas dans la solution seront en rouge. Vous avez 6 essais pour trouver la solution.

### Fonctionnalités
les differents bouton on les fonctionnalités suivantes :
- entrer : valider l'equation
- supprimer : supprimer le dernier caractère
- quitter : retourner au menu principal
- recommencer : recommencer la partie
- aide : demander de l'aide au solveur

le solveur est un solveur trés simple basé sur la théorie de l'information, il donne l'équation donnant le plus d'information parmis les équations possibles.