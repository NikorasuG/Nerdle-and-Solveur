# Nerdle Clone V0.1

## Sommaire

- [À propos](#apropos)
- [Getting Started](#explications)
- [Déploiement](#deploiement)


## À propos <a name="apropos"></a>

Une application web sur le concept du Nerdle avec un solveur.

## Explications <a name="explications"></a>

Le but du jeu est similaire à celui du Wordle. Il faut proposer une équation, si ce n'est pas l'équation attendue, les caractères correctement placés seront affichés en vert, les caractères présents mais mal placés seront en jaune et les caractères qui ne sont pas dans la solution seront en rouge. Voir [Déploiement](#deploiement) pour déployer le projet.


## Déploiement <a name="deploiement"></a>
### Prérequis

J'ai eu la flemme, vérifier juste les modules Python qui vous manquent dans les imports.

### Installation

Pour installer le front : 
aller dans ```NerdleApp\front``` et exécuter les commandes suivantes : 
```
npm install
npm run dev
```

Pour installer le back si vous avez les Prérequis :

```
flask run
```
Enfin il faut creer un fichier ```.env``` par copy du fichier ```.env.example```
