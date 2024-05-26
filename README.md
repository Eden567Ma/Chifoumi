# Chifoumi
## Présentation générale du projet

On propose dans ce projet d'implémenter une version spatialisée du jeu Chifoumi (Pierre, Feuille, Ciseaux). 
On s'inspire librement des verions spatialisées de ce jeu récemment proposées (voir Bibliographie). 
Le principe général du jeu est le suivant: trois types d'objets sont présents sur un terrain (une grille de jeu): des flammes, des potions, ou des citrouilles. La potion bat la flamme, la flamme bat la citrouille, et la citrouille bat la potion (ne me demandez pas pourquoi). 

Dans la configuration initiale, 6 potions, 6 flammes, et 6 citrouilles sont disposées à des positions prédéfinies. Un certain nombre d'autres objets de ces types sont ensuite disposés aléatoirement sur la grille. Les joueurs sont eux-mêmes disposés aléatoirement. Ils vont pouvoir ramasser ces objets et les placer dans leur sac. 

Les joueurs ont une **observabilité partielle de l'environnement**, ce qui signifie qu'ils perçoivent seulement une région autour d'eux (que l'on pourra paramétrer, par exemple en considérant les cases autour du joueur). **Aucune connaissance n'est supposée**: en particulier, les joueurs ne connaissent pas l'état du sac de l'autre joueur, et ils ne connaissent pas les emplacements des différents objets sur la carte. 

Les joueurs jouent **à tour de rôle**, en effectuant un coup à chaque fois. 
Les coups possibles sont:
* le **déplacement** de son joueur. Il est possible de se déplacer d'une case, dans toutes les directions sauf les diagonales. On suppose ici que les joueurs ne se bloquent pas entre eux, et qu'ils peuvent éventuellement être sur la même case à un moment donné. 
* le **déclenchement du chifoumi**. Il faut pour que l'autre joueur se situe dans sa région de visibilité. Toutefois il n'est pas obligatoire de déclencher le chifoumi. 
* lorsqu'un joueur se trouve sur une case comportant un objet d'un certain type, **il le ramasse nécessairement**. 


Lorsqu'un **duel de chifoumi** est déclenché, les règles sont les suivantes:
* chaque joueur joue nécessairement selon une stratégie mixte qui est donnée par la répartition des objets ramassés. Ainsi, un joueur qui aurait ramassé 2 flammes, 1 potion, et 1 citrouille va jouer avec 50% de chance la flamme, avec 25% la potion, et avec 25% la citrouille. Un joueur qui n'a rien ramassé joue selon la stratégie uniforme. Un joueur qui n'a ramassé qu'une citrouille va nécessairement jouer citrouille. 
* Les joueurs reçoivent les gains résultant de la bataille. Les objets sont replacés et une nouvelle partie commence. Les points gagnés sont donnés par la matrice classique : 1 point pour une victoire, 0 pour un match nul, -1 pour une défaite. 
* les parties sont limitées en nombre de tours. Si aucun chifoumi n'a eu lieu à cette limite, la partie est nulle. 
* après le duel de chifoumi ou avoir atteint le nombre de tour max la partie est terminée
* à la fin d'une partie, le joueur perdant réinitialise son sac (et donc sa stratégie). Si il s'agit d'un match nul les deux inventaires sont conservés.  
* puis une nouvelle partie commence en réallouant les joueurs et les objets sur la carte


Un **match** se déroule en un nombre pré-déterminé de parties (par exemple, 10), en cumulant les points. 
En cas d'égalité, c'est le joueur qui a déclenché le plus de batailles de chifoumi qui remporte la manche. 
Les joueurs peuvent se remémorer tout ce qu'ils veulent au cours d'une partie, et même d'un match en entier. Par exemple, le joueur peut se souvenir des coups joués par l'autre joueur lors des précédentes parties. 
 
'un objet de ce type apparait dans sa région de visibilité (on rappelle que la région d'observabilité est limitée), et sans ramasser d'autres objets au passage (**stratégie focused**). Dès qu'un joueur entre dans la région de l'autre joueur, ce dernier déclenche un chifoumi.  
 
# Rapport de projet 




## _Description des choix importants d'implémentation_

