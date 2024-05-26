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
