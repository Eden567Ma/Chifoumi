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
 

