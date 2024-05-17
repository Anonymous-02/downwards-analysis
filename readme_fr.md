# analyse descendante

## Methode d'utilisation

1. placer les fichiers .pas du projet dans le meme dossier que les fichiers info.txt et main.py
2. mettre le nom du fihier pricipal sans oublier l'extension .pas à la place de la 1e ligne du fichier info.txt
3. mettre la liste des modules à ignorer a la place de la 2e ligne du fichier info.txt
   les modules a inorer sont les librairies externes et celles contenant des classes
4.(optionel) executez le setup de graphviz, cochez l'option "add graphviz to the system path for current user" et redemarrez votre ordinateur une fois l'installation terminée pour obtenir la version imagée de l'analyse descendante
5. lancez main.py si cela echoue essayez d'installer python, si cela echoue toujours essayez de l'installer dans le dossier actuel
## Restricitions

1. ce programme ne fonctionne pas avec des classes
2. ce programme ne fait pas la différence entre les fonctions de meme nom
3. ce programme ne fait pas la différence entre fonctions et variables si elles ont le meme nom 

   cela pourrait etre problématique avec la façon dont les fonctions sont implémentés en pascal, mais la récursivité n'est pas prise en compte