Une interface au début du programme permet notamment de choisir les stratégies des deux joueurs ainsi que le nombre de parties du match.
Les stratégies focused et aleatoire sont basées sur les comportements du programme d'origine, mais "réarrangés" pour correspondre aux règles.
Le champ de vision des joueurs a une forme de carré plus ou moins grand (et il est centré sur le joueur).
Toutes les stratégies sont implémentés sous forme de fonctions qui sont appelées à chaque tour et qui mettent à jour toutes les variables nécessaires (position, objets, sac...).
On a une fonction chifoumi qui peut être appelée par les fonctions des stratégies, et qui gère toutes les conséquences de l'issue d'un chifoumi.
Les fonctions des stratégies 3, 4 et 5 utilisent les fonctions focused et aleatoire pour fonctionner.



### _Description des stratégies proposées_

Strat 3 : Stratégie "Majorité"
Le joueur détermine le coup X le plus joué par l'adversaire lors des chifoumis des parties précédentes (depuis le début du match).
Il souhaite donc jouer le coup Y qui bat X.
Il cherche alors les objets Y grâce à la stratégie Focused.

Strat 4 : Stratégie "Majorité alter"
Le joueur détermine le coup X le plus joué par l'adversaire lors des chifoumis des parties précédentes, mais en prenant seulement en compte les coups qui ont été joués après la dernière défaite de l'adversaire, puisque son sac a été réinitialisé à ce moment.
Il souhaite donc jouer le coup Y qui bat X.
Il cherche alors les objets Y grâce à la stratégie Focused.

Strat 5 :
Le joueur détermine l'objet X majoritaire de son sac. 
Il souhaite donc jouer X.
Il cherche alors les objets X grâce à la stratégie Focused.
Cette stratégie est comme Focused, mais change d'"objet préféré" à chaque défaite, et teste ainsi plusieurs objets jusqu'à avoir "trouvé le bon objet".



### _Description des résultats_
Nous avons testé des affrontements entre les différentes stratégies.
Chaque affrontement s'est fait sur 40 matchs de 10 parties chacun (les matchs nuls ne sont pas indiqués), avec un champ de vision qui est un carré de 11 sur 11.
Nous avons choisi de faire tous les affrontements sur l'arène du code original.

Aléatoire vs Focused :
Aléatoire -> 13 victoires
Focused -> 23 victoires
On pourrait expliquer ce résultat par le fait que Focused déclenche des chifoumi et Aléatoire n'en déclenche aucun.

Aléatoire vs Majorité :
Aléatoire -> 18 victoires
Majorité -> 22 victoires
Majorité n'est pas pertinent contre Aléatoire puisque les coups de Aléatoire fluctuent trop.

Aléatoire vs Majorité alter :
Aléatoire -> 16 victoires
Majorité alter -> 24 victoires
Majorité alter est plus pertinent que Majorité contre aléatoire car il essaye réellement d'estimer le coup majoritaire du sac adverse.

Focused vs Majorité :
Focused -> 7 victoires
Majorité -> 33 victoires
Majorité est bien adapté pour estimer l'objet qui est recherché par une stratégie Focused.

Focused vs Majorité alter :
Focused -> 12 victoires
Majorité alter -> 28 victoires
Majorité alter est moins bien adapté que Majorité pour estimer l'objet qui est recherché par une stratégie Focused, mais il est quand même efficace.

Majorité vs Majorité alter:
Majorité -> 12 victoires
Majorité alter -> 27 victoires
Majorité n'est pas pertinent contre Aléatoire puisque Majorité alter réadapte trop souvent sa stratégie pour contrer Majorité.


Aléatoire vs Spécialisation :
Aléatoire -> 21 victoires
Spécialisation -> 19 victoires

Focused vs Spécialisation :
Focused -> 22 victoires
Spécialisation -> 18 victoires

Majorité vs Spécialisation:
Majorité -> 23 victoires
Spécialisation -> 17 victoires

Majorité alter vs Spécialisation:
Majorité alter -> 29 victoires
Spécialisation -> 10 victoires

Spécialisation semble ne jamais être efficace. Peut-être qu'il faudrait des parties beaucoup plus longues pour qu'il devienne un peu efficace.